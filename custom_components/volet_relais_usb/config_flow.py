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
    DEFAULT_PULSE_MODE,
    DEFAULT_SHORT_PULSE_DURATION,
    DEFAULT_LONG_PULSE_DURATION,
    CONF_INVERT_RELAY,
    CONF_PULSE_MODE,
    CONF_SHORT_PULSE_DURATION,
    CONF_LONG_PULSE_DURATION,
    PULSE_MODE_SHORT,
    PULSE_MODE_LONG,
    SHORT_PULSE_MIN,
    SHORT_PULSE_MAX,
    LONG_PULSE_MIN,
    LONG_PULSE_MAX,
    normalize_short_pulse_ms,
)

_LOGGER = logging.getLogger(__name__)

PULSE_MODE_LABELS = {
    PULSE_MODE_SHORT: "Impulsion courte (50-600 ms) - Pour commandes momentanées",
    PULSE_MODE_LONG: "Maintenu (2s-2min) - Pour course complète du volet",
}


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

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Obtenir le flux d'options."""
        return VoletRelaisUSBOptionsFlow()

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

                self._data = user_input
                if user_input[CONF_PULSE_MODE] == PULSE_MODE_SHORT:
                    return await self.async_step_pulse_short()
                return await self.async_step_pulse_long()

        # Afficher le formulaire avec sélecteurs modernes
        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=DEFAULT_NAME): cv.string,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.string,
                vol.Required(CONF_PULSE_MODE, default=DEFAULT_PULSE_MODE): vol.In(
                    PULSE_MODE_LABELS
                ),
                vol.Optional(CONF_INVERT_RELAY, default=False): cv.boolean,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_pulse_short(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Étape dédiée à la durée d'impulsion courte (mode impulsion uniquement)."""
        if user_input is not None:
            self._data.update(user_input)
            return self.async_create_entry(title=self._data[CONF_NAME], data=self._data)

        default_short_pulse = normalize_short_pulse_ms(
            self._data.get(CONF_SHORT_PULSE_DURATION, DEFAULT_SHORT_PULSE_DURATION)
        )
        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_SHORT_PULSE_DURATION, default=default_short_pulse
                ): vol.All(vol.Coerce(int), vol.Range(min=SHORT_PULSE_MIN, max=SHORT_PULSE_MAX)),
            }
        )

        return self.async_show_form(
            step_id="pulse_short",
            data_schema=data_schema,
        )

    async def async_step_pulse_long(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Étape dédiée à la durée de maintien (mode maintenu uniquement)."""
        if user_input is not None:
            self._data.update(user_input)
            return self.async_create_entry(title=self._data[CONF_NAME], data=self._data)

        default_long_pulse = self._data.get(
            CONF_LONG_PULSE_DURATION, DEFAULT_LONG_PULSE_DURATION
        )
        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_LONG_PULSE_DURATION, default=default_long_pulse
                ): vol.All(vol.Coerce(int), vol.Range(min=LONG_PULSE_MIN, max=LONG_PULSE_MAX)),
            }
        )

        return self.async_show_form(
            step_id="pulse_long",
            data_schema=data_schema,
        )

    async def async_step_import(self, import_config: dict[str, Any]) -> FlowResult:
        """Import d'une configuration depuis configuration.yaml."""
        return await self.async_step_user(import_config)


class VoletRelaisUSBOptionsFlow(config_entries.OptionsFlow):
    """Flux d'options pour Volet Roulant Relais USB."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Gérer les options communes, puis router vers la durée du mode choisi."""
        if user_input is not None:
            self._data = dict(user_input)
            if user_input[CONF_PULSE_MODE] == PULSE_MODE_SHORT:
                return await self.async_step_pulse_short()
            return await self.async_step_pulse_long()

        # Récupérer les valeurs actuelles depuis data ou options
        current_invert_relay = self.config_entry.options.get(
            CONF_INVERT_RELAY,
            self.config_entry.data.get(CONF_INVERT_RELAY, False)
        )
        current_pulse_mode = self.config_entry.options.get(
            CONF_PULSE_MODE,
            self.config_entry.data.get(CONF_PULSE_MODE, DEFAULT_PULSE_MODE)
        )

        options_schema = vol.Schema(
            {
                vol.Required(CONF_PULSE_MODE, default=current_pulse_mode): vol.In(
                    PULSE_MODE_LABELS
                ),
                vol.Optional(
                    CONF_INVERT_RELAY, default=current_invert_relay
                ): cv.boolean,
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
        )

    async def async_step_pulse_short(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Étape dédiée à la durée d'impulsion courte (mode impulsion uniquement)."""
        if user_input is not None:
            self._data.update(user_input)
            return self.async_create_entry(title="", data=self._data)

        current_short_pulse = normalize_short_pulse_ms(
            self.config_entry.options.get(
                CONF_SHORT_PULSE_DURATION,
                self.config_entry.data.get(
                    CONF_SHORT_PULSE_DURATION, DEFAULT_SHORT_PULSE_DURATION
                )
            )
        )

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_SHORT_PULSE_DURATION, default=current_short_pulse
                ): vol.All(vol.Coerce(int), vol.Range(min=SHORT_PULSE_MIN, max=SHORT_PULSE_MAX)),
            }
        )

        return self.async_show_form(
            step_id="pulse_short",
            data_schema=data_schema,
        )

    async def async_step_pulse_long(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Étape dédiée à la durée de maintien (mode maintenu uniquement)."""
        if user_input is not None:
            self._data.update(user_input)
            return self.async_create_entry(title="", data=self._data)

        current_long_pulse = self.config_entry.options.get(
            CONF_LONG_PULSE_DURATION,
            self.config_entry.data.get(
                CONF_LONG_PULSE_DURATION, DEFAULT_LONG_PULSE_DURATION
            )
        )

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_LONG_PULSE_DURATION, default=current_long_pulse
                ): vol.All(vol.Coerce(int), vol.Range(min=LONG_PULSE_MIN, max=LONG_PULSE_MAX)),
            }
        )

        return self.async_show_form(
            step_id="pulse_long",
            data_schema=data_schema,
        )
