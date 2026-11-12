"""Zigbee-aware 2.4 GHz channel search.

The router's own optimization (misystem/channel_scan_*) only returns one suggested channel and ignores
Zigbee. Here every 2.4 GHz channel (1–11) gets an interference score computed from the neighbouring
networks (xqnetwork/wifi_list), channels that overlap the Zigbee channel are excluded and the 2.4 GHz
band is kept at 20 MHz (40 MHz would cover the Zigbee channel again).

The same algorithm exists in desktop/painel.html (manual search in every panel); keep both in sync.
This module also runs the periodic search configured in the integration options (main router only).
"""
from __future__ import annotations

import asyncio
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.event import async_track_time_change
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

from .const import (
    CONF_CANAL_COMPENSA,
    CONF_CANAL_DIAS,
    CONF_CANAL_HORA,
    CONF_ZIGBEE_CANAL,
    DOMAIN,
    ROLE_NODE,
)

_LOGGER = logging.getLogger(__name__)
SINAL_CANAL = f"{DOMAIN}_canal_atualizado"
EVENTO_TROCA = f"{DOMAIN}_canal_trocado"
CANAIS = range(1, 12)          # 12/13 are not allowed in Brazil and some devices don't see them
MARGEM_ZIGBEE_MHZ = 12          # 20 MHz Wi-Fi (±10) + Zigbee (±1) + 1 MHz guard
GANHO_MINIMO = 0.30             # "only if worth it": the new channel must have 30 % less interference
CANAIS_PADRAO = (1, 6, 11)      # the non-overlapping channels most neighbours sit on
PESO_INTERMEDIARIO = 1.25       # in-between channels partially overlap two groups of neighbours: CSMA can only
                                # energy-detect them (no frame decoding / NAV), which is worse than sharing a channel


def freq_wifi(c: int) -> int:
    return 2407 + 5 * c


def freq_zigbee(z: int) -> int:
    return 2405 + 5 * (z - 11)


def bloqueado(c: int, zigbee: int | None) -> bool:
    return bool(zigbee) and abs(freq_wifi(c) - freq_zigbee(zigbee)) < MARGEM_ZIGBEE_MHZ


def notas(vizinhos: list[dict], zigbee: int | None, proprios: set[str]) -> list[dict]:
    """Interference per channel, 0–100 (100 = worst channel of this scan).

    Channels 1/6/11 count their interference as is; the in-between ones get PESO_INTERMEDIARIO (×1.25).
    1, 6 and 11 are weighted equally (decided 2026-11-11 after a day of sampling, Zigbee on 25)."""
    bruto = {}
    for c in CANAIS:
        s = 0.0
        for v in vizinhos:
            if v.get("band") != "2g" or (v.get("ssid") or "") in proprios:
                continue
            try:
                d = abs(c - int(v.get("channel")))
            except (TypeError, ValueError):
                continue
            if d < 4:  # 20 MHz channels overlap up to 3 channels apart
                s += float(v.get("signal") or 0) * (1 - d / 4)
        bruto[c] = s if c in CANAIS_PADRAO else s * PESO_INTERMEDIARIO
    mx = max(bruto.values()) or 1.0
    return [{"canal": c, "nota": round(100 * bruto[c] / mx), "bloqueado": bloqueado(c, zigbee)} for c in CANAIS]


def escolher(lista: list[dict]) -> dict | None:
    livres = [x for x in lista if not x["bloqueado"]]
    if not livres:
        return None
    # tie-break: prefer the standard non-overlapping channels 1/6/11, then the lower channel
    return min(livres, key=lambda x: (x["nota"], 0 if x["canal"] in CANAIS_PADRAO else 1, x["canal"]))


def zigbee_canal(hass: HomeAssistant) -> int | None:
    """Zigbee channel: running ZHA first, then the latest network backup in zigbee.db."""
    try:
        from homeassistant.components.zha.helpers import get_zha_data  # noqa: PLC0415

        ch = get_zha_data(hass).gateway_proxy.gateway.application_controller.state.network_info.channel
        if ch:
            return int(ch)
    except Exception:  # noqa: BLE001 - ZHA internals change between versions
        pass
    try:
        con = sqlite3.connect(f"file:{hass.config.path('zigbee.db')}?mode=ro", uri=True, timeout=5)
        try:
            tabs = [r[0] for r in con.execute("select name from sqlite_master where type='table' and name like 'network_backups_v%'")]
            for t in sorted(tabs, key=lambda n: int(n.rsplit("v", 1)[-1] or 0), reverse=True):
                r = con.execute(f"select json_extract(backup_json, '$.network_info.channel') from {t} order by rowid desc limit 1").fetchone()  # noqa: S608
                if r and r[0]:
                    return int(r[0])
        finally:
            con.close()
    except Exception:  # noqa: BLE001
        pass
    return None


