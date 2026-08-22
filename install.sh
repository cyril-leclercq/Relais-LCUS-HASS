#!/bin/bash
# Script d'installation pour l'intégration Home Assistant

echo "=== Installation du contrôle de volet roulant pour Home Assistant ==="
echo ""

# 1. Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Installez-le d'abord."
    exit 1
fi
echo "✅ Python 3 trouvé: $(python3 --version)"

# 2. Installer pyserial
echo ""
echo "Installation de pyserial..."
python3 -m pip install pyserial
echo "✅ pyserial installé"

# 3. Tester la connexion USB
echo ""
echo "Test de la connexion USB..."
if [ -e "/dev/tty.usbserial-1110" ]; then
    echo "✅ Port USB trouvé: /dev/tty.usbserial-1110"
elif [ -e "/dev/ttyUSB0" ]; then
    echo "✅ Port USB trouvé: /dev/ttyUSB0"
    echo "⚠️  Modifiez relais.py pour utiliser /dev/ttyUSB0"
else
    echo "⚠️  Port USB non trouvé. Vérifiez votre connexion et modifiez relais.py"
fi

# 4. Rendre les scripts exécutables
echo ""
echo "Configuration des permissions..."
chmod +x volet_*.py
echo "✅ Scripts rendus exécutables"

# 5. Test des scripts
echo ""
echo "Test des scripts (sans exécution réelle)..."
echo "Vérification: volet_monter.py"
python3 -c "import volet_monter; print('✅ volet_monter.py OK')" 2>/dev/null || echo "⚠️  Vérifiez volet_monter.py"
echo "Vérification: volet_descendre.py"
python3 -c "import volet_descendre; print('✅ volet_descendre.py OK')" 2>/dev/null || echo "⚠️  Vérifiez volet_descendre.py"
echo "Vérification: volet_arreter.py"
python3 -c "import volet_arreter; print('✅ volet_arreter.py OK')" 2>/dev/null || echo "⚠️  Vérifiez volet_arreter.py"

# 6. Instructions Home Assistant
echo ""
echo "=== PROCHAINES ÉTAPES ==="
echo ""
echo "1. Copiez le contenu de 'homeassistant_config.yaml'"
echo "2. Collez-le dans votre configuration Home Assistant (configuration.yaml)"
echo "3. IMPORTANT: Modifiez les chemins dans homeassistant_config.yaml:"
echo "   - Remplacez /opt/homebrew/bin/python3 par le chemin de votre Python"
echo "   - Remplacez /Users/zunix/Src/relais par le chemin de ce répertoire"
echo "4. Ajustez la durée (30 secondes par défaut) selon votre volet"
echo "5. Redémarrez Home Assistant"
echo "6. Votre volet apparaîtra comme 'cover.volet_roulant'"
echo ""
echo "Pour trouver le chemin de Python, exécutez:"
echo "  which python3"
echo ""
echo "Chemin actuel du projet: $(pwd)"
echo ""
echo "✅ Installation terminée!"
