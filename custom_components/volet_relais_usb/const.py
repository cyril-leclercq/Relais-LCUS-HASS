"""Constantes pour l'intégration Volet Roulant Relais USB."""

DOMAIN = "volet_relais_usb"

# Valeurs par défaut
DEFAULT_NAME = "Volet Roulant"
DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BAUD_RATE = 9600
DEFAULT_PULSE_MODE = "short"
DEFAULT_SHORT_PULSE_DURATION = 500  # millisecondes
DEFAULT_LONG_PULSE_DURATION = 30  # secondes

# Configuration
CONF_INVERT_RELAY = "invert_relay"
CONF_PULSE_MODE = "pulse_mode"
CONF_SHORT_PULSE_DURATION = "short_pulse_duration"
CONF_LONG_PULSE_DURATION = "long_pulse_duration"

# Modes d'impulsion
PULSE_MODE_SHORT = "short"
PULSE_MODE_LONG = "long"

# Plages de durée
SHORT_PULSE_MIN = 50  # millisecondes
SHORT_PULSE_MAX = 600  # millisecondes
LONG_PULSE_MIN = 2  # secondes
LONG_PULSE_MAX = 120  # secondes

# Canaux du relais
CANAL_MONTEE = 1
CANAL_DESCENTE = 2

# Durée maximale de sécurité (secondes)
DUREE_MAX = 120


def normalize_short_pulse_ms(value: float) -> int:
    """Normalise une durée d'impulsion courte en millisecondes.

    Les anciennes configurations stockaient cette durée en secondes
    (0.2 à 1.0) ; on les convertit et on les recadre dans la nouvelle
    plage (50 à 600 ms) plutôt que d'invalider les entrées existantes.
    """
    ms = round(value * 1000) if value < 10 else int(value)
    return max(SHORT_PULSE_MIN, min(SHORT_PULSE_MAX, ms))
