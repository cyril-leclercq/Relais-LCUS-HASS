#!/bin/bash
# Script d'installation pour Home Assistant dans Docker

echo "=== Installation du volet roulant pour Home Assistant (Docker) ==="
echo ""

# 1. Variables
HASS_CONFIG_DIR="/opt/docker/hass/config"
SCRIPT_DIR="$HASS_CONFIG_DIR/scripts/relais"

# Demander le répertoire de config Home Assistant
read -p "Chemin vers le config de Home Assistant [$HASS_CONFIG_DIR]: " custom_dir
HASS_CONFIG_DIR=${custom_dir:-$HASS_CONFIG_DIR}
SCRIPT_DIR="$HASS_CONFIG_DIR/scripts/relais"

echo ""
echo "Configuration:"
echo "  - Home Assistant config: $HASS_CONFIG_DIR"
echo "  - Scripts: $SCRIPT_DIR"
echo ""

# 2. Identifier le port USB
echo "=== Identification du port USB ==="
echo "Ports USB disponibles:"
ls /dev/tty* 2>/dev/null | grep -i usb || echo "Aucun port ttyUSB trouvé"
ls /dev/tty.* 2>/dev/null | grep -i usb || echo "Aucun port tty.usb trouvé"
echo ""

read -p "Quel port USB utilisez-vous? [/dev/ttyUSB0]: " usb_port
USB_PORT=${usb_port:-/dev/ttyUSB0}

echo "✅ Port USB: $USB_PORT"

# 3. Créer le répertoire pour les scripts
echo ""
echo "=== Création du répertoire scripts ==="
if [ ! -d "$HASS_CONFIG_DIR" ]; then
    echo "❌ Le répertoire $HASS_CONFIG_DIR n'existe pas!"
    echo "Vérifiez le chemin vers votre configuration Home Assistant."
    exit 1
fi

mkdir -p "$SCRIPT_DIR"
echo "✅ Répertoire créé: $SCRIPT_DIR"

# 4. Copier les scripts
echo ""
echo "=== Copie des scripts Python ==="
cp -v relais.py "$SCRIPT_DIR/"
cp -v volet_monter.py "$SCRIPT_DIR/"
cp -v volet_descendre.py "$SCRIPT_DIR/"
cp -v volet_arreter.py "$SCRIPT_DIR/"
chmod +x "$SCRIPT_DIR"/volet_*.py
echo "✅ Scripts copiés et rendus exécutables"

# 5. Installer pyserial dans le conteneur
echo ""
echo "=== Installation de pyserial dans Home Assistant ==="
echo "Vérification du conteneur..."

if docker ps | grep -q homeassistant; then
    echo "Conteneur Home Assistant trouvé!"
    echo "Installation de pyserial..."
    docker exec homeassistant pip install pyserial
    echo "✅ pyserial installé"
else
    echo "⚠️  Conteneur 'homeassistant' non trouvé ou arrêté"
    echo "Installez manuellement pyserial avec:"
    echo "  docker exec homeassistant pip install pyserial"
fi

# 6. Créer/mettre à jour docker-compose.yml
echo ""
echo "=== Configuration Docker ==="
echo ""
echo "⚠️  IMPORTANT: Ajoutez cette section à votre docker-compose.yml:"
echo ""
cat << EOF
services:
  homeassistant:
    # ... votre configuration existante ...
    devices:
      - $USB_PORT:$USB_PORT
EOF
echo ""

# 7. Créer une règle udev (optionnel)
echo ""
read -p "Voulez-vous créer une règle udev pour un nom persistant? (recommandé) [o/N]: " create_udev
if [[ "$create_udev" =~ ^[oOyY]$ ]]; then
    echo ""
    echo "Recherche du numéro de série du périphérique..."
    SERIAL=$(udevadm info -a -n "$USB_PORT" 2>/dev/null | grep 'ATTRS{serial}' | head -1 | sed 's/.*=="\(.*\)".*/\1/')
    
    if [ -n "$SERIAL" ]; then
        echo "Numéro de série trouvé: $SERIAL"
        UDEV_FILE="/etc/udev/rules.d/99-volet-relais.rules"
        
        echo "Création de la règle udev..."
        sudo bash -c "cat > $UDEV_FILE" << EOF