def _nos(hass: HomeAssistant) -> list:
    """Every Mesh node configured in the integration (there may be more than one repeater)."""
    return [c for c in hass.data.get(DOMAIN, {}).values() if getattr(c, "role", None) == ROLE_NODE]


async def buscar(hass: HomeAssistant, coord, zigbee: int | None) -> dict[str, Any]:
    """Runs the scan on the main router and returns the full result (nothing is changed)."""
    api = coord.api
    wf = await api.call("xqnetwork/wifi_detail_all")
    info = wf.get("info") or []
    w24 = info[0] if info else {}
    proprios = {i.get("ssid") for i in info if i.get("ssid")}
    gi = ((await api.safe("misns/wifi_share_info")).get("info") or {}).get("data") or {}
    if gi.get("ssid"):
        proprios.add(gi["ssid"])
    viz = (await api.call("xqnetwork/wifi_list")).get("list") or []
    lista = notas(viz, zigbee, proprios)
    sug = escolher(lista)
    atual = int(((w24.get("channelInfo") or {}).get("channel")) or 0)
    atuais_nos = []
    for no in _nos(hass):
        try:
            wn = ((await no.api.call("xqnetwork/wifi_detail_all")).get("info") or [{}])[0]
            c_no = int(((wn.get("channelInfo") or {}).get("channel")) or 0)
            if c_no:
                atuais_nos.append(c_no)
        except Exception:  # noqa: BLE001
            pass
    atual_no = atuais_nos[0] if atuais_nos else None
    nota = {x["canal"]: x["nota"] for x in lista}
    fixo20 = str(w24.get("channel")) != "0" and str(w24.get("bandwidth")) == "20"
    motivos = []
    if atual and bloqueado(atual, zigbee):
        motivos.append("principal_no_zigbee")
    if any(bloqueado(c, zigbee) for c in atuais_nos):
        motivos.append("repetidor_no_zigbee")
    if not fixo20:
        motivos.append("nao_fixo_20mhz")
    if atual and atual not in CANAIS:
        motivos.append("canal_fora_1_11")
    ganho = bool(sug and atual in nota and sug["canal"] != atual and sug["nota"] <= (1 - GANHO_MINIMO) * nota[atual])
    if ganho:
        motivos.append("ganho")
    return {
        "quando": dt_util.utcnow().isoformat(),
        "zigbee": zigbee,
        "atual": atual or None,
        "atual_repetidor": atual_no,
        "config": {"canal": w24.get("channel"), "largura": w24.get("bandwidth"), "bsd": wf.get("bsd")},
        "canais": lista,
        "sugerido": sug["canal"] if sug else None,
        "nota_atual": nota.get(atual),
        "nota_sugerido": sug["nota"] if sug else None,
        "compensa": bool(motivos) and bool(sug),
        "motivos": motivos,
        "vizinhos": sum(1 for v in viz if v.get("band") == "2g" and (v.get("ssid") or "") not in proprios),
    }


async def aplicar(hass: HomeAssistant, coord, canal: int) -> dict[str, Any]:
    """Puts the 2.4 GHz band on `canal` at 20 MHz (main router; copied to the Mesh node)."""
    api = coord.api
    wf = await api.call("xqnetwork/wifi_detail_all")
    info = wf.get("info") or []
    a = info[0] if info else {}
    b5 = info[1] if len(info) > 1 else {}
    if str(wf.get("bsd")) == "1":
        # unified Wi-Fi: same payload as the official page (bsdWiFiSubmitHandler)
        p = {"bsd": 1, "on1": 1, "ssid1": a.get("ssid"), "encryption1": a.get("encryption"), "channel1": canal, "bandwidth1": 20,
             "hidden1": a.get("hidden"), "txpwr1": a.get("txpwr"), "pwd1": a.get("password") or "",
             "on2": 1, "ssid2": a.get("ssid"), "encryption2": a.get("encryption"), "channel2": b5.get("channel"), "bandwidth2": b5.get("bandwidth"),
             "hidden2": a.get("hidden"), "txpwr2": b5.get("txpwr"), "pwd2": a.get("password") or ""}
        r = await api.call("xqnetwork/set_all_wifi", p, post=True)
        metodo = "set_all_wifi"
    elif str(a.get("bandwidth")) == "20" and str(a.get("channel")) != "0":
        # already fixed at 20 MHz: fast switch (~5 s, Wi-Fi stays up); not mirrored → apply on the node too
        c5 = (b5.get("channelInfo") or {}).get("channel") or b5.get("channel")
        r = await api.call("misystem/set_channel", {"channel1": canal, "channel2": c5})
        if r.get("code") == 0:
            for no in _nos(hass):
                try:
                    wn = (await no.api.call("xqnetwork/wifi_detail_all")).get("info") or [{}, {}]
                    c5n = ((wn[1] if len(wn) > 1 else {}).get("channelInfo") or {}).get("channel") or c5
                    await no.api.call("misystem/set_channel", {"channel1": canal, "channel2": c5n})
                except Exception as err:  # noqa: BLE001
                    _LOGGER.warning("Channel change on Mesh node %s failed: %s", no.api.host, err)
        metodo = "set_channel"
    else:
        # full save (restarts the Wi-Fi ~30 s; the Mesh copies it to the node)
        p = {"wifiIndex": 1, "on": 1, "ssid": a.get("ssid"), "pwd": a.get("password") or "", "encryption": a.get("encryption"),
             "channel": canal, "bandwidth": 20, "hidden": a.get("hidden"), "txpwr": a.get("txpwr")}
        r = await api.call("xqnetwork/set_wifi", p, post=True)
        metodo = "set_wifi"
    return {"code": r.get("code"), "metodo": metodo}


