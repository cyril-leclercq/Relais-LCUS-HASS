"""Configuration flow pour Volet Roulant Relais USB."""
import logging
from typing import Any

import serial
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_PORT,
    DEFAULT_TRAVEL_TIME,
    CONF_TRAVEL_TIME,
    CONF_INVERT_RELAY,
)

_LOGGER = logging.getLogger(__name__)


def validate_serial_port(port: str) -> bool:
    """Valider que le port série est accessible."""
    try:
        ser = serial.Serial(port, 9600, timeout=1)
        ser.close()
        return True
    except (serial.SerialException, OSError) as err:
        _LOGGER.error("Port série invalide %s: %s", port, err)
        return False


class VoletRelaisUSBConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Flux de configuration pour Volet Roulant Relais USB."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Gérer une configuration initiée par l'utilisateur."""
        errors = {}

        if user_input is not None:
            # Valider le port série
            port = user_input[CONF_PORT]
            is_valid = await self.hass.async_add_executor_job(
                validate_serial_port, port
            )

            if not is_valid:
                errors["base"] = "cannot_connect"
            else:
                # Créer l'entrée de configuration
                await self.async_set_unique_id(f"{DOMAIN}_{port.replace('/', '_')}")
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                )

        # Afficher le formulaire
        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=DEFAULT_NAME): cv.string,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.string,
                vol.Required(
                    CONF_TRAVEL_TIME, default=DEFAULT_TRAVEL_TIME
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=60)),
                vol.Optional(CONF_INVERT_RELAY, default=False): cv.boolean,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_import(self, import_config: dict[str, Any]) -> FlowResult:
        """Import d'une configuration depuis configuration.yaml."""
        return await self.async_step_user(import_config)
