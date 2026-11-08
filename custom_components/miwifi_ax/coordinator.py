"""Coordenador: consulta o roteador a cada ciclo — só o que as entidades ATIVADAS usam."""
from __future__ import annotations

import logging
import time
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MiWiFiApi, MiWiFiAuthError, MiWiFiConnError
from .const import CONN_TYPE, DOMAIN, ROLE_MAIN, ROLE_NODE, SCAN_INTERVAL_S

_LOGGER = logging.getLogger(__name__)
FIRMWARE_INTERVALO_S = 6 * 3600  # check_rom_update consulta os servidores da Xiaomi

# chave da entidade -> grupo de consulta (endpoint). Chaves ausentes vêm do misystem/status (sempre lido).
GRUPO = {
    "led": "led", "avisos": "msg",
    "canal_24": "wifi", "canal_5": "wifi", "largura_24": "wifi", "largura_5": "wifi",
    "potencia_24": "wifi", "potencia_5": "wifi", "wifi_24": "wifi", "wifi_5": "wifi",
    "mu_mimo": "wifi", "modo_wifi5": "wifi", "wifi_unificado": "wifi",
    "clientes_24": "newstatus", "clientes_5": "newstatus",
    "hora_roteador": "time", "relogio_diferenca": "time",
    "sinal_ate_principal": "signal",
    "conexao_rapida": "miot", "varredura_aiot": "miscan", "prioridade_muitos_aparelhos": "backhaul",
    "visitante": "guest", "visitante_ssid": "guest", "qos": "qos",
    "anti_intrusos": "arn", "anti_intrusos_nivel": "arn", "intrusoes_bloqueadas": "arn",
    "firewall_sites": "sec", "firewall_virus": "sec",
    "filtro_mac": "macfilter", "filtro_mac_qtd": "macfilter",
    "vpn_status": "vpn", "wps": "wps", "repetidor_na_mesh": "topo",
    "internet": "wan", "wan_cabo": "wan", "ip_publico": "wan", "ipv6": "wan", "internet_conectada_ha": "wan",
    "gateway_wan": "wan", "dns": "wan",
    "firmware_atualizacao": "upd", "qtd_reservas": "macbind",
    "qtd_cabo": "devices", "qtd_24": "devices", "qtd_5": "devices", "qtd_visitante": "devices",
}


