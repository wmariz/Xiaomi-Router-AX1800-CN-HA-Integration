"""Rastreamento de aparelhos escolhidos nas opções (presença na rede)."""
from __future__ import annotations

from homeassistant.components.device_tracker import ScannerEntity, SourceType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_TRACKED, DOMAIN, ROLE_MAIN


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    if c.role != ROLE_MAIN:
        return
    async_add_entities(Aparelho(c, mac) for mac in entry.options.get(CONF_TRACKED, []))


class Aparelho(CoordinatorEntity, ScannerEntity):
    def __init__(self, coord, mac: str) -> None:
        super().__init__(coord)
        self._mac = mac.upper()
        self._attr_unique_id = f"miwifi_ax_tracker_{self._mac}"
        self._attr_name = (coord.devices.get(self._mac) or {}).get("nome") or self._mac

    @property
    def _d(self):
        return self.coordinator.devices.get(self._mac) or {}

    @property
    def source_type(self):
        return SourceType.ROUTER

    @property
    def is_connected(self) -> bool:
        return bool(self._d.get("online"))

    @property
    def ip_address(self):
        return self._d.get("ip")

    @property
    def mac_address(self):
        return self._mac

    @property
    def hostname(self):
        return self._d.get("nome")

    @property
    def extra_state_attributes(self):
        d = self._d
        return {k: d.get(k) for k in ("conexao", "via_repetidor", "download", "upload", "online_ha", "internet_liberada")}
