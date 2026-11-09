"""Painel 'Roteadores' na barra lateral do HA + API usada por ele.

A interface é a mesma do painel do PC (desktop/painel.html), empacotada em
frontend/miwifi-panel.js pelo script tools/build_ha_panel.py.
"""
from __future__ import annotations

import re
from http import HTTPStatus
from pathlib import Path
from typing import Any

from aiohttp import web

from homeassistant.components import frontend, panel_custom
from homeassistant.components.http import HomeAssistantView, StaticPathConfig
from homeassistant.core import HomeAssistant

from .const import DOMAIN

URL_BASE = "/miwifi_ax_static"
PAINEL_PATH = "roteadores"
WEBCOMPONENT = "miwifi-ax-panel"

ESCRITA = re.compile(
    r"(^|/)(set_|add_|del|remove|reboot|reset|shutdown|upgrade|flash|login|logout|"
    r"c_restore|c_upload|c_backup|bandwidth_test|scan_|qos_mode|qos_limit|qos_offlimit|qos_guest|"
    r"unbind|bind|apply|start|stop|clean|clear|format|repair|register|renew|grant|update|connect|"
    r"wps$|wps_cancel|iperf|speed_test$|ota$|password|disable|edit_|manually_|mac_clone|r_ip_conflict|"
    r"usb_u3|usbservice|usbmode|upload|web_access_opt|led$|netacctl_set|parctl_(add|delete|update)|request)"
    r"|switch",
    re.I,
)
SENSIVEIS = re.compile(r"(pass|pwd|psk|key|token|stok|secret|sswd|senha)", re.I)
PAGINAS = [
    "web/home", "web/setting/wifi", "web/setting/wan", "web/setting/lannetset",
    "web/setting/safe", "web/setting/upgrade", "web/apsetting/wifi", "web/store", "web/prosetting/qos",
]
EXTRAS = [
    "api/misns/wifi_share_info", "api/misystem/status", "api/misystem/sys_time", "api/misystem/led",
    "api/xqnetwork/wan_info", "api/xqnetwork/wifi_detail_all", "api/misystem/devicelist",
    "api/misystem/topo_graph", "api/misystem/messages", "api/misystem/qos_info",
    "api/misystem/arn_status", "api/misystem/arn_records", "api/misystem/arn_security",
    "api/misystem/router_common_status", "api/misystem/qos_info_new", "api/misystem/channel_scan_result",
    "api/misystem/smartvpn_info", "api/xqsystem/vpn", "api/xqsystem/vpn_status", "api/xqsystem/wps_status",
    "api/xqsystem/push_settings", "api/xqsystem/system_info", "api/xqnetwork/get_son_backhaul_mode",
    "api/xqnetwork/get_miscan_switch", "api/xqnetwork/get_miotrelay_switch", "api/xqsystem/country_code",
]