def _f(v, d=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return d


class MiWiFiCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, api: MiWiFiApi, name: str, entry_id: str | None = None) -> None:
        super().__init__(hass, _LOGGER, name=f"{DOMAIN} {name}", update_interval=timedelta(seconds=SCAN_INTERVAL_S))
        self.api = api
        self.entry_id = entry_id
        self.role: str | None = None
        self.hw: dict[str, Any] = {}
        self.devices: dict[str, dict[str, Any]] = {}
        self._primeira = True
        self._nome: dict[str, Any] = {}
        self._upd: dict[str, Any] = {}
        self._upd_t = 0.0

    def _grupos(self) -> set[str] | None:
        """Grupos necessários pelas entidades ativadas. None = tudo (primeira leitura)."""
        if self._primeira or not self.entry_id:
            return None
        reg = er.async_get(self.hass)
        g: set[str] = set()
        for e in er.async_entries_for_config_entry(reg, self.entry_id):
            if e.disabled_by is not None:
                continue
            if e.domain == "device_tracker":
                g.add("devices")
                continue
            uid = e.unique_id or ""
            key = uid.split("_", 1)[1] if "_" in uid else uid
            key = key[3:] if key.startswith("sw_") else key
            if key in GRUPO:
                g.add(GRUPO[key])
        return g

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            d = await self._fetch()
            self._primeira = False
            return d
        except MiWiFiAuthError as err:
            raise ConfigEntryAuthFailed(str(err)) from err
        except MiWiFiConnError as err:
            raise UpdateFailed(f"roteador inacessível: {err}") from err

    async def _fetch(self) -> dict[str, Any]:
        a = self.api
        g = self._grupos()
        quer = (lambda x: True) if g is None else (lambda x: x in g)
        d: dict[str, Any] = {}

        st = await a.call("misystem/status")
        self.hw = st.get("hardware") or {}
        if self.role is None or quer("time"):
            tm = await a.safe("misystem/sys_time")
            self.role = ROLE_NODE if tm.get("role") == "whc_re" else ROLE_MAIN
            t = tm.get("time") or {}
            if t:
                hora = f"{t['year']:04d}-{t['month']:02d}-{t['day']:02d} {t['hour']:02d}:{t['min']:02d}:{t['sec']:02d}"
                d["hora_roteador"] = hora
                try:
                    d["relogio_diferenca"] = int(time.mktime(time.strptime(hora, "%Y-%m-%d %H:%M:%S")) - time.time())
                except ValueError:
                    pass
        if not self._nome:
            self._nome = await a.safe("misystem/router_name")
        d.update({
            "ligado_ha": int(_f(st.get("upTime"))),
            "cpu": round(_f((st.get("cpu") or {}).get("load")) * 100, 1),
            "memoria": round(_f((st.get("mem") or {}).get("usage")) * 100, 1),
            "firmware": self.hw.get("version"),
            "nome": self._nome.get("name"),
            "local": self._nome.get("locale"),
        })
        if quer("led"):
            d["led"] = (await a.safe("misystem/led")).get("status") == 1
        if quer("msg"):
            d["avisos"] = (await a.safe("misystem/messages")).get("count", 0)
        if quer("newstatus"):
            ns = await a.safe("misystem/newstatus")
            d["clientes_24"] = (ns.get("2g") or {}).get("online_sta_count")
            d["clientes_5"] = (ns.get("5g") or {}).get("online_sta_count")
        if quer("wifi"):
            wf = await a.safe("xqnetwork/wifi_detail_all")
            info = wf.get("info") or []
            for i, w in enumerate(info[:2]):
                b = "24" if i == 0 else "5"
                ci = w.get("channelInfo") or {}
                d[f"canal_{b}"] = ci.get("channel") or w.get("channel")
                lg = str(ci.get("bandwidth") or w.get("bandwidth") or "0")
                d[f"largura_{b}"] = "automática" if lg == "0" else f"{lg} MHz"
                d[f"potencia_{b}"] = {"max": "máxima", "mid": "padrão", "min": "economia"}.get(w.get("txpwr"), w.get("txpwr"))
                d[f"wifi_{b}"] = w.get("status") == "1"
            if self.role == ROLE_MAIN:
                d["mu_mimo"] = any(w.get("txbf") == "1" for w in info)
                d["modo_wifi5"] = any(w.get("ax") == "0" for w in info)
                d["wifi_unificado"] = wf.get("bsd") == 1

        if self.role == ROLE_NODE:
            if quer("signal"):
                sig = await a.safe("xqnetwork/wifiap_signal")
                if "signal" in sig:
                    d["sinal_ate_principal"] = sig.get("signal")
            return d

        # ---- só no principal ----
        cnt = st.get("count") or {}
        wan = st.get("wan") or {}
        d.update({
            "aparelhos_online": cnt.get("online"),
            "aparelhos_conhecidos": cnt.get("all"),
            "download": round(_f(wan.get("downspeed")) * 8 / 1000, 1),
            "upload": round(_f(wan.get("upspeed")) * 8 / 1000, 1),
            "pico_download": round(_f(wan.get("maxdownloadspeed")) * 8 / 1000, 1),
            "pico_upload": round(_f(wan.get("maxuploadspeed")) * 8 / 1000, 1),
            "total_baixado": round(_f(wan.get("download")) / 1048576, 1),
            "total_enviado": round(_f(wan.get("upload")) / 1048576, 1),
        })
        if quer("miot"):
            d["conexao_rapida"] = (await a.safe("xqnetwork/get_miotrelay_switch")).get("enabled") == 1
        if quer("miscan"):
            d["varredura_aiot"] = (await a.safe("xqnetwork/get_miscan_switch")).get("enabled") == 1
        if quer("backhaul"):
            d["prioridade_muitos_aparelhos"] = str((await a.safe("xqnetwork/get_son_backhaul_mode")).get("mode")) == "1"
        if quer("guest"):
            gi = (await a.safe("misns/wifi_share_info")).get("info") or {}
            d["visitante"] = gi.get("guest") == 1
            d["visitante_ssid"] = (gi.get("data") or {}).get("ssid")
            d["_visitante_cfg"] = gi.get("data") or {}
        if quer("qos"):
            d["qos"] = ((await a.safe("misystem/qos_info")).get("status") or {}).get("on") == 1
        if quer("arn"):
            arn = await a.safe("misystem/arn_status")
            d["anti_intrusos"] = arn.get("open") == 1
            d["anti_intrusos_nivel"] = arn.get("level")
            d["intrusoes_bloqueadas"] = arn.get("count")
        if quer("sec"):
            sec = await a.safe("misystem/arn_security")
            d["firewall_sites"] = sec.get("malicious_url_firewall") == 1
            d["firewall_virus"] = sec.get("virus_file_firewall") == 1
        if quer("macfilter"):
            mf = await a.safe("xqnetwork/wifi_macfilter_info")
            d["filtro_mac"] = mf.get("enable") == 1
            d["_filtro_mac_modo"] = mf.get("model", 0)
            d["filtro_mac_lista"] = [{"nome": x.get("name"), "mac": x.get("mac")} for x in mf.get("macfilter") or []]
            d["filtro_mac_qtd"] = len(d["filtro_mac_lista"])
        if quer("vpn"):
            d["vpn_status"] = (await a.safe("xqsystem/vpn_status")).get("status")
        if quer("wps"):
            d["wps"] = (await a.safe("xqsystem/wps_status")).get("status") == 1
        if quer("topo"):
            tp = (await a.safe("misystem/topo_graph")).get("graph") or {}
            d["repetidor_na_mesh"] = len(tp.get("leafs") or []) > 0
        if quer("wan"):
            w = (await a.safe("xqnetwork/wan_info")).get("info") or {}
            lk = await a.safe("xqnetwork/wan_link")
            v4 = (w.get("ipv4") or [{}])[0]
            d.update({
                "internet": bool(v4.get("ip")) and lk.get("link") == 1,
                "wan_cabo": lk.get("link") == 1,
                "ip_publico": v4.get("ip"),
                "ipv6": ((w.get("ipv6_info") or {}).get("ip6addr") or [None])[0],
                "internet_conectada_ha": w.get("uptime"),
                "gateway_wan": w.get("gateWay"),
                "dns": ", ".join((w.get("details") or {}).get("dns") or []),
            })
        if quer("upd"):
            if time.time() - self._upd_t > FIRMWARE_INTERVALO_S:
                self._upd = await a.safe("xqsystem/check_rom_update")
                self._upd_t = time.time()
            d["firmware_atualizacao"] = self._upd.get("needUpdate") == 1
            d["firmware_nova"] = self._upd.get("version")
        if quer("macbind"):
            mb = (await a.safe("xqnetwork/macbind_info")).get("list") or []
            d["reservas"] = sorted(
                ({"nome": r.get("name"), "mac": (r.get("mac") or "").upper(), "ip": r.get("ip")} for r in mb),
                key=lambda r: [int(x) for x in str(r["ip"]).split(".") if x.isdigit()],
            )
            d["qtd_reservas"] = len(mb)
        if quer("devices"):
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

    async def async_devices(self) -> dict[str, dict[str, Any]]:
        """Lista de aparelhos sob demanda (tela de opções), mesmo com as entidades desativadas."""
        if not self.devices:
            for x in (await self.api.safe("misystem/devicelist")).get("list") or []:
                mac = (x.get("mac") or "").upper()
                ip = ((x.get("ip") or [{}])[0]) or {}
                self.devices[mac] = {"nome": x.get("name") or x.get("oname") or mac, "ip": ip.get("ip"), "isap": x.get("isap")}
        return self.devices
