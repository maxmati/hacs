"""The Burak plan monitoring integration."""

from __future__ import annotations

from .burak import Burak
from .const import SLAVE

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_ID, CONF_HOST, CONF_PASSWORD, CONF_USERNAME

from homeassistant.core import HomeAssistant

# For your initial PR, limit it to 1 platform.
_PLATFORMS: list[Platform] = [Platform.LIGHT, Platform.SWITCH]

type BurakConfigEntry = ConfigEntry[Burak]


# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: BurakConfigEntry) -> bool:
    """Set up Burak plan monitoring from a config entry."""

    host = entry.data.get(CONF_HOST)
    slave_id = entry.data.get(CONF_ID)
    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)

    burak = Burak(host, slave_id, username, password)

    entry.runtime_data = burak

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: BurakConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)
