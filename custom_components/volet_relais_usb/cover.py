"""Plateforme Cover pour Volet Roulant Relais USB."""
import logging
import asyncio
from typing import Any

import serial

from homeassistant.components.cover import (
    CoverEntity,
    CoverDeviceClass,
    CoverEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    CONF_TRAVEL_TIME,
    CONF_INVERT_RELAY,
    CANAL_MONTEE,
    CANAL_DESCENTE,
    DUREE_MAX,
    DEFAULT_BAUD_RATE,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configuration de l'entité cover depuis une config entry."""
    name = config_entry.data[CONF_NAME]
    port = config_entry.data[CONF_PORT]
    
    # Utiliser les options en priorité, sinon les données de configuration
    travel_time = config_entry.options.get(
        CONF_TRAVEL_TIME,
        config_entry.data.get(CONF_TRAVEL_TIME)
    )
    invert_relay = config_entry.options.get(
        CONF_INVERT_RELAY,
        config_entry.data.get(CONF_INVERT_RELAY, False)
    )

    cover = VoletRelaisUSBCover(name, port, travel_time, invert_relay)
    
    # Ajouter un listener pour les changements d'options
    config_entry.async_on_unload(
        config_entry.add_update_listener(update_listener)
    )
    
    async_add_entities([cover], True)


async def update_listener(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Gérer les mises à jour des options."""
    await hass.config_entries.async_reload(config_entry.entry_id)


class VoletRelaisUSBCover(CoverEntity):
    """Représentation d'un volet roulant contrôlé par relais USB."""

    _attr_device_class = CoverDeviceClass.SHUTTER
    _attr_supported_features = (
        CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP
    )

    def __init__(self, name: str, port: str, travel_time: int, invert_relay: bool = False) -> None:
        """Initialisation du volet."""
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{port.replace('/', '_')}"
        self._port = port
        self._travel_time = travel_time
        self._invert_relay = invert_relay
        self._serial_port = None
        self._is_opening = False
        self._is_closing = False
        
        # Définir les canaux selon l'inversion
        if self._invert_relay:
            self._canal_montee = CANAL_DESCENTE
            self._canal_descente = CANAL_MONTEE
        else:
            self._canal_montee = CANAL_MONTEE
            self._canal_descente = CANAL_DESCENTE
        
        # Initialiser la connexion série
        self._init_serial()

    def _init_serial(self) -> None:
        """Initialiser la connexion série."""
        try:
            self._serial_port = serial.Serial(
                self._port, DEFAULT_BAUD_RATE, timeout=1
            )
            _LOGGER.info("Connexion série établie sur %s", self._port)
        except serial.SerialException as err:
            _LOGGER.error("Impossible d'ouvrir le port %s: %s", self._port, err)
            self._serial_port = None

    def _relais(self, canal: int, etat: bool) -> None:
        """Contrôler un relais."""
        if self._serial_port is None or not self._serial_port.is_open:
            _LOGGER.warning("Port série non disponible")
            return

        try:
            # Trame de commande : [0xA0, canal, état, checksum]
            trame = bytes([
                0xA0,
                canal,
                1 if etat else 0,
                (0xA0 + canal + (1 if etat else 0)) & 0xFF
            ])
            self._serial_port.write(trame)
            _LOGGER.debug("Commande envoyée: canal=%d, etat=%d", canal, etat)
        except serial.SerialException as err:
            _LOGGER.error("Erreur lors de l'envoi de la commande: %s", err)

    def _stop_tous_relais(self) -> None:
        """Arrêter tous les relais."""
        self._relais(self._canal_montee, False)
        self._relais(self._canal_descente, False)
        self._is_opening = False
        self._is_closing = False

    @property
    def is_opening(self) -> bool:
        """Retourne si le volet est en train de s'ouvrir."""
        return self._is_opening

    @property
    def is_closing(self) -> bool:
        """Retourne si le volet est en train de se fermer."""
        return self._is_closing

    @property
    def is_closed(self) -> bool | None:
        """Retourne si le volet est fermé (None = inconnu)."""
        return None

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Ouvrir le volet."""
        _LOGGER.info("Ouverture du volet pendant %d secondes", self._travel_time)
        
        await self.hass.async_add_executor_job(self._stop_tous_relais)
        await asyncio.sleep(0.1)
        
        self._is_opening = True
        self.async_write_ha_state()
        
        try:
            await self.hass.async_add_executor_job(
                self._relais, self._canal_montee, True
            )
            await asyncio.sleep(min(self._travel_time, DUREE_MAX))
        finally:
            await self.hass.async_add_executor_job(
                self._relais, self._canal_montee, False
            )
            self._is_opening = False
            self.async_write_ha_state()

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Fermer le volet."""
        _LOGGER.info("Fermeture du volet pendant %d secondes", self._travel_time)
        
        await self.hass.async_add_executor_job(self._stop_tous_relais)
        await asyncio.sleep(0.1)
        
        self._is_closing = True
        self.async_write_ha_state()
        
        try:
            await self.hass.async_add_executor_job(
                self._relais, self._canal_descente, True
            )
            await asyncio.sleep(min(self._travel_time, DUREE_MAX))
        finally:
            await self.hass.async_add_executor_job(
                self._relais, self._canal_descente, False
            )
            self._is_closing = False
            self.async_write_ha_state()

    async def async_stop_cover(self, **kwargs: Any) -> None:
        """Arrêter le volet."""
        _LOGGER.info("Arrêt du volet")
        await self.hass.async_add_executor_job(self._stop_tous_relais)
        self.async_write_ha_state()

    async def async_will_remove_from_hass(self) -> None:
        """Nettoyage avant suppression."""
        if self._serial_port and self._serial_port.is_open:
            await self.hass.async_add_executor_job(self._stop_tous_relais)
            await self.hass.async_add_executor_job(self._serial_port.close)
