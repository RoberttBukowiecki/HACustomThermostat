from homeassistant import config_entries
from .config_flow import CustomThermostatConfigFlow

async def async_setup(hass, config):
    """Set up the custom thermostat integration."""
    hass.config_entries.async_register(
        "climate_module", CustomThermostatConfigFlow
    )
    return True