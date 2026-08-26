"""Constantes pour l'intégration Volet Roulant Relais USB."""

DOMAIN = "volet_relais_usb"

# Valeurs par défaut
DEFAULT_NAME = "Volet Roulant"
DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BAUD_RATE = 9600
DEFAULT_TRAVEL_TIME = 30
DEFAULT_PULSE_MODE = "short"
DEFAULT_SHORT_PULSE_DURATION = 0.5
DEFAULT_LONG_PULSE_DURATION = 30

# Configuration
CONF_TRAVEL_TIME = "travel_time"
CONF_INVERT_RELAY = "invert_relay"
CONF_PULSE_MODE = "pulse_mode"
CONF_SHORT_PULSE_DURATION = "short_pulse_duration"
CONF_LONG_PULSE_DURATION = "long_pulse_duration"

# Modes d'impulsion
PULSE_MODE_SHORT = "short"
PULSE_MODE_LONG = "long"

# Plages de durée (en secondes)
SHORT_PULSE_MIN = 0.2
SHORT_PULSE_MAX = 1.0
LONG_PULSE_MIN = 2
LONG_PULSE_MAX = 120

# Canaux du relais
CANAL_MONTEE = 1
CANAL_DESCENTE = 2

# Durée maximale de sécurité (secondes)
DUREE_MAX = 120
