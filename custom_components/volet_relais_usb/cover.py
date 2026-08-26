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
    CONF_INVERT_RELAY,
    CONF_PULSE_MODE,
    CONF_SHORT_PULSE_DURATION,
    CONF_LONG_PULSE_DURATION,
    CANAL_MONTEE,
    CANAL_DESCENTE,
    DUREE_MAX,
    DEFAULT_BAUD_RATE,
    DEFAULT_PULSE_MODE,
    DEFAULT_SHORT_PULSE_DURATION,
    DEFAULT_LONG_PULSE_DURATION,
    PULSE_MODE_SHORT,
    PULSE_MODE_LONG,
    normalize_short_pulse_ms,
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
    invert_relay = config_entry.options.get(
        CONF_INVERT_RELAY,
        config_entry.data.get(CONF_INVERT_RELAY, False)
    )
    pulse_mode = config_entry.options.get(
        CONF_PULSE_MODE,
        config_entry.data.get(CONF_PULSE_MODE, DEFAULT_PULSE_MODE)
    )
    short_pulse_duration = normalize_short_pulse_ms(
        config_entry.options.get(
            CONF_SHORT_PULSE_DURATION,
            config_entry.data.get(CONF_SHORT_PULSE_DURATION, DEFAULT_SHORT_PULSE_DURATION)
        )
    )
    long_pulse_duration = config_entry.options.get(
        CONF_LONG_PULSE_DURATION,
        config_entry.data.get(CONF_LONG_PULSE_DURATION, DEFAULT_LONG_PULSE_DURATION)
    )

    cover = VoletRelaisUSBCover(
        name,
        port,
        invert_relay,
        pulse_mode,
        short_pulse_duration,
        long_pulse_duration
    )
    
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

    def __init__(
        self,
        name: str,
        port: str,
        invert_relay: bool = False,
        pulse_mode: str = DEFAULT_PULSE_MODE,
        short_pulse_duration: int = DEFAULT_SHORT_PULSE_DURATION,
        long_pulse_duration: int = DEFAULT_LONG_PULSE_DURATION
    ) -> None:
        """Initialisation du volet."""
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{port.replace('/', '_')}"
        self._port = port
        self._invert_relay = invert_relay
        self._pulse_mode = pulse_mode
        self._short_pulse_duration_ms = short_pulse_duration
        self._long_pulse_duration = long_pulse_duration
        self._serial_port = None
        self._is_opening = False
        self._is_closing = False
        self._canal_actif: int | None = None
        
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
        """Couper les relais (sans envoyer d'impulsion d'arrêt au moteur)."""
        self._relais(self._canal_montee, False)
        self._relais(self._canal_descente, False)

    def _mode_description(self) -> str:
        """Décrit le mode d'impulsion actif et sa durée, pour les logs."""
        if self._pulse_mode == PULSE_MODE_SHORT:
            return f"mode impulsion ({self._short_pulse_duration_ms} ms)"
        return f"mode continu ({self._long_pulse_duration} s)"

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

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Attributs supplémentaires : mode d'impulsion actif et sa durée."""
        if self._pulse_mode == PULSE_MODE_SHORT:
            return {
                "pulse_mode": "Impulsion courte",
                "pulse_duration": f"{self._short_pulse_duration_ms} ms",
            }
        return {
            "pulse_mode": "Maintenu",
            "pulse_duration": f"{self._long_pulse_duration} s",
        }

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Ouvrir le volet."""
        await self._demarrer_mouvement(self._canal_montee, ouverture=True)

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Fermer le volet."""
        await self._demarrer_mouvement(self._canal_descente, ouverture=False)

    async def _demarrer_mouvement(self, canal: int, ouverture: bool) -> None:
        """Déclencher le mouvement d'ouverture ou de fermeture sur un canal."""
        # Déterminer la durée selon le mode
        if self._pulse_mode == PULSE_MODE_SHORT:
            duration = self._short_pulse_duration_ms / 1000
        else:
            duration = self._long_pulse_duration

        _LOGGER.info(
            "%s du volet - %s",
            "Ouverture" if ouverture else "Fermeture", self._mode_description()
        )

        # Arrêter proprement un éventuel mouvement en cours avant d'en lancer un nouveau
        await self._envoyer_arret()
        await asyncio.sleep(0.1)

        self._is_opening = ouverture
        self._is_closing = not ouverture
        self._canal_actif = canal
        self.async_write_ha_state()

        try:
            await self.hass.async_add_executor_job(self._relais, canal, True)
            await asyncio.sleep(min(duration, DUREE_MAX))
        finally:
            await self.hass.async_add_executor_job(self._relais, canal, False)
            if self._pulse_mode == PULSE_MODE_LONG:
                # Mode maintenu : le relais couvre toute la course, le mouvement
                # est donc terminé une fois la durée écoulée.
                self._is_opening = False
                self._is_closing = False
                self._canal_actif = None
            # En mode impulsion courte, le moteur continue de bouger seul après
            # le relâchement du bouton : l'état n'est réinitialisé qu'à l'arrêt
            # effectif (async_stop_cover), pas ici.
            self.async_write_ha_state()

    async def _envoyer_arret(self) -> None:
        """Envoyer le signal d'arrêt approprié selon le mode d'impulsion."""
        _LOGGER.info("Arrêt du volet - %s", self._mode_description())

        if self._pulse_mode == PULSE_MODE_SHORT and self._canal_actif is not None:
            # Ces moteurs s'arrêtent par un nouvel appui sur le bouton déjà
            # actif (montée/montée ou descente/descente) : un simple coupure
            # du relais (déjà retombé depuis longtemps) ne suffit pas.
            canal = self._canal_actif
            await self.hass.async_add_executor_job(self._relais, canal, True)
            await asyncio.sleep(self._short_pulse_duration_ms / 1000)
            await self.hass.async_add_executor_job(self._relais, canal, False)
        else:
            await self.hass.async_add_executor_job(self._stop_tous_relais)

    async def async_stop_cover(self, **kwargs: Any) -> None:
        """Arrêter le volet."""
        await self._envoyer_arret()
        self._is_opening = False
        self._is_closing = False
        self._canal_actif = None
        self.async_write_ha_state()

    async def async_will_remove_from_hass(self) -> None:
        """Nettoyage avant suppression."""
        if self._serial_port and self._serial_port.is_open:
            await self.hass.async_add_executor_job(self._stop_tous_relais)
            await self.hass.async_add_executor_job(self._serial_port.close)
