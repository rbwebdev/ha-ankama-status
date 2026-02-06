"""Sensor platform for Ankama Status."""
import logging
from datetime import timedelta
from typing import Any

import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, ANKAMA_API_URL, STATUS_ONLINE, STATUS_MAINTENANCE

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ankama Status sensors."""
    game_filter = entry.data.get("game_filter", "all")
    scan_interval = entry.data.get("scan_interval", 300)

    coordinator = AnkamaStatusCoordinator(hass, scan_interval)
    await coordinator.async_config_entry_first_refresh()

    sensors = []
    for server in coordinator.data:
        # Filter by game if needed
        if game_filter != "all":
            if game_filter not in server.get("tags", []):
                continue
        
        sensors.append(AnkamaServerSensor(coordinator, server, entry))

    async_add_entities(sensors)


class AnkamaStatusCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Ankama server status data."""

    def __init__(self, hass: HomeAssistant, scan_interval: int) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> list[dict[str, Any]]:
        """Fetch data from API."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(ANKAMA_API_URL, timeout=30) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error fetching data: {response.status}")
                    
                    data = await response.json()
                    
                    if not isinstance(data, list):
                        raise UpdateFailed("Invalid data format")
                    
                    return data
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}")


class AnkamaServerSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Ankama game server status sensor."""

    def __init__(
        self,
        coordinator: AnkamaStatusCoordinator,
        server_data: dict[str, Any],
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        
        self._server_name_en = server_data["names"].get("en", "Unknown")
        self._server_name_fr = server_data["names"].get("fr", self._server_name_en)
        self._tags = server_data.get("tags", [])
        self._game = self._get_game_from_tags()
        
        # Create unique ID
        self._attr_unique_id = f"{DOMAIN}_{self._game}_{self._server_name_en.lower().replace(' ', '_')}"
        
        # Set name
        self._attr_name = f"{self._game.title()} - {self._server_name_fr}"
        
        # Set device info for grouping
        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"{self._game}")},
            "name": f"Ankama {self._game.title()}",
            "manufacturer": "Ankama",
            "model": self._game.title(),
        }

    def _get_game_from_tags(self) -> str:
        """Extract game name from tags."""
        game_tags = ["dofus2", "wakfu", "waven", "dofusTouch", "dofusRetro"]
        for tag in self._tags:
            if tag in game_tags:
                return tag
        return "unknown"

    def _get_server_data(self) -> dict[str, Any] | None:
        """Get current server data from coordinator."""
        if not self.coordinator.data:
            return None
        
        for server in self.coordinator.data:
            if (
                server["names"].get("en") == self._server_name_en
                and self._game in server.get("tags", [])
            ):
                return server
        return None

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        server_data = self._get_server_data()
        if server_data is None:
            return None
        return server_data.get("status", "Unknown")

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        status = self.native_value
        if status == STATUS_ONLINE:
            return "mdi:server-network"
        elif status == STATUS_MAINTENANCE:
            return "mdi:server-network-off"
        else:
            return "mdi:server-off"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        server_data = self._get_server_data()
        if server_data is None:
            return {}
        
        return {
            "server_name_en": server_data["names"].get("en"),
            "server_name_fr": server_data["names"].get("fr"),
            "server_name_es": server_data["names"].get("es"),
            "server_name_de": server_data["names"].get("de"),
            "server_name_pt": server_data["names"].get("pt"),
            "game": self._game,
            "tags": server_data.get("tags", []),
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self._get_server_data() is not None
