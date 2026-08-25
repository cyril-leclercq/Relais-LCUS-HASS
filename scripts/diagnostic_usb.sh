#\!/bin/bash
# Script de diagnostic USB pour module relais LCUS

echo "=== Diagnostic Module USB Relais LCUS ==="
echo ""

echo "1. Vérification périphériques USB connectés:"
lsusb | grep -E "1a86:7523|CH340|USB.*Serial"
echo ""

echo "2. Vérification des ports série disponibles:"
ls -la /dev/tty* | grep -E "USB|ACM"
echo ""

echo "3. Vérification messages kernel (dmesg):"
dmesg | grep -E "tty|USB|ch341" | tail -20
echo ""

echo "4. Vérification processus utilisant les ports série:"
sudo lsof 2>/dev/null | grep -E "ttyUSB|ttyACM" || echo "Aucun processus détecté"
echo ""

echo "5. Vérification permissions utilisateur:"
echo "Utilisateur actuel: $(whoami)"
echo "Groupes: $(groups)"
echo "Membre de dialout: $(groups | grep -q dialout && echo 'OUI ✓' || echo 'NON ✗')"
echo ""

echo "6. Test de connexion série (si port trouvé):"
PORT=$(ls /dev/ttyUSB* 2>/dev/null | head -1)
if [ -n "$PORT" ]; then
    echo "Test sur $PORT..."
    python3 -c "
import serial
try:
    s = serial.Serial('$PORT', 9600, timeout=1)
    print('✓ Connexion réussie\!')
    s.close()
except Exception as e:
    print('✗ Erreur:', e)
" 2>&1
else
    echo "Aucun port /dev/ttyUSB* trouvé"
fi
echo ""

echo "=== Fin du diagnostic ==="
