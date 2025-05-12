"""Platform for light integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (ATTR_BRIGHTNESS, PLATFORM_SCHEMA,
                                            LightEntity, ColorMode)
from . import Burak
from .const import DOMAIN
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ID, CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback, AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:


    burak = config.runtime_data

    # Add devices
    channels = await burak.channels()
    async_add_entities(BurakLight(burak, channel) for channel in channels)

class BurakLight(LightEntity):
    """Representation of an Awesome Light."""

    def __init__(self, burak: Burak, channel: str) -> None:
        """Initialize an AwesomeLight."""
        # self.entity_id = f"light.burak_led_{channel}"
        self._burak = burak
        self._channel = channel
        self._name = f"LED {channel}"
        self._state = None
        self._brightness = None

    @property
    def unique_id(self) -> str | None:
        return f"light.{self._burak.slave}_led_{self._channel}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._burak.slave)
            },
            name=f"Burak {self._burak.slave}",
            manufacturer="memleak",
            model="burak-v1",
        )

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    @property
    def color_mode(self) -> ColorMode | str | None:
        return ColorMode.BRIGHTNESS

    @property
    def supported_color_modes(self) -> set[ColorMode] | None:
        return {ColorMode.BRIGHTNESS}

    async def async_turn_on(self, **kwargs: Any) -> None:
        brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
        await self._burak.set_brightness(self._channel, brightness)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        await self._burak.set_brightness(self._channel, 0)

    async def async_update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        brightness = await self._burak.get_brightness(self._channel)
        self._state = brightness != 0
        if brightness != 0:
            self._brightness = brightness
