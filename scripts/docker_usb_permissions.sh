#\!/bin/bash
# Configuration permissions USB pour Docker

echo "=== Configuration USB pour Home Assistant Docker ==="
echo ""

echo "IMPORTANT: L'utilisateur DOCKER n'a PAS besoin d'être dans dialout\!"
echo "Les permissions se gèrent au niveau de l'HÔTE."
echo ""

# Méthode 1: Permissions sur l'hôte (RECOMMANDÉ)
echo "📌 Méthode 1: Permissions hôte + udev (RECOMMANDÉ)"
echo "=================================================="
echo ""
echo "1. Créer la règle udev sur l'HÔTE:"
echo "   sudo nano /etc/udev/rules.d/99-lcus-relay.rules"
echo ""
echo "   Contenu:"
echo '   SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="lcus_relay", MODE="0666", GROUP="dialout"'
echo ""
echo "2. Recharger udev:"
echo "   sudo udevadm control --reload-rules"
echo "   sudo udevadm trigger"
echo ""
echo "3. Vérifier les permissions:"
echo "   ls -l /dev/lcus_relay"
echo "   # Doit afficher: crw-rw-rw- ... dialout ... /dev/lcus_relay"
echo ""
echo "4. Dans docker-compose.yml:"
echo "   services:"
echo "     homeassistant:"
echo "       devices:"
echo "         - /dev/lcus_relay:/dev/lcus_relay"
echo ""

# Méthode 2: Permissions temporaires
echo "📌 Méthode 2: Permissions temporaires (TEST RAPIDE)"
echo "===================================================="
echo ""
echo "sudo chmod 666 /dev/ttyUSB0"
echo "# Les permissions seront perdues au reboot\!"
echo ""

# Méthode 3: Privileged mode
echo "📌 Méthode 3: Mode privileged (MOINS SÉCURISÉ)"
echo "==============================================="
echo ""
echo "Dans docker-compose.yml:"
echo "  services:"
echo "    homeassistant:"
echo "      privileged: true"
echo "      devices:"
echo "        - /dev/ttyUSB0:/dev/ttyUSB0"
echo ""

# Vérification
echo "📋 Vérification actuelle:"
echo "========================="
echo ""

if [ -e /dev/ttyUSB0 ]; then
    echo "✓ Port série détecté: /dev/ttyUSB0"
    ls -l /dev/ttyUSB0
    echo ""
    echo "Permissions actuelles:"
    stat -c "%a %U:%G %n" /dev/ttyUSB0 2>/dev/null || stat -f "%Lp %Su:%Sg %N" /dev/ttyUSB0
else
    echo "✗ Aucun port /dev/ttyUSB0 trouvé"
fi
echo ""

if [ -e /dev/lcus_relay ]; then
    echo "✓ Device persistant détecté: /dev/lcus_relay"
    ls -l /dev/lcus_relay
else
    echo "ℹ️  Pas de device persistant /dev/lcus_relay (créer règle udev)"
fi
echo ""

echo "👤 Utilisateur actuel: $(whoami)"
echo "📦 Groupes: $(groups)"
echo ""

echo "=== Fin ==="
