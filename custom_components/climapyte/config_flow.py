from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME, CONF_HOST
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

class CustomThermostatConfigFlow(config_entries.ConfigFlow, domain="climate_module"):
    """Handle a config flow for CustomThermostat."""

    def __init__(self):
        """Initialize the flow."""
        self._host = None
        self._name = None
        self._day_temp_entity = None
        self._night_temp_entity = None
        self._away_temp_entity = None
        self._is_night_entity = None
        self._heaters = []
        self._coolers = []

    async def async_step_user(self, user_input=None):
        """Handle the user input step."""
        if user_input is not None:
            self._name = user_input[CONF_NAME]
            self._host = user_input[CONF_HOST]

            # Provide defaults if not supplied by user
            self._day_temp_entity = user_input.get("day_temp_entity", "sensor.default_day_temp")
            self._night_temp_entity = user_input.get("night_temp_entity", "sensor.default_night_temp")
            self._away_temp_entity = user_input.get("away_temp_entity", "sensor.default_away_temp")
            self._is_night_entity = user_input.get("is_night_entity", "binary_sensor.is_night")
            self._heaters = user_input["heaters"]  # This is now a required field
            self._coolers = user_input.get("coolers", ["climate.default_cooler"])

            # Create the entry with all the configurations
            return self.async_create_entry(
                title=self._name,
                data={
                    CONF_HOST: self._host,
                    CONF_NAME: self._name,
                    "day_temp_entity": self._day_temp_entity,
                    "night_temp_entity": self._night_temp_entity,
                    "away_temp_entity": self._away_temp_entity,
                    "is_night_entity": self._is_night_entity,
                    "heaters": self._heaters,
                    "coolers": self._coolers,
                }
            )

        # Show the form to the user for each step of the configuration
        return self.async_show_form(
            step_id="user", data_schema=self._get_data_schema()
        )

    def _get_data_schema(self):
        """Return the schema for the configuration form."""
        return vol.Schema(
            {
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_HOST): cv.string,
                vol.Optional("day_temp_entity", default="sensor.default_day_temp"): cv.entity_id,
                vol.Optional("night_temp_entity", default="sensor.default_night_temp"): cv.entity_id,
                vol.Optional("away_temp_entity", default="sensor.default_away_temp"): cv.entity_id,
                vol.Optional("is_night_entity", default="binary_sensor.is_night"): cv.entity_id,
                vol.Required("heaters"): cv.entity_ids,  # Heaters are now required
                vol.Optional("coolers", default=["climate.default_cooler"]): cv.entity_ids,
            }
        )
