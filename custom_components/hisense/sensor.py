from datetime import datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy, UnitOfTime
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .entity import HisenseEntity

AC_ENERGY_SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="today_energy",
        translation_key="today_energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        icon="mdi:flash",
    ),
    SensorEntityDescription(
        key="run_time",
        translation_key="run_time",
        native_unit_of_measurement=UnitOfTime.HOURS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL,
        icon="mdi:timer-outline",
    ),
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinators = hass.data[DOMAIN][config_entry.entry_id]
    ac_coordinators = [c for c in coordinators.values() if c.device_type == "空调"]

    sensors = [
        HisenseACEnergySensor(coordinator, desc)
        for coordinator in ac_coordinators
        for desc in AC_ENERGY_SENSOR_DESCRIPTIONS
    ]
    async_add_entities(sensors)


class HisenseACEnergySensor(HisenseEntity, SensorEntity):
    entity_description: SensorEntityDescription

    def __init__(self, coordinator, description: SensorEntityDescription):
        super().__init__(
            coordinator,
            description.key,
            description.key,
            description.icon,
        )
        self.entity_description = description

    @property
    def available(self) -> bool:
        return self.status.get(self.entity_description.key) is not None

    @property
    def native_value(self):
        return self.status.get(self.entity_description.key)

    @property
    def last_reset(self) -> datetime:
        """The App values are cumulative for the current local calendar day."""
        return dt_util.start_of_local_day()