class CanalAuto:
    """Periodic search (main router only), its options and the last result (persisted)."""

    def __init__(self, hass: HomeAssistant, entry, coord) -> None:
        self.hass, self.entry, self.coord = hass, entry, coord
        self._store: Store = Store(hass, 1, f"{DOMAIN}_canal_{entry.entry_id}")
        self.ultimo: dict[str, Any] | None = None
        self._lock = asyncio.Lock()
        self._unsub = None

    @property
    def dias(self) -> int:
        return int(self.entry.options.get(CONF_CANAL_DIAS, 0) or 0)

    @property
    def hora(self) -> int:
        return int(self.entry.options.get(CONF_CANAL_HORA, 4) or 0)

    @property
    def compensa(self) -> bool:
        return bool(self.entry.options.get(CONF_CANAL_COMPENSA, True))

    async def zigbee(self) -> int | None:
        manual = int(self.entry.options.get(CONF_ZIGBEE_CANAL, 0) or 0)
        if manual:
            return manual
        return await self.hass.async_add_executor_job(zigbee_canal, self.hass)

    async def async_start(self) -> None:
        self.ultimo = await self._store.async_load()
        if self.dias:
            self._unsub = async_track_time_change(self.hass, self._tick, hour=self.hora, minute=0, second=0)

    @callback
    def async_stop(self) -> None:
        if self._unsub:
            self._unsub()
            self._unsub = None

    async def _tick(self, now: datetime) -> None:
        ult = (self.ultimo or {}).get("quando_auto")
        if ult:
            try:
                if dt_util.utcnow() - datetime.fromisoformat(ult) < timedelta(days=self.dias) - timedelta(hours=2):
                    return
            except ValueError:
                pass
        await self.executar(automatico=True)

    async def executar(self, automatico: bool) -> dict[str, Any]:
        async with self._lock:
            res = await buscar(self.hass, self.coord, await self.zigbee())
            res["automatico"] = automatico
            res["aplicado"] = None
            troca = res["sugerido"] and (res["compensa"] if self.compensa else (res["sugerido"] != res["atual"] or bool(res["motivos"])))
            if automatico and troca:
                antes = res["atual"]
                r = await aplicar(self.hass, self.coord, res["sugerido"])
                res["aplicado"] = {"de": antes, "para": res["sugerido"], **r}
                if r.get("code") == 0:
                    self.hass.bus.async_fire(EVENTO_TROCA, {"de": antes, "para": res["sugerido"], "zigbee": res["zigbee"],
                                                           "nota_antes": res["nota_atual"], "nota_depois": res["nota_sugerido"],
                                                           "motivos": res["motivos"], "metodo": r.get("metodo")})
                    self._notificar(res)
            if automatico:
                res["quando_auto"] = res["quando"]
            elif self.ultimo and self.ultimo.get("quando_auto"):
                res["quando_auto"] = self.ultimo["quando_auto"]
            self.ultimo = res
            await self._store.async_save(res)
            async_dispatcher_send(self.hass, SINAL_CANAL, self.entry.entry_id)
            return res

    def _notificar(self, res: dict[str, Any]) -> None:
        pt = (self.hass.config.language or "").lower().startswith("pt")
        a = res["aplicado"]
        if pt:
            titulo = "Canal do Wi-Fi trocado"
            msg = (f"A busca automática mudou o 2,4 GHz do canal {a['de']} para o {a['para']} (20 MHz), evitando o Zigbee "
                   f"no canal {res['zigbee']}. Interferência: {res['nota_atual']} → {res['nota_sugerido']}.")
        else:
            titulo = "Wi-Fi channel changed"
            msg = (f"The automatic search moved 2.4 GHz from channel {a['de']} to {a['para']} (20 MHz), avoiding Zigbee "
                   f"on channel {res['zigbee']}. Interference: {res['nota_atual']} → {res['nota_sugerido']}.")
        self.hass.async_create_task(self.hass.services.async_call(
            "persistent_notification", "create", {"title": titulo, "message": msg, "notification_id": f"{DOMAIN}_canal"}))
