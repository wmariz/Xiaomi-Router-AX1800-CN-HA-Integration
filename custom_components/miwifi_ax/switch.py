"""Interruptores (LED, QoS, rede de visitante e chaves de Wi-Fi)."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, ROLE_MAIN
from .entity import MiWiFiEntity

CFG = EntityCategory.CONFIG


@dataclass(frozen=True, kw_only=True)
class Desc(SwitchEntityDescription):
    ep: str
    params: Callable[[bool, dict], dict]
    post: bool = False
    so_principal: bool = True


def _visitante(on: bool, d: dict) -> dict:
    """Rede de visitante: xqnetwork/set_wifi_without_restart com wifiIndex=3 e só "on" —
    mantém nome/senha e não reinicia o Wi-Fi. (set_wifi wifiIndex=3 e o on3 do
    set_all_wifi são aceitos mas ignorados; mandar ssid/pwd juntos dá código 1615.)"""
    return {"wifiIndex": 3, "on": int(on)}


CHAVES: tuple[Desc, ...] = (
    Desc(key="led", ep="misystem/led", params=lambda on, d: {"on": int(on)}, so_principal=False),
    Desc(key="qos", ep="misystem/qos_switch", params=lambda on, d: {"on": int(on)}),
    Desc(key="visitante", ep="xqnetwork/set_wifi_without_restart", params=_visitante),
    Desc(key="mu_mimo", ep="xqnetwork/set_wifi_txbf", params=lambda on, d: {"txbf": int(on)}, post=True, entity_category=CFG),
    Desc(key="modo_wifi5", ep="xqnetwork/set_wifi_ax", params=lambda on, d: {"ax": 0 if on else 1}, post=True, entity_category=CFG),
    Desc(key="conexao_rapida", ep="xqnetwork/miotrelay_switch", params=lambda on, d: {"on": int(on)}, post=True, entity_category=CFG),
    Desc(key="varredura_aiot", ep="xqnetwork/miscan_switch", params=lambda on, d: {"on": int(on)}, post=True, entity_category=CFG),
    Desc(key="prioridade_muitos_aparelhos", ep="xqnetwork/set_son_backhaul_mode", params=lambda on, d: {"mode": int(on)}, post=True, entity_category=CFG),
    Desc(key="filtro_mac", ep="xqnetwork/set_wifi_macfilter", params=lambda on, d: {"model": d.get("_filtro_mac_modo", 0), "enable": int(on)}, entity_category=CFG),
)


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(Chave(c, d) for d in CHAVES if (c.role == ROLE_MAIN or not d.so_principal) and d.key in c.data)


class Chave(MiWiFiEntity, SwitchEntity):
    entity_description: Desc

    def __init__(self, coord, desc: Desc) -> None:
        super().__init__(coord, "sw_" + desc.key)
        self._attr_translation_key = desc.key
        self.entity_description = desc

    @property
    def is_on(self):
        return bool(self.coordinator.data.get(self.entity_description.key))

    async def _set(self, on: bool) -> None:
        d = self.entity_description
        params = d.params(on, self.coordinator.data)
        j = await self.coordinator.api.call(d.ep, params, post=d.post)
        if j.get("code") != 0:
            raise HomeAssistantError(translation_domain=DOMAIN, translation_key="roteador_recusou", translation_placeholders={"detalhe": str(j.get("msg") or j)})
        self.coordinator.data[d.key] = on
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self._set(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self._set(False)
