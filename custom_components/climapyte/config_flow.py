from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME, CONF_HOST

class CustomThermostatConfigFlow(config_entries.ConfigFlow, domain="climate_module"):
    """Handle a config flow for CustomThermostat."""

    def __init__(self):
        """Initialize the flow."""
        self._host = None
        self._name = None

    async def async_step_user(self, user_input=None):
        """Handle the user input step."""
        if user_input is not None:
            self._name = user_input[CONF_NAME]
            self._host = user_input[CONF_HOST]
            # Create the entry
            return self.async_create_entry(
                title=self._name, data={CONF_HOST: self._host, CONF_NAME: self._name}
            )

        # Show the form to the user
        return self.async_show_form(
            step_id="user", data_schema=self._get_data_schema()
        )

    def _get_data_schema(self):
        """Return the schema for the configuration form."""
        import voluptuous as vol
        from homeassistant.helpers import config_validation as cv

        return vol.Schema(
            {
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_HOST): cv.string,
            }
        )
