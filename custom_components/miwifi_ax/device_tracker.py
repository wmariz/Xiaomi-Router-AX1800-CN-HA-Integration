"""Rastreamento de aparelhos escolhidos nas opções (presença na rede)."""
from __future__ import annotations

from homeassistant.components.device_tracker import ScannerEntity, SourceType
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_TRACKED, DOMAIN, ROLE_MAIN


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    if c.role != ROLE_MAIN:
        return
    devs = await c.async_devices()
    async_add_entities(Aparelho(c, mac, (devs.get(mac.upper()) or {}).get("nome")) for mac in entry.options.get(CONF_TRACKED, []))


class Aparelho(CoordinatorEntity, ScannerEntity):
    # O HA (2026.x) cria rastreadores de roteador desativados por padrão; aqui o
    # aparelho foi escolhido de propósito nas opções, então já nasce ativo.
    _attr_entity_registry_enabled_default = True
    _attr_source_type = SourceType.ROUTER

    def __init__(self, coord, mac: str, nome: str | None) -> None:
        super().__init__(coord)
        self._mac = mac.upper()
        # unique_id = MAC (definido pelo ScannerEntity do HA)
        self._attr_mac_address = self._mac.lower()
        self._attr_name = None  # usa o nome do dispositivo
        # Dispositivo do aparelho rastreado (exigido pelo HA a partir de 2027.11);
        # se já existir um dispositivo com esse MAC (ex.: HASS.Agent), o rastreador se junta a ele.
        self._attr_device_info = DeviceInfo(connections={(CONNECTION_NETWORK_MAC, self._mac.lower())}, name=nome or self._mac)

    @property
    def _d(self):
        return self.coordinator.devices.get(self._mac) or {}

    @property
    def is_connected(self) -> bool:
        return bool(self._d.get("online"))

    @property
    def ip_address(self):
        return self._d.get("ip")

    @property
    def hostname(self):
        return self._d.get("nome")

    @property
    def extra_state_attributes(self):
        d = self._d
        return {k: d.get(k) for k in ("conexao", "via_repetidor", "download", "upload", "online_ha", "internet_liberada")}
