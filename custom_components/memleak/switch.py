"""Platform for light integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (ATTR_BRIGHTNESS, PLATFORM_SCHEMA,
                                            LightEntity, ColorMode)
from homeassistant.components.memleak import Burak
from homeassistant.components.memleak.const import DOMAIN
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
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

    # Setup connection with devices/cloud
    burak = config.runtime_data


    # Add devices
    async_add_entities([BurakSwitch(burak, "power"), BurakSwitch(burak, "pump")])


class BurakSwitch(SwitchEntity):
    def __init__(self, burak: Burak, channel: str) -> None:
        """Initialize an AwesomeLight."""
        self._burak = burak
        self._channel = channel

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
    def unique_id(self) -> str | None:
        return f"switch.{self._burak.slave}_{self._channel}"

    @property
    def name(self) -> str:
        """Return the display name of this switch."""
        return self._channel.capitalize()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the device on."""
        _LOGGER.debug("Switch: %s status: %s, turning on", self._channel, self._attr_is_on)
        await self._burak.set_output(self._channel, True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the device off."""
        _LOGGER.debug(
            "Switch name: %s status: %s, turning off", self._channel, self._attr_is_on
        )
        await self._burak.set_output(self._channel, False)

    async def async_update(self) -> None:
        self._attr_is_on = await self._burak.get_output(self._channel)