# Règle pour le module relais du volet roulant
SUBSYSTEM=="tty", ATTRS{serial}=="$SERIAL", SYMLINK+="volet_relais", MODE="0666"
EOF
        
        echo "Rechargement des règles udev..."
        sudo udevadm control --reload-rules
        sudo udevadm trigger
        
        echo "✅ Règle udev créée: $UDEV_FILE"
        echo "   Device: /dev/volet_relais"
        echo ""
        echo "⚠️  Mettez à jour docker-compose.yml avec:"
        echo "    devices:"
        echo "      - /dev/volet_relais:/dev/volet_relais"
        echo ""
        USB_PORT="/dev/volet_relais"
    else
        echo "⚠️  Impossible de trouver le numéro de série"
        echo "Vérifiez que le périphérique est branché: $USB_PORT"
    fi
fi

# 8. Configuration Home Assistant
echo ""
echo "=== Configuration Home Assistant ==="
CONFIG_SNIPPET="$HASS_CONFIG_DIR/volet_roulant_config.yaml"

cat > "$CONFIG_SNIPPET" << EOF
# Configuration pour le volet roulant USB
# Copiez ce contenu dans votre configuration.yaml

input_text:
  volet_usb_port:
    name: Port USB du volet roulant
    initial: $USB_PORT
    icon: mdi:usb-port

shell_command:
  volet_monter: "RELAIS_USB_PORT={{ states('input_text.volet_usb_port') }} python3 /config/scripts/relais/volet_monter.py {{ duree|default(30) }}"
  volet_descendre: "RELAIS_USB_PORT={{ states('input_text.volet_usb_port') }} python3 /config/scripts/relais/volet_descendre.py {{ duree|default(30) }}"
  volet_arreter: "RELAIS_USB_PORT={{ states('input_text.volet_usb_port') }} python3 /config/scripts/relais/volet_arreter.py"

cover:
  - platform: template
    covers:
      volet_roulant:
        device_class: shutter
        friendly_name: "Volet Roulant"
        open_cover:
          service: shell_command.volet_monter
          data:
            duree: 30
        close_cover:
          service: shell_command.volet_descendre
          data:
            duree: 30
        stop_cover:
          service: shell_command.volet_arreter
        icon_template: >-
          {% if is_state('cover.volet_roulant', 'open') %}
            mdi:window-shutter-open
          {% else %}
            mdi:window-shutter
          {% endif %}
EOF

echo "✅ Configuration créée: $CONFIG_SNIPPET"
echo ""
echo "Copiez le contenu de ce fichier dans votre configuration.yaml"

# 9. Résumé
echo ""
echo "==================================================================="
echo "=== INSTALLATION TERMINÉE ==="
echo "==================================================================="
echo ""
echo "PROCHAINES ÉTAPES:"
echo ""
echo "1. Modifiez docker-compose.yml pour ajouter le device USB:"
echo "   services:"
echo "     homeassistant:"
echo "       devices:"
echo "         - $USB_PORT:$USB_PORT"
echo ""
echo "2. Redéployez le stack:"
echo "   docker stack deploy -c docker-compose.yml votre-stack"
echo "   # OU"
echo "   docker-compose up -d --force-recreate"
echo ""
echo "3. Ajoutez la configuration dans Home Assistant:"
echo "   cat $CONFIG_SNIPPET"
echo ""
echo "4. Redémarrez Home Assistant depuis l'interface"
echo ""
echo "5. Testez le volet depuis Developer Tools > Services:"
echo "   service: shell_command.volet_arreter"
echo ""
echo "==================================================================="
echo ""
echo "📚 Documentation complète: DOCKER_SETUP.md"
echo ""
