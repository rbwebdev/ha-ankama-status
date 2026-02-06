"""Config flow for Ankama Status integration."""
import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import aiohttp

from .const import DOMAIN, ANKAMA_API_URL

_LOGGER = logging.getLogger(__name__)

GAME_OPTIONS = {
    "all": "All games",
    "dofus2": "Dofus 3",
    "wakfu": "Wakfu",
    "waven": "Waven",
    "dofusTouch": "Dofus Touch",
    "dofusRetro": "Dofus Retro",
}


async def validate_connection(hass: HomeAssistant) -> bool:
    """Validate that we can connect to the Ankama API."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(ANKAMA_API_URL, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return isinstance(data, list) and len(data) > 0
    except Exception as err:
        _LOGGER.error("Error connecting to Ankama API: %s", err)
        return False
    return False


class AnkamaStatusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ankama Status."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate connection
            if await validate_connection(self.hass):
                # Check if already configured
                await self.async_set_unique_id("ankama_status")
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title="Ankama Game Servers",
                    data=user_input,
                )
            else:
                errors["base"] = "cannot_connect"

        # Show form
        data_schema = vol.Schema(
            {
                vol.Optional("game_filter", default="all"): vol.In(GAME_OPTIONS),
                vol.Optional("scan_interval", default=300): vol.All(
                    vol.Coerce(int), vol.Range(min=60, max=3600)
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
