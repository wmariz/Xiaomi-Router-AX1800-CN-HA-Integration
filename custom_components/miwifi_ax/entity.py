"""Entidade base: liga tudo ao dispositivo do roteador."""
from __future__ import annotations

from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, ROLE_MAIN
from .coordinator import MiWiFiCoordinator


def _url(coord: MiWiFiCoordinator) -> str:
    """Botão 'Visitar': painel local (com o roteador pré-selecionado) ou a interface do roteador."""
    p = (getattr(coord, "painel_url", "") or "").strip()
    if not p:
        return f"http://{coord.api.host}"
    return f"{p}{'&' if '?' in p else '?'}rot={coord.role}"


# Ativadas por padrão; o resto nasce DESATIVADO (ative só o que usar — a integração
# só consulta no roteador o que alguma entidade ativada precisa).
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
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, mac)},
            connections={(CONNECTION_NETWORK_MAC, mac.lower())},
            manufacturer="Xiaomi",
            model="Mi Router AX1800 (RM1800)",
            name=(coord.data or {}).get("nome") or ("Roteador principal" if coord.role == ROLE_MAIN else "Repetidor"),
            sw_version=coord.hw.get("version"),
            serial_number=coord.hw.get("sn"),
            configuration_url=_url(coord),
            suggested_area=(coord.data or {}).get("local"),
        )
