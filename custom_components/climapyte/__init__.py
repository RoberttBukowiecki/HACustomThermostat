import logging
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
import voluptuous as vol
from homeassistant.const import CONF_NAME

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration through the UI."""
    _LOGGER.info("Setting up custom climate integration.")
    return True

class ClimateConfigFlow(config_entries.ConfigFlow, domain="custom_thermostat"):
    """Handle a config flow for the custom climate integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the user input for configuring the integration."""
        if user_input is not None:
            # Save the configuration to a new entry
            self.hass.config_entries.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input
            )
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        # Show a form for the user to input their configuration
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME): str,
                vol.Required("day_temp_entity"): str,
                vol.Required("night_temp_entity"): str,
                vol.Required("away_temp_entity"): str,
                vol.Required("current_mode_entity"): str,
            })
        )
