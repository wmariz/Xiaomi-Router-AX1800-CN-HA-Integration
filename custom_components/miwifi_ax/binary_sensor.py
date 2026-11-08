"""Sensores binários."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity, BinarySensorEntityDescription
from homeassistant.const import EntityCategory

from .const import DOMAIN, ROLE_MAIN
from .entity import MiWiFiEntity

DIAG = EntityCategory.DIAGNOSTIC


@dataclass(frozen=True, kw_only=True)
class Desc(BinarySensorEntityDescription):
    so_principal: bool = False


BINARIOS: tuple[Desc, ...] = (
    Desc(key="internet", device_class=BinarySensorDeviceClass.CONNECTIVITY, so_principal=True),
    Desc(key="wan_cabo", device_class=BinarySensorDeviceClass.PLUG, so_principal=True),
    Desc(key="repetidor_na_mesh", device_class=BinarySensorDeviceClass.CONNECTIVITY, so_principal=True),
    Desc(key="firmware_atualizacao", device_class=BinarySensorDeviceClass.UPDATE, so_principal=True),
    Desc(key="wifi_24", icon="mdi:wifi", entity_category=DIAG),
    Desc(key="wifi_5", icon="mdi:wifi", entity_category=DIAG),
    Desc(key="wifi_unificado", icon="mdi:wifi-sync", so_principal=True, entity_category=DIAG),
    Desc(key="anti_intrusos", icon="mdi:shield-check", so_principal=True),
    Desc(key="firewall_sites", icon="mdi:web-cancel", so_principal=True, entity_category=DIAG),
    Desc(key="firewall_virus", icon="mdi:virus-off", so_principal=True, entity_category=DIAG),
    Desc(key="wps", icon="mdi:wifi-lock-open", so_principal=True, entity_category=DIAG),
)


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(Bin(c, d) for d in BINARIOS if (c.role == ROLE_MAIN or not d.so_principal) and d.key in c.data)


class Bin(MiWiFiEntity, BinarySensorEntity):
    entity_description: Desc

    def __init__(self, coord, desc: Desc) -> None:
        super().__init__(coord, desc.key)
        self.entity_description = desc

    @property
    def is_on(self):
        return bool(self.coordinator.data.get(self.entity_description.key))

    @property
    def extra_state_attributes(self):
        if self.entity_description.key == "firmware_atualizacao" and self.coordinator.data.get("firmware_nova"):
            return {"versao_nova": self.coordinator.data["firmware_nova"]}
        return None
