"""Local integration for Xiaomi AX1800 (RM1800) routers."""
from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import SOURCE_INTEGRATION_DISCOVERY, ConfigEntry
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv, device_registry as dr
from homeassistant.helpers.aiohttp_client import async_create_clientsession, async_get_clientsession
from homeassistant.util import dt as dt_util, slugify

from .api import MiWiFiApi
from .const import CONF_MESMA_SENHA, CONF_NOS_REMOVIDOS, CONF_PAINEL, DOMAIN, PAINEL_PADRAO, PLATFORMS, ROLE_MAIN
from .canal import CanalAuto
from .coordinator import MiWiFiCoordinator
from .painel import async_registrar, async_remover

SERVICE_INTERNET = "definir_internet"
SCHEMA_INTERNET = vol.Schema({vol.Required("mac"): cv.string, vol.Required("liberar"): cv.boolean})
SERVICE_LOG = "salvar_log"
SCHEMA_LOG = vol.Schema({vol.Optional("device_id"): vol.All(cv.ensure_list, [cv.string])})
PASTA_LOGS = "miwifi_ax_logs"
LOGS_POR_ROTEADOR = 20


async def salvar_log(hass: HomeAssistant, coord) -> dict:
    """Asks the router for its system-log package (misystem/sys_log) and saves it in /config/miwifi_ax_logs.

    The router's persistent log (/data/usr/log/messages) rotates in about 1.5 h, so it has to be fetched soon
    after an unexpected restart to still contain the lines before it. The package includes the Wi-Fi
    passwords (base64, in mimesh.log), so it stays local. Keeps the newest LOGS_POR_ROTEADOR per router.
    """
    j = await coord.api.call("misystem/sys_log")
    caminho = str(j.get("path") or "")
    if j.get("code") != 0 or "/backup/log/" not in caminho:
        raise HomeAssistantError(translation_domain=DOMAIN, translation_key="roteador_recusou", translation_placeholders={"detalhe": str(j)})
    url = f"http://{coord.api.host}/backup/log/" + caminho.split("/backup/log/", 1)[1]
    async with async_get_clientsession(hass).get(url, timeout=aiohttp.ClientTimeout(total=60)) as r:
        r.raise_for_status()
        dados = await r.read()
    nome = slugify(coord.name) or coord.api.host.replace(".", "_")
    pasta = Path(hass.config.path(PASTA_LOGS))
    arq = pasta / f"{nome}_{dt_util.now().strftime('%Y%m%d-%H%M%S')}.tar.gz"

    def _gravar() -> None:
        pasta.mkdir(exist_ok=True)
        arq.write_bytes(dados)
        for velho in sorted(pasta.glob(f"{nome}_*.tar.gz"))[:-LOGS_POR_ROTEADOR]:
            velho.unlink()

    await hass.async_add_executor_job(_gravar)
    return {"roteador": coord.name, "arquivo": str(arq), "bytes": len(dados)}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    session = async_create_clientsession(hass)
    api = MiWiFiApi(session, entry.data[CONF_HOST], entry.data[CONF_PASSWORD])
    coord = MiWiFiCoordinator(hass, api, entry.title, entry.entry_id)
    coord.painel_url = entry.options.get(CONF_PAINEL, PAINEL_PADRAO)
    await coord.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coord
    if coord.role == ROLE_MAIN:
        # periodic Zigbee-aware channel search (options); also used by the panel API and the sensor
        coord.canal_auto = CanalAuto(hass, entry, coord)
        await coord.canal_auto.async_start()
        entry.async_on_unload(coord.canal_auto.async_stop)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await async_registrar(hass)
    entry.async_on_unload(entry.add_update_listener(_reload))

    if coord.role == ROLE_MAIN:
        async def _procurar_nos(_now=None) -> None:
            """Offers to set up every Mesh node not configured yet."""
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
                        raise HomeAssistantError(translation_domain=DOMAIN, translation_key="roteador_recusou", translation_placeholders={"detalhe": str(j)})
                    await c.async_request_refresh()
                    return
            raise HomeAssistantError(translation_domain=DOMAIN, translation_key="sem_principal")

        hass.services.async_register(DOMAIN, SERVICE_INTERNET, _internet, schema=SCHEMA_INTERNET)

    if not hass.services.has_service(DOMAIN, SERVICE_LOG):
        async def _log(call: ServiceCall) -> ServiceResponse:
            alvos = list(hass.data.get(DOMAIN, {}).items())
            if call.data.get("device_id"):
                reg = dr.async_get(hass)
                ids = {e for d in call.data["device_id"] if (dev := reg.async_get(d)) for e in dev.config_entries}
                alvos = [(i, c) for i, c in alvos if i in ids]
            salvos = []
            for _id, c in alvos:
                try:
                    salvos.append(await salvar_log(hass, c))
                except Exception as err:  # noqa: BLE001
                    salvos.append({"roteador": c.name, "erro": str(err)})
            return {"arquivos": salvos}

        hass.services.async_register(DOMAIN, SERVICE_LOG, _log, schema=SCHEMA_LOG, supports_response=SupportsResponse.OPTIONAL)
    return True


async def async_remove_config_entry_device(hass: HomeAssistant, entry: ConfigEntry, device) -> bool:
    """Allows removing tracked devices (not the routers themselves)."""
    return not any(i[0] == DOMAIN for i in device.identifiers)


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Mesh node deleted by the user: the main router remembers it so it is not re-added automatically."""
    if not entry.data.get(CONF_MESMA_SENHA):
        return
    host = entry.data.get(CONF_HOST)
    for e in hass.config_entries.async_entries(DOMAIN):
        if e.entry_id != entry.entry_id and not e.data.get(CONF_MESMA_SENHA):
            nos = list(e.data.get(CONF_NOS_REMOVIDOS, []))
            if host and host not in nos:
                hass.config_entries.async_update_entry(e, data={**e.data, CONF_NOS_REMOVIDOS: nos + [host]})


async def _reload(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, SERVICE_INTERNET)
            hass.services.async_remove(DOMAIN, SERVICE_LOG)
            async_remover(hass)
    return ok
