from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME, CONF_HOST
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

class CustomThermostatConfigFlow(config_entries.ConfigFlow, domain="custom_thermostat"):
    """Handle a config flow for CustomThermostat."""

    def __init__(self):
        """Initialize the flow."""
        self._host = None
        self._name = None
        self._day_temp_entity = None
        self._night_temp_entity = None
        self._away_temp_entity = None
        self._current_mode_entity = None
        self._temperature_offset = 0
        self._heaters = []
        self._coolers = []

    async def async_step_user(self, user_input=None):
        """Handle the user input step."""
        if user_input is not None:
            self._name = user_input[CONF_NAME]
            self._host = user_input[CONF_HOST]
            self._day_temp_entity = user_input.get("day_temp_entity")
            self._night_temp_entity = user_input.get("night_temp_entity")
            self._away_temp_entity = user_input.get("away_temp_entity")
            self._current_mode_entity = user_input.get("current_mode_entity")
            self._temperature_offset = user_input.get("temperature_offset", 0)
            self._heaters = user_input.get("heaters", [])
            self._coolers = user_input.get("coolers", [])

            # Create the entry
            return self.async_create_entry(
                title=self._name,
                data={
                    CONF_HOST: self._host,
                    CONF_NAME: self._name,
                    "day_temp_entity": self._day_temp_entity,
                    "night_temp_entity": self._night_temp_entity,
                    "away_temp_entity": self._away_temp_entity,
                    "current_mode_entity": self._current_mode_entity,
                    "temperature_offset": self._temperature_offset,
                    "heaters": self._heaters,
                    "coolers": self._coolers,
                }
            )
        return self.async_show_form(step_id="user", data_schema=self._get_data_schema())

    def _get_data_schema(self):
        """Return the schema for the configuration form."""
        return vol.Schema(
            {
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_HOST): cv.string,
                vol.Optional("day_temp_entity"): cv.entity_id,  # Temperature entity for day
                vol.Optional("night_temp_entity"): cv.entity_id,  # Temperature entity for night
                vol.Optional("away_temp_entity"): cv.entity_id,  # Temperature entity for away
                vol.Optional("current_mode_entity"): cv.entity_id,  # Boolean input for current mode
                vol.Optional("temperature_offset", default=0): vol.Coerce(float),  # Offset for temperature
                vol.Optional("heaters", default=[]): vol.All(cv.ensure_list, [cv.entity_id]),  # List of heater entities
                vol.Optional("coolers", default=[]): vol.All(cv.ensure_list, [cv.entity_id]),  # List of cooler entities
            }
        )

    async def async_step_zeroconf(self, discovery_info):
        """Handle zeroconf discovery."""
        return await self.async_step_user()
