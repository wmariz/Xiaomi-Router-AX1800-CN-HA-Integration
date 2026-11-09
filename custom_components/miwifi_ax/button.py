"""Botões."""
from __future__ import annotations

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.const import EntityCategory
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .entity import MiWiFiEntity


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([Reiniciar(c), Atualizar(c)])


class Reiniciar(MiWiFiEntity, ButtonEntity):
    _attr_device_class = ButtonDeviceClass.RESTART
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coord) -> None:
        super().__init__(coord, "reiniciar")

    async def async_press(self) -> None:
        j = await self.coordinator.api.call("xqsystem/reboot", {"client": "web"})
        if j.get("code") != 0:
            raise HomeAssistantError(translation_domain=DOMAIN, translation_key="roteador_recusou", translation_placeholders={"detalhe": str(j.get("msg") or j)})


class Atualizar(MiWiFiEntity, ButtonEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coord) -> None:
        super().__init__(coord, "atualizar_dados")

    async def async_press(self) -> None:
        await self.coordinator.async_request_refresh()
