"""Coordenador: lê tudo do roteador a cada ciclo."""
from __future__ import annotations

import logging
import time
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MiWiFiApi, MiWiFiAuthError, MiWiFiConnError
from .const import CONN_TYPE, DOMAIN, ROLE_MAIN, ROLE_NODE, SCAN_INTERVAL_S

_LOGGER = logging.getLogger(__name__)


def _f(v, d=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return d


class MiWiFiCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, api: MiWiFiApi, name: str) -> None:
        super().__init__(hass, _LOGGER, name=f"{DOMAIN} {name}", update_interval=timedelta(seconds=SCAN_INTERVAL_S))
        self.api = api
        self.role: str | None = None
        self.hw: dict[str, Any] = {}
        self.devices: dict[str, dict[str, Any]] = {}

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self._fetch()
        except MiWiFiAuthError as err:
            raise ConfigEntryAuthFailed(str(err)) from err
        except MiWiFiConnError as err:
            raise UpdateFailed(f"roteador inacessível: {err}") from err

    async def _fetch(self) -> dict[str, Any]:
        a = self.api
        st = await a.call("misystem/status")
        tm = await a.safe("misystem/sys_time")
        self.role = ROLE_MAIN if tm.get("role", "whc_cap") != "whc_re" else ROLE_NODE
        self.hw = st.get("hardware") or {}
        t = tm.get("time") or {}
        led = await a.safe("misystem/led")
        msg = await a.safe("misystem/messages")
        wf = await a.safe("xqnetwork/wifi_detail_all")
        ns = await a.safe("misystem/newstatus")
        nm = await a.safe("misystem/router_name")
        info = wf.get("info") or []
        d: dict[str, Any] = {
            "ligado_ha": int(_f(st.get("upTime"))),
            "cpu": round(_f((st.get("cpu") or {}).get("load")) * 100, 1),
            "memoria": round(_f((st.get("mem") or {}).get("usage")) * 100, 1),
            "led": led.get("status") == 1,
            "avisos": msg.get("count", 0),
            "clientes_24": (ns.get("2g") or {}).get("online_sta_count"),
            "clientes_5": (ns.get("5g") or {}).get("online_sta_count"),
            "firmware": self.hw.get("version"),
            "nome": nm.get("name"),
            "local": nm.get("locale"),
        }
        if t:
            hora = f"{t['year']:04d}-{t['month']:02d}-{t['day']:02d} {t['hour']:02d}:{t['min']:02d}:{t['sec']:02d}"
            d["hora_roteador"] = hora
            try:
                d["relogio_diferenca"] = int(time.mktime(time.strptime(hora, "%Y-%m-%d %H:%M:%S")) - time.time())
            except ValueError:
                pass
        for i, w in enumerate(info[:2]):
            b = "24" if i == 0 else "5"
            ci = w.get("channelInfo") or {}
            d[f"canal_{b}"] = ci.get("channel") or w.get("channel")
            d[f"largura_{b}"] = ci.get("bandwidth") or w.get("bandwidth")
            d[f"potencia_{b}"] = {"max": "máxima", "mid": "padrão", "min": "economia"}.get(w.get("txpwr"), w.get("txpwr"))
            d[f"wifi_{b}"] = w.get("status") == "1"
        if self.role == ROLE_NODE:
            sig = await a.safe("xqnetwork/wifiap_signal")
            if "signal" in sig:
                d["sinal_ate_principal"] = sig.get("signal")
            return d

        # ---- só no principal ----
        cnt = st.get("count") or {}
        d["aparelhos_online"] = cnt.get("online")
        d["aparelhos_conhecidos"] = cnt.get("all")
        d["mu_mimo"] = any(w.get("txbf") == "1" for w in info)
        d["modo_wifi5"] = any(w.get("ax") == "0" for w in info)
        d["wifi_unificado"] = wf.get("bsd") == 1
        d["conexao_rapida"] = (await a.safe("xqnetwork/get_miotrelay_switch")).get("enabled") == 1
        d["varredura_aiot"] = (await a.safe("xqnetwork/get_miscan_switch")).get("enabled") == 1
        d["prioridade_muitos_aparelhos"] = str((await a.safe("xqnetwork/get_son_backhaul_mode")).get("mode")) == "1"
        gi = (await a.safe("misns/wifi_share_info")).get("info") or {}
        d["visitante"] = gi.get("guest") == 1
        d["visitante_ssid"] = (gi.get("data") or {}).get("ssid")
        d["_visitante_cfg"] = gi.get("data") or {}
        q = await a.safe("misystem/qos_info")
        d["qos"] = (q.get("status") or {}).get("on") == 1
        arn = await a.safe("misystem/arn_status")
        sec = await a.safe("misystem/arn_security")
        d["anti_intrusos"] = arn.get("open") == 1
        d["anti_intrusos_nivel"] = arn.get("level")
        d["intrusoes_bloqueadas"] = arn.get("count")
        d["firewall_sites"] = sec.get("malicious_url_firewall") == 1
        d["firewall_virus"] = sec.get("virus_file_firewall") == 1
        mf = await a.safe("xqnetwork/wifi_macfilter_info")
        d["filtro_mac"] = mf.get("enable") == 1
        d["_filtro_mac_modo"] = mf.get("model", 0)
        d["filtro_mac_lista"] = [{"nome": x.get("name"), "mac": x.get("mac")} for x in mf.get("macfilter") or []]
        d["filtro_mac_qtd"] = len(d["filtro_mac_lista"])
        d["vpn_status"] = (await a.safe("xqsystem/vpn_status")).get("status")
        d["wps"] = (await a.safe("xqsystem/wps_status")).get("status") == 1
        tp = (await a.safe("misystem/topo_graph")).get("graph") or {}
        d["repetidor_na_mesh"] = len(tp.get("leafs") or []) > 0
        # WAN
        w = (await a.safe("xqnetwork/wan_info")).get("info") or {}
        lk = await a.safe("xqnetwork/wan_link")
        v4 = (w.get("ipv4") or [{}])[0]
        wan = st.get("wan") or {}
        d.update({
            "internet": bool(v4.get("ip")) and lk.get("link") == 1,
            "wan_cabo": lk.get("link") == 1,
            "ip_publico": v4.get("ip"),
            "ipv6": ((w.get("ipv6_info") or {}).get("ip6addr") or [None])[0],
            "internet_conectada_ha": w.get("uptime"),
            "gateway_wan": w.get("gateWay"),
            "dns": ", ".join((w.get("details") or {}).get("dns") or []),
            "download": round(_f(wan.get("downspeed")) * 8 / 1000, 1),
            "upload": round(_f(wan.get("upspeed")) * 8 / 1000, 1),
            "pico_download": round(_f(wan.get("maxdownloadspeed")) * 8 / 1000, 1),
            "pico_upload": round(_f(wan.get("maxuploadspeed")) * 8 / 1000, 1),
            "total_baixado": round(_f(wan.get("download")) / 1048576, 1),
            "total_enviado": round(_f(wan.get("upload")) / 1048576, 1),
        })
        upd = await a.safe("xqsystem/check_rom_update")
        d["firmware_atualizacao"] = upd.get("needUpdate") == 1
        d["firmware_nova"] = upd.get("version")
        # reservas
        mb = (await a.safe("xqnetwork/macbind_info")).get("list") or []
        d["reservas"] = sorted(
            ({"nome": r.get("name"), "mac": (r.get("mac") or "").upper(), "ip": r.get("ip")} for r in mb),
            key=lambda r: [int(x) for x in str(r["ip"]).split(".") if x.isdigit()],
        )
        d["qtd_reservas"] = len(mb)
        # aparelhos
        grupos: dict[str, list[str]] = {"cabo": [], "2,4 GHz": [], "5 GHz": [], "visitante": []}
        devs: dict[str, dict[str, Any]] = {}
        for x in (await a.safe("misystem/devicelist")).get("list") or []:
            mac = (x.get("mac") or "").upper()
            ip = ((x.get("ip") or [{}])[0]) or {}
            con = CONN_TYPE.get(x.get("type"), "outro")
            devs[mac] = {
                "nome": x.get("name") or x.get("oname") or mac,
                "online": bool(x.get("online")),
                "ip": ip.get("ip"),
                "conexao": con,
                "isap": x.get("isap"),
                "download": round(_f(ip.get("downspeed")) * 8 / 1000, 1),
                "upload": round(_f(ip.get("upspeed")) * 8 / 1000, 1),
                "online_ha": int(_f(ip.get("online"))),
                "internet_liberada": (x.get("authority") or {}).get("wan", 1) == 1,
                "via_repetidor": bool(x.get("parent")),
            }
            if x.get("online") and not x.get("isap"):
                grupos.setdefault(con, []).append(f"{devs[mac]['nome']} ({ip.get('ip', '')})")
        self.devices = devs
        d["grupos"] = grupos
        for k, n in (("cabo", "cabo"), ("24", "2,4 GHz"), ("5", "5 GHz"), ("visitante", "visitante")):
            d[f"qtd_{k}"] = len(grupos.get(n, []))
        return d
