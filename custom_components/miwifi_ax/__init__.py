"""Integração local dos roteadores Xiaomi AX1800 (RM1800)."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
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
