"""Constantes pour l'intégration Volet Roulant Relais USB."""

DOMAIN = "volet_relais_usb"

# Valeurs par défaut
DEFAULT_NAME = "Volet Roulant"
DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BAUD_RATE = 9600
DEFAULT_TRAVEL_TIME = 30

# Configuration
CONF_TRAVEL_TIME = "travel_time"

# Canaux du relais
CANAL_MONTEE = 1
CANAL_DESCENTE = 2

# Durée maximale de sécurité (secondes)
DUREE_MAX = 40
