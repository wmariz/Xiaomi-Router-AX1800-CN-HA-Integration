"""Sensores."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfDataRate, UnitOfInformation, UnitOfTime

from .const import DOMAIN, ROLE_MAIN
from .entity import MiWiFiEntity

M = SensorStateClass.MEASUREMENT
DIAG = EntityCategory.DIAGNOSTIC


@dataclass(frozen=True, kw_only=True)
class Desc(SensorEntityDescription):
    so_principal: bool = False
    atributo: str | None = None  # chave de self.coordinator.data com lista para atributos


SENSORES: tuple[Desc, ...] = (
    Desc(key="ligado_ha", device_class=SensorDeviceClass.DURATION, native_unit_of_measurement=UnitOfTime.SECONDS, suggested_unit_of_measurement=UnitOfTime.HOURS, icon="mdi:timer-outline"),
    Desc(key="cpu", native_unit_of_measurement=PERCENTAGE, state_class=M, icon="mdi:cpu-64-bit"),
    Desc(key="memoria", native_unit_of_measurement=PERCENTAGE, state_class=M, icon="mdi:memory"),
    Desc(key="clientes_24", state_class=M, icon="mdi:wifi"),
    Desc(key="clientes_5", state_class=M, icon="mdi:wifi"),
    Desc(key="canal_24", icon="mdi:wifi-cog", entity_category=DIAG, so_principal=True),
    Desc(key="canal_5", icon="mdi:wifi-cog", entity_category=DIAG, so_principal=True),
    Desc(key="largura_24", icon="mdi:arrow-expand-horizontal", entity_category=DIAG, so_principal=True),
    Desc(key="largura_5", icon="mdi:arrow-expand-horizontal", entity_category=DIAG, so_principal=True),
    Desc(key="potencia_24", icon="mdi:signal", entity_category=DIAG, so_principal=True),
    Desc(key="potencia_5", icon="mdi:signal", entity_category=DIAG, so_principal=True),
    Desc(key="avisos", icon="mdi:bell-outline", entity_category=DIAG, so_principal=True),
    Desc(key="firmware", icon="mdi:package-variant", entity_category=DIAG),
    Desc(key="hora_roteador", icon="mdi:clock-outline", entity_category=DIAG, so_principal=True),
    Desc(key="relogio_diferenca", native_unit_of_measurement=UnitOfTime.SECONDS, state_class=M, icon="mdi:clock-alert-outline", entity_category=DIAG),
    Desc(key="sinal_ate_principal", native_unit_of_measurement=PERCENTAGE, state_class=M, icon="mdi:access-point-network", entity_registry_enabled_default=False),
    Desc(key="aparelhos_online", state_class=M, icon="mdi:devices", so_principal=True),
    Desc(key="aparelhos_conhecidos", icon="mdi:devices", so_principal=True, entity_category=DIAG),
    Desc(key="qtd_cabo", state_class=M, icon="mdi:ethernet", so_principal=True, atributo="cabo"),
    Desc(key="qtd_24", state_class=M, icon="mdi:wifi", so_principal=True, atributo="2,4 GHz"),
    Desc(key="qtd_5", state_class=M, icon="mdi:wifi", so_principal=True, atributo="5 GHz"),
    Desc(key="qtd_visitante", state_class=M, icon="mdi:account-group", so_principal=True, atributo="visitante"),
    Desc(key="qtd_reservas", icon="mdi:ip-network", so_principal=True, atributo="reservas"),
    Desc(key="filtro_mac_qtd", icon="mdi:filter", so_principal=True, atributo="filtro_mac_lista"),
    Desc(key="visitante_ssid", icon="mdi:account-group", so_principal=True, entity_category=DIAG),
    Desc(key="intrusoes_bloqueadas", state_class=SensorStateClass.TOTAL_INCREASING, icon="mdi:shield-alert", so_principal=True),
    Desc(key="anti_intrusos_nivel", icon="mdi:shield-account", so_principal=True, entity_category=DIAG),
    Desc(key="vpn_status", icon="mdi:vpn", so_principal=True, entity_category=DIAG),
    Desc(key="ip_publico", icon="mdi:ip", so_principal=True),
    Desc(key="ipv6", icon="mdi:ip", so_principal=True, entity_category=DIAG),
    Desc(key="gateway_wan", icon="mdi:router-network", so_principal=True, entity_category=DIAG),
    Desc(key="dns", icon="mdi:dns", so_principal=True, entity_category=DIAG),
    Desc(key="internet_conectada_ha", device_class=SensorDeviceClass.DURATION, native_unit_of_measurement=UnitOfTime.SECONDS, suggested_unit_of_measurement=UnitOfTime.HOURS, icon="mdi:web-clock", so_principal=True),
    Desc(key="download", device_class=SensorDeviceClass.DATA_RATE, native_unit_of_measurement=UnitOfDataRate.KILOBITS_PER_SECOND, state_class=M, icon="mdi:download", so_principal=True),
    Desc(key="upload", device_class=SensorDeviceClass.DATA_RATE, native_unit_of_measurement=UnitOfDataRate.KILOBITS_PER_SECOND, state_class=M, icon="mdi:upload", so_principal=True),
    Desc(key="pico_download", device_class=SensorDeviceClass.DATA_RATE, native_unit_of_measurement=UnitOfDataRate.KILOBITS_PER_SECOND, icon="mdi:download-circle", so_principal=True, entity_category=DIAG),
    Desc(key="pico_upload", device_class=SensorDeviceClass.DATA_RATE, native_unit_of_measurement=UnitOfDataRate.KILOBITS_PER_SECOND, icon="mdi:upload-circle", so_principal=True, entity_category=DIAG),
    Desc(key="total_baixado", device_class=SensorDeviceClass.DATA_SIZE, native_unit_of_measurement=UnitOfInformation.MEGABYTES, state_class=SensorStateClass.TOTAL_INCREASING, icon="mdi:download-network", so_principal=True),
    Desc(key="total_enviado", device_class=SensorDeviceClass.DATA_SIZE, native_unit_of_measurement=UnitOfInformation.MEGABYTES, state_class=SensorStateClass.TOTAL_INCREASING, icon="mdi:upload-network", so_principal=True),
)


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    ents = [Sensor(c, d) for d in SENSORES if (c.role == ROLE_MAIN or not d.so_principal) and d.key in c.data]
    async_add_entities(ents)


class Sensor(MiWiFiEntity, SensorEntity):
    entity_description: Desc

    def __init__(self, coord, desc: Desc) -> None:
        super().__init__(coord, desc.key)
        self.entity_description = desc

    @property
    def native_value(self):
        return self.coordinator.data.get(self.entity_description.key)

    @property
    def extra_state_attributes(self):
        at = self.entity_description.atributo
        if not at:
            return None
        d = self.coordinator.data
        if at in ("reservas", "filtro_mac_lista"):
            return {"lista": d.get(at, [])}
        return {"aparelhos": (d.get("grupos") or {}).get(at, [])}