def _mascarar(obj: Any, mostrar: bool) -> Any:
    if mostrar:
        return obj
    if isinstance(obj, dict):
        return {
            k: ("••••••" if SENSIVEIS.search(k) and isinstance(v, (str, int)) and v != "" else _mascarar(v, False))
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [_mascarar(v, False) for v in obj]
    return obj


def _coords(hass: HomeAssistant) -> dict[str, Any]:
    """{chave: coordenador}. Um principal = 'principal'; um nó = 'repetidor';
    com vários nós, 'repetidor (<local ou nome>)'. Chaves sempre únicas."""
    cs = [c for c in hass.data.get(DOMAIN, {}).values() if c.role]
    out: dict[str, Any] = {}
    for papel in ("principal", "repetidor"):
        grupo = sorted((c for c in cs if c.role == papel), key=lambda c: c.api.host)
        for c in grupo:
            if len(grupo) == 1:
                k = papel
            else:
                d = c.data or {}
                k = f"{papel} ({d.get('local') or d.get('nome') or c.api.host})"
            if k in out:
                k = f"{papel} ({c.api.host})"
            out[k] = c
    return out


class _Base(HomeAssistantView):
    requires_auth = True

    def _admin(self, request: web.Request) -> bool:
        user = request.get("hass_user")
        return bool(user and user.is_admin)


class EstadoView(_Base):
    url = "/api/miwifi_ax/estado"
    name = "api:miwifi_ax:estado"

    async def get(self, request: web.Request) -> web.Response:
        if not self._admin(request):
            return self.json_message("Somente administradores", HTTPStatus.FORBIDDEN)
        cs = _coords(request.app["hass"])
        return self.json({
            "roteadores": {r: c.api.host for r, c in cs.items()},
            "logado": {r: True for r in cs},
            "papeis": {r: c.role for r, c in cs.items()},
        })


class ChamarView(_Base):
    url = "/api/miwifi_ax/chamar"
    name = "api:miwifi_ax:chamar"

    async def post(self, request: web.Request) -> web.Response:
        if not self._admin(request):
            return self.json_message("Somente administradores", HTTPStatus.FORBIDDEN)
        corpo = await request.json()
        c = _coords(request.app["hass"]).get(corpo.get("roteador"))
        if not c:
            return self.json({"ok": False, "erro": "roteador não configurado na integração"})
        ep = str(corpo.get("endpoint", "")).lstrip("/")
        ep = ep[4:] if ep.startswith("api/") else ep
        metodo = corpo.get("metodo", "GET")
        escrita = bool(ESCRITA.search(ep.split("/")[-1])) or metodo == "POST"
        if escrita and not corpo.get("confirmado"):
            return self.json({"ok": False, "erro": "Este endpoint altera o roteador: confirme antes."})
        try:
            j = await c.api.call(ep, corpo.get("params") or None, post=(metodo == "POST"))
        except Exception as err:  # noqa: BLE001
            return self.json({"ok": False, "erro": str(err)})
        if escrita:
            await c.async_request_refresh()
        return self.json({"ok": True, "status": 200, "json": _mascarar(j, bool(corpo.get("mostrar")))})


class EndpointsView(_Base):
    url = "/api/miwifi_ax/endpoints"
    name = "api:miwifi_ax:endpoints"

    async def get(self, request: web.Request) -> web.Response:
        if not self._admin(request):
            return self.json_message("Somente administradores", HTTPStatus.FORBIDDEN)
        c = _coords(request.app["hass"]).get(request.query.get("roteador", ""))
        if not c:
            return self.json([])
        if getattr(c, "_eps_cache", None) is None:
            achados = set(EXTRAS)
            for p in PAGINAS:
                try:
                    html = await c.api.page(p)
                except Exception:  # noqa: BLE001
                    continue
                achados.update(re.findall(r"api/[a-z_]+/[a-z_0-9]+", html, re.I))
            c._eps_cache = sorted(
                ({"endpoint": e, "escrita": bool(ESCRITA.search(e.split("/", 2)[-1]))} for e in achados),
                key=lambda d: (d["escrita"], d["endpoint"]),
            )
        return self.json(c._eps_cache)


async def async_registrar(hass: HomeAssistant) -> None:
    """Registra API, arquivos e o painel (uma vez)."""
    if hass.data.get(f"{DOMAIN}_painel"):
        return
    hass.data[f"{DOMAIN}_painel"] = True
    hass.http.register_view(EstadoView())
    hass.http.register_view(ChamarView())
    hass.http.register_view(EndpointsView())
    pasta = Path(__file__).parent / "frontend"
    await hass.http.async_register_static_paths([StaticPathConfig(URL_BASE, str(pasta), False)])
    versao = int((pasta / "miwifi-panel.js").stat().st_mtime)
    await panel_custom.async_register_panel(
        hass,
        webcomponent_name=WEBCOMPONENT,
        frontend_url_path=PAINEL_PATH,
        module_url=f"{URL_BASE}/miwifi-panel.js?v={versao}",
        sidebar_title="Roteadores" if (hass.config.language or "").lower().startswith("pt") else "Routers",
        sidebar_icon="mdi:router-wireless",
        require_admin=True,
        config={},
    )


def async_remover(hass: HomeAssistant) -> None:
    if hass.data.pop(f"{DOMAIN}_painel", None):
        frontend.async_remove_panel(hass, PAINEL_PATH)
