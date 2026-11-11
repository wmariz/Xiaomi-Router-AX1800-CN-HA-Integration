"""Sensores."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfDataRate, UnitOfInformation, UnitOfTime

from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.util import dt as dt_util

from .canal import SINAL_CANAL
from .const import DOMAIN, ROLE_MAIN
from .entity import MiWiFiEntity

M = SensorStateClass.MEASUREMENT
DIAG = EntityCategory.DIAGNOSTIC


@dataclass(frozen=True, kw_only=True)
class Desc(SensorEntityDescription):
    so_principal: bool = False
    atributo: str | None = None  # key in self.coordinator.data holding a list for the attributes


SENSORES: tuple[Desc, ...] = (
    Desc(key="ligado_ha", device_class=SensorDeviceClass.DURATION, native_unit_of_measurement=UnitOfTime.SECONDS, suggested_unit_of_measurement=UnitOfTime.HOURS),
    Desc(key="memoria", native_unit_of_measurement=PERCENTAGE, state_class=M),
    Desc(key="clientes_24", state_class=M),
    Desc(key="clientes_5", state_class=M),
    Desc(key="canal_24", entity_category=DIAG, so_principal=True),
    Desc(key="canal_5", entity_category=DIAG, so_principal=True),
    Desc(key="largura_24", entity_category=DIAG, so_principal=True),
    Desc(key="largura_5", entity_category=DIAG, so_principal=True),
    Desc(key="potencia_24", entity_category=DIAG, so_principal=True),
    Desc(key="potencia_5", entity_category=DIAG, so_principal=True),
    Desc(key="avisos", entity_category=DIAG, so_principal=True),
    Desc(key="firmware", entity_category=DIAG),
    Desc(key="hora_roteador", entity_category=DIAG, so_principal=True),
    Desc(key="relogio_diferenca", native_unit_of_measurement=UnitOfTime.SECONDS, state_class=M, entity_category=DIAG),
    Desc(key="sinal_ate_principal", native_unit_of_measurement=PERCENTAGE, state_class=M, entity_registry_enabled_default=False),
    Desc(key="aparelhos_online", state_class=M, so_principal=True),
    Desc(key="aparelhos_conhecidos", so_principal=True, entity_category=DIAG),
    Desc(key="qtd_cabo", state_class=M, so_principal=True, atributo="cabo"),
    Desc(key="qtd_24", state_class=M, so_principal=True, atributo="2,4 GHz"),
    Desc(key="qtd_5", state_class=M, so_principal=True, atributo="5 GHz"),
    Desc(key="qtd_visitante", state_class=M, so_principal=True, atributo="visitante"),
    Desc(key="qtd_reservas", so_principal=True, atributo="reservas"),
    Desc(key="upnp_mapeamentos", state_class=M, so_principal=True, atributo="upnp_lista"),
    Desc(key="redirecionamentos", so_principal=True, atributo="redirecionamentos_lista"),
    Desc(key="filtro_mac_qtd", so_principal=True, atributo="filtro_mac_lista"),
    Desc(key="visitante_ssid", so_principal=True, entity_category=DIAG),
    Desc(key="intrusoes_bloqueadas", state_class=SensorStateClass.TOTAL_INCREASING, so_principal=True),
    Desc(key="anti_intrusos_nivel", so_principal=True, entity_category=DIAG),
    Desc(key="vpn_status", so_principal=True, entity_category=DIAG),
    Desc(key="ip_publico", so_principal=True),
    Desc(key="ipv6", so_principal=True, entity_category=DIAG),
    Desc(key="gateway_wan", so_principal=True, entity_category=DIAG),
    Desc(key="dns", so_principal=True, entity_category=DIAG),
    Desc(key="internet_conectada_ha", device_class=SensorDeviceClass.DURATION, native_unit_of_measurement=UnitOfTime.SECONDS, suggested_unit_of_measurement=UnitOfTime.HOURS, so_principal=True),
    Desc(key="download", device_class=SensorDeviceClass.DATA_RATE, native_unit_of_measurement=UnitOfDataRate.KIBIBYTES_PER_SECOND, state_class=M, so_principal=True),
    Desc(key="upload", device_class=SensorDeviceClass.DATA_RATE, native_unit_of_measurement=UnitOfDataRate.KIBIBYTES_PER_SECOND, state_class=M, so_principal=True),
    Desc(key="pico_download", device_class=SensorDeviceClass.DATA_RATE, native_unit_of_measurement=UnitOfDataRate.KIBIBYTES_PER_SECOND, so_principal=True, entity_category=DIAG),
    Desc(key="pico_upload", device_class=SensorDeviceClass.DATA_RATE, native_unit_of_measurement=UnitOfDataRate.KIBIBYTES_PER_SECOND, so_principal=True, entity_category=DIAG),
    Desc(key="total_baixado", device_class=SensorDeviceClass.DATA_SIZE, native_unit_of_measurement=UnitOfInformation.MEGABYTES, state_class=SensorStateClass.TOTAL_INCREASING, so_principal=True),
    Desc(key="total_enviado", device_class=SensorDeviceClass.DATA_SIZE, native_unit_of_measurement=UnitOfInformation.MEGABYTES, state_class=SensorStateClass.TOTAL_INCREASING, so_principal=True),
)


async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    ents = [Sensor(c, d) for d in SENSORES if (c.role == ROLE_MAIN or not d.so_principal) and d.key in c.data]
    if c.role == ROLE_MAIN and getattr(c, "canal_auto", None):
        ents.append(CanalSensor(c))
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
        if at in ("reservas", "filtro_mac_lista", "upnp_lista", "redirecionamentos_lista"):
            return {"lista": d.get(at, [])}
        return {"aparelhos": (d.get("grupos") or {}).get(at, [])}


class CanalSensor(MiWiFiEntity, SensorEntity):
    """Last Zigbee-aware channel search (manual or periodic); details in the attributes."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, coord) -> None:
        super().__init__(coord, "ultima_busca_canal")
        self._attr_entity_registry_enabled_default = True

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()

        @callback
        def _atualizar(entry_id: str) -> None:
            if entry_id == self.coordinator.entry_id:
                self.async_write_ha_state()

        self.async_on_remove(async_dispatcher_connect(self.hass, SINAL_CANAL, _atualizar))

    @property
    def native_value(self):
        u = self.coordinator.canal_auto.ultimo or {}
        return dt_util.parse_datetime(u["quando"]) if u.get("quando") else None

    @property
    def extra_state_attributes(self):
        ca = self.coordinator.canal_auto
        u = ca.ultimo or {}
        return {
            "zigbee": u.get("zigbee"),
            "canal_atual": u.get("atual"),
            "canal_repetidor": u.get("atual_repetidor"),
            "canal_sugerido": u.get("sugerido"),
            "interferencia_atual": u.get("nota_atual"),
            "interferencia_sugerido": u.get("nota_sugerido"),
            "compensa": u.get("compensa"),
            "motivos": u.get("motivos"),
            "aplicado": u.get("aplicado"),
            "automatico": u.get("automatico"),
            "ultima_automatica": u.get("quando_auto"),
            "repetir_dias": ca.dias,
            "hora": ca.hora,
            "so_se_compensar": ca.compensa,
            "canais": u.get("canais"),
        }
