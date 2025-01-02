from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_HEAT,
    HVAC_MODE_COOL,
    HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.const import TEMP_CELSIUS
import logging

_LOGGER = logging.getLogger(__name__)

class CustomThermostat(ClimateEntity):
    """Representation of a custom thermostat."""

    def __init__(self, hass, config):
        """Initialize the thermostat."""
        self.hass = hass
        self._name = config.get("name")
        self._day_temp_entity = config.get("day_temp_entity", "sensor.default_day_temp")
        self._night_temp_entity = config.get("night_temp_entity", "sensor.default_night_temp")
        self._away_temp_entity = config.get("away_temp_entity", "sensor.default_away_temp")
        self._is_night_entity = config.get("is_night_entity", "binary_sensor.is_night")
        self._heaters = config.get("heaters", ["climate.default_heater"])
        self._coolers = config.get("coolers", ["climate.default_cooler"])
        self._current_temperature = None
        self._target_temperature = None
        self._hvac_mode = HVAC_MODE_OFF

    @property
    def name(self):
        """Return the name of the thermostat."""
        return self._name

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def hvac_modes(self):
        """Return the list of available HVAC modes."""
        return [HVAC_MODE_HEAT, HVAC_MODE_COOL, HVAC_MODE_OFF]

    @property
    def hvac_mode(self):
        """Return the current HVAC mode."""
        return self._hvac_mode

    def set_hvac_mode(self, hvac_mode):
        """Set a new HVAC mode."""
        self._hvac_mode = hvac_mode
        self.schedule_update_ha_state()

    @property
    def target_temperature(self):
        """Return the target temperature."""
        return self._target_temperature

    def set_temperature(self, **kwargs):
        """Set a new target temperature."""
        self._target_temperature = kwargs.get("temperature")
        self.schedule_update_ha_state()

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._current_temperature

    def update(self):
        """Fetch new state data for the thermostat."""
        # Check if night mode should be active
        if self._is_night_entity:
            is_night = self.hass.states.get(self._is_night_entity).state
            if is_night == "on":
                _LOGGER.info(f"{self._name}: Night mode activated.")
                self._target_temperature = float(self.hass.states.get(self._night_temp_entity).state)

        # Determine the target temperature based on the mode
        mode = self.hass.states.get(self._current_mode_entity).state
        if mode == "day":
            self._target_temperature = float(self.hass.states.get(self._day_temp_entity).state)
        elif mode == "night":
            self._target_temperature = float(self.hass.states.get(self._night_temp_entity).state)
        elif mode == "away":
            self._target_temperature = float(self.hass.states.get(self._away_temp_entity).state)

        # Update current temperature based on temperature sensors
        current_temps = [
            float(self.hass.states.get(sensor).state)
            for sensor in self._temperature_sensors
            if self.hass.states.get(sensor) is not None
        ]
        self._current_temperature = sum(current_temps) / len(current_temps) if current_temps else None

        # Control heating and cooling devices
        self._control_heating_cooling()

    def _control_heating_cooling(self):
        """Control heaters and coolers based on the target and current temperatures."""
        if self._hvac_mode == HVAC_MODE_HEAT and self._current_temperature < self._target_temperature:
            for heater in self._heaters:
                self.hass.services.call("homeassistant", "turn_on", {"entity_id": heater})
        elif self._hvac_mode == HVAC_MODE_COOL and self._current_temperature > self._target_temperature:
            for cooler in self._coolers:
                self.hass.services.call("homeassistant", "turn_on", {"entity_id": cooler})
        else:
            for device in self._heaters + self._coolers:
                self.hass.services.call("homeassistant", "turn_off", {"entity_id": device})
