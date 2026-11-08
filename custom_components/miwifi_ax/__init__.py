"""Integração local dos roteadores Xiaomi AX1800 (RM1800)."""
from __future__ import annotations

from datetime import timedelta

import voluptuous as vol

from homeassistant.config_entries import SOURCE_INTEGRATION_DISCOVERY, ConfigEntry
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import MiWiFiApi
from .const import CONF_PAINEL, DOMAIN, PAINEL_PADRAO, PLATFORMS, ROLE_MAIN
from .coordinator import MiWiFiCoordinator
from .painel import async_registrar, async_remover

SERVICE_INTERNET = "definir_internet"
SCHEMA_INTERNET = vol.Schema({vol.Required("mac"): cv.string, vol.Required("liberar"): cv.boolean})


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    session = async_create_clientsession(hass)
    api = MiWiFiApi(session, entry.data[CONF_HOST], entry.data[CONF_PASSWORD])
    coord = MiWiFiCoordinator(hass, api, entry.title, entry.entry_id)
    coord.painel_url = entry.options.get(CONF_PAINEL, PAINEL_PADRAO)
    await coord.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coord
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await async_registrar(hass)
    entry.async_on_unload(entry.add_update_listener(_reload))

    if coord.role == ROLE_MAIN:
        async def _procurar_nos(_now=None) -> None:
            """Oferece para configurar cada nó da Mesh ainda não cadastrado."""
            topo = (await coord.api.safe("misystem/topo_graph")).get("graph") or {}
            ja = {e.data.get(CONF_HOST) for e in hass.config_entries.async_entries(DOMAIN)}
            for no in topo.get("leafs") or []:
                ip = no.get("ip")
                if ip and ip not in ja:
                    hass.async_create_task(hass.config_entries.flow.async_init(
                        DOMAIN,
                        context={"source": SOURCE_INTEGRATION_DISCOVERY},
                        data={CONF_HOST: ip, "nome": no.get("name") or no.get("locale") or ip, "principal": entry.entry_id},
                    ))

        entry.async_create_background_task(hass, _procurar_nos(), f"{DOMAIN}_procurar_nos")
        entry.async_on_unload(async_track_time_interval(hass, _procurar_nos, timedelta(hours=6)))

    if not hass.services.has_service(DOMAIN, SERVICE_INTERNET):
        async def _internet(call: ServiceCall) -> None:
            mac = call.data["mac"].upper()
            for c in hass.data.get(DOMAIN, {}).values():
                if c.role == ROLE_MAIN:
                    j = await c.api.call("xqsystem/set_mac_filter", {"mac": mac, "wan": 1 if call.data["liberar"] else 0})
                    if j.get("code") != 0:
                        raise HomeAssistantError(f"Roteador recusou: {j}")
                    await c.async_request_refresh()
                    return
            raise HomeAssistantError("Nenhum roteador principal configurado")

        hass.services.async_register(DOMAIN, SERVICE_INTERNET, _internet, schema=SCHEMA_INTERNET)
    return True


async def async_remove_config_entry_device(hass: HomeAssistant, entry: ConfigEntry, device) -> bool:
    """Permite desvincular aparelhos rastreados (não os próprios roteadores)."""
    return not any(i[0] == DOMAIN for i in device.identifiers)


async def _reload(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, SERVICE_INTERNET)
            async_remover(hass)
    return ok
