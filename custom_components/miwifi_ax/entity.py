"""Base entity: attaches everything to the router device."""
from __future__ import annotations

from homeassistant.helpers import area_registry as ar
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, ROLE_MAIN
from .coordinator import MiWiFiCoordinator


def _url(coord: MiWiFiCoordinator) -> str:
    """'Visit' button: local panel (with the router preselected) or the router's own interface."""
    p = (getattr(coord, "painel_url", "") or "").strip()
    if not p:
        return f"http://{coord.api.host}"
    # identifies the router by IP (stable even with several repeaters)
    return f"{p}{'&' if '?' in p else '?'}rot={coord.api.host}"


def _area(coord: MiWiFiCoordinator) -> str | None:
    """Router 'location' (Xiaomi app: "Office", "Living room"…) as the suggested area, but only when an area with
    that name already exists — otherwise HA would create a new, usually English-named area on its own."""
    local = ((coord.data or {}).get("local") or "").strip()
    if local and ar.async_get(coord.hass).async_get_area_by_name(local):
        return local
    return None


# Enabled by default; everything else starts DISABLED (enable only what you use — the integration
# only queries what some enabled entity needs).
VISIVEIS = {"internet", "reiniciar"}


class MiWiFiEntity(CoordinatorEntity[MiWiFiCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coord: MiWiFiCoordinator, key: str) -> None:
        super().__init__(coord)
        mac = (coord.hw.get("mac") or coord.api.host).upper()
        self._key = key
        self._attr_entity_registry_enabled_default = key in VISIVEIS
        self._attr_unique_id = f"{mac}_{key}"
        self._attr_translation_key = key
        nome = (coord.data or {}).get("nome")
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, mac)},
            connections={(CONNECTION_NETWORK_MAC, mac.lower())},
            manufacturer="Xiaomi",
            model="Mi Router AX1800 (RM1800)",
            name=nome or None,
            translation_key=None if nome else ("principal" if coord.role == ROLE_MAIN else "repetidor"),
            sw_version=coord.hw.get("version"),
            serial_number=coord.hw.get("sn"),
            configuration_url=_url(coord),
            suggested_area=_area(coord),
        )
