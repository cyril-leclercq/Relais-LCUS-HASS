# Détection du Module LCUS sur Linux Distant

Guide complet pour identifier et configurer le module relais USB LCUS sur un serveur Linux.

---

## 🔍 Étape 1 : Connexion au serveur Linux distant

```bash
# Connexion SSH à votre serveur
ssh user@votre-serveur-linux

# Ou si vous utilisez une clé SSH spécifique
ssh -i ~/.ssh/votre_cle user@votre-serveur-linux
```

---

## 🔌 Étape 2 : Détecter les périphériques USB série

### Méthode 1 : Lister tous les ports USB

```bash
# Voir tous les ports série USB
ls -la /dev/tty* | grep -E 'USB|ACM'

# Résultat attendu (exemple):
# /dev/ttyUSB0
# /dev/ttyUSB1
# /dev/ttyACM0
```

### Méthode 2 : Voir les périphériques USB connectés

```bash
# Lister tous les périphériques USB avec détails
lsusb

# Résultat exemple:
# Bus 001 Device 004: ID 1a86:7523 QinHeng Electronics CH340 serial converter
# Bus 001 Device 003: ID 0403:6001 Future Technology Devices International, Ltd FT232 Serial (UART) IC
```

### Méthode 3 : Informations détaillées sur les ports série

```bash
# Voir les informations détaillées
dmesg | grep -i "tty\|usb" | tail -20

# Ou plus spécifique pour les nouveaux devices
dmesg | grep -i "ch340\|ftdi\|cp210\|pl2303" | tail -10
```

### Méthode 4 : Utiliser udevadm

```bash
# Lister les attributs des périphériques USB
for device in /dev/ttyUSB*; do
  echo "=== $device ==="
  udevadm info -a -n $device | grep -E 'KERNEL|SUBSYSTEM|DRIVER|ATTRS{idVendor}|ATTRS{idProduct}|ATTRS{serial}'
  echo ""
done
```

---

## 🧪 Étape 3 : Identifier le bon port (test en live)

### Méthode 1 : Débrancher/rebrancher le module

```bash
# 1. Surveiller les changements en temps réel
watch -n 1 'ls -la /dev/tty* | grep USB'

# 2. Dans un autre terminal (ou déconnectez-vous temporairement)
#    Débranchez physiquement le module USB
#    Notez quel /dev/ttyUSBX disparaît
#    Rebranchez le module
#    Notez quel /dev/ttyUSBX réapparaît
#    → C'est votre module !

# Alternative avec dmesg (plus précis)
sudo dmesg -w

# Débranchez/rebranchez le module USB et observez les messages
# Vous verrez quelque chose comme:
# [ 1234.567890] usb 1-1.2: USB disconnect
# [ 1240.123456] usb 1-1.2: new full-speed USB device
# [ 1240.234567] ch341 1-1.2:1.0: ch341-uart converter detected
# [ 1240.345678] usb 1-1.2: ch341-uart converter now attached to ttyUSB0
#                                                                  ^^^^^^^^
#                                                          C'est votre port !
```

### Méthode 2 : Tester la communication série

```bash
# Installer pyserial si pas déjà fait
sudo apt update
sudo apt install python3-pip -y
pip3 install pyserial

# Tester chaque port USB détecté
for port in /dev/ttyUSB*; do
  echo "Test du port: $port"
  python3 -c "
import serial
try:
    s = serial.Serial('$port', 9600, timeout=1)
    print('✅ Connexion réussie sur $port')
    s.close()
except Exception as e:
    print('❌ Erreur sur $port:', e)
"
  echo ""
done
```

---

## 🔑 Étape 4 : Vérifier les permissions

### Voir les permissions actuelles

```bash
# Vérifier le propriétaire et les permissions
ls -l /dev/ttyUSB0

# Résultat typique:
# crw-rw---- 1 root dialout 188, 0 Jan 25 10:30 /dev/ttyUSB0
#            └─────┬─────┘
#              Groupe dialout requis
```

### Ajouter l'utilisateur au groupe dialout

```bash
# Ajouter votre utilisateur au groupe dialout
sudo usermod -aG dialout $USER

# Vérifier l'appartenance aux groupes
groups

# Si "dialout" n'apparaît pas encore, déconnectez-vous et reconnectez-vous
# OU redémarrez la session SSH
exit
ssh user@votre-serveur-linux
groups  # Vérifier à nouveau
```

### Solution temporaire (si pas de redémarrage possible)

```bash
# Donner les permissions temporairement (perdues au redémarrage)
sudo chmod 666 /dev/ttyUSB0

# Vérifier
ls -l /dev/ttyUSB0
# Devrait maintenant afficher: crw-rw-rw-
```

---

## 🏷️ Étape 5 : Créer un nom persistant avec udev (RECOMMANDÉ)

Le port USB peut changer (`/dev/ttyUSB0` → `/dev/ttyUSB1`) au redémarrage. 
Créons un nom fixe `/dev/volet_relais` ou `/dev/lcus_relay`.

### Identifier les attributs uniques du module

```bash
# Remplacez ttyUSB0 par votre port détecté
udevadm info -a -n /dev/ttyUSB0 | grep -E 'idVendor|idProduct|serial' | head -5

# Résultat exemple:
# ATTRS{idVendor}=="1a86"
# ATTRS{idProduct}=="7523"
# ATTRS{serial}=="0001"
```

### Créer la règle udev

```bash
# Créer le fichier de règle udev
sudo nano /etc/udev/rules.d/99-lcus-relay.rules

# Copier-coller cette règle (ajustez idVendor et idProduct selon votre module):
```

**Contenu du fichier `99-lcus-relay.rules`** :

```udev
# Règle udev pour module relais LCUS USB
# Identifié par idVendor et idProduct

# Pour CH340 (exemple: idVendor=1a86, idProduct=7523)
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="lcus_relay", MODE="0666", GROUP="dialout"

# OU pour FTDI (exemple: idVendor=0403, idProduct=6001)
# SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", SYMLINK+="lcus_relay", MODE="0666", GROUP="dialout"

# OU pour CP2102 (exemple: idVendor=10c4, idProduct=ea60)
# SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="lcus_relay", MODE="0666", GROUP="dialout"

# Si vous avez un numéro de série unique, utilisez cette règle (plus précis):
# SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{serial}=="0001", SYMLINK+="lcus_relay", MODE="0666", GROUP="dialout"
```

**Enregistrer** : `Ctrl+O`, `Entrée`, `Ctrl+X`

### Recharger les règles udev

```bash
# Recharger les règles udev
sudo udevadm control --reload-rules
sudo udevadm trigger

# Débrancher et rebrancher le module USB (ou attendre quelques secondes)

# Vérifier que le lien symbolique existe
ls -l /dev/lcus_relay

# Résultat attendu:
# lrwxrwxrwx 1 root root 7 Jan 25 10:45 /dev/lcus_relay -> ttyUSB0
```

---

## ✅ Étape 6 : Test final de communication

### Test Python depuis le serveur Linux

```bash
# Créer un script de test
cat > test_lcus.py << 'EOF'
#!/usr/bin/env python3
import serial
import time

# Testez avec /dev/ttyUSB0 OU /dev/lcus_relay
PORT = '/dev/lcus_relay'  # ou /dev/ttyUSB0
BAUD = 9600

print(f"🔌 Test de connexion au module LCUS sur {PORT}")

try:
    # Ouvrir la connexion série
    ser = serial.Serial(PORT, BAUD, timeout=1)
    print(f"✅ Connexion série ouverte sur {PORT}")
    print(f"   Débit: {BAUD} bauds")
    print(f"   Port: {ser.name}")
    
    # Test d'envoi de commande (exemple: activer relais 1)
    # Protocole: [0xA0, canal, état, checksum]
    commande = bytes([0xA0, 0x01, 0x01, 0xA2])  # Canal 1 ON
    print(f"\n📤 Envoi commande test: {commande.hex()}")
    ser.write(commande)
    
    time.sleep(0.1)
    
    # Lire la réponse si disponible
    if ser.in_waiting > 0:
        response = ser.read(ser.in_waiting)
        print(f"📥 Réponse reçue: {response.hex()}")
    else:
        print("📭 Pas de réponse (normal pour certains modules)")
    
    # Arrêt du relais
    commande_off = bytes([0xA0, 0x01, 0x00, 0xA1])  # Canal 1 OFF
    print(f"\n📤 Envoi commande arrêt: {commande_off.hex()}")
    ser.write(commande_off)
    
    time.sleep(0.1)
    
    ser.close()
    print("\n✅ Test terminé avec succès!")
    print(f"🎉 Le module LCUS est bien détecté sur {PORT}")
    
except serial.SerialException as e:
    print(f"❌ Erreur de connexion série: {e}")
    print("\n🔧 Vérifications à faire:")
    print("   1. Le port est-il correct? Vérifiez avec: ls -l /dev/tty*")
    print("   2. Avez-vous les permissions? Vérifiez avec: groups")
    print("   3. Le module est-il branché? Vérifiez avec: lsusb")
except Exception as e:
    print(f"❌ Erreur inattendue: {e}")

EOF

# Rendre le script exécutable
chmod +x test_lcus.py

# Exécuter le test
python3 test_lcus.py
```

---

## 🐳 Étape 7 : Configuration Docker (si Home Assistant dans conteneur)

### Vérifier que le port est accessible depuis le conteneur

```bash
# Si Home Assistant tourne dans Docker
docker exec homeassistant ls -l /dev/ttyUSB0

# Si erreur "No such file or directory":
# → Le mapping n'est pas fait dans docker-compose.yml

# Si erreur "Permission denied":
# → Problème de permissions (chmod 666 ou groupe dialout)
```

### Avec nom persistant (recommandé)

```bash
# Vérifier le lien symbolique
docker exec homeassistant ls -l /dev/lcus_relay

# Tester la connexion depuis le conteneur
docker exec homeassistant python3 -c "
import serial
s = serial.Serial('/dev/lcus_relay', 9600, timeout=1)
print('✅ Module LCUS accessible depuis le conteneur!')
s.close()
"
```

---

## 📋 Récapitulatif des commandes clés

```bash
# 1. Détecter les ports USB
ls -la /dev/tty* | grep USB
lsusb

# 2. Identifier le bon port (débrancher/rebrancher)
sudo dmesg -w

# 3. Vérifier les permissions
ls -l /dev/ttyUSB0
sudo usermod -aG dialout $USER

# 4. Créer un nom persistant
sudo nano /etc/udev/rules.d/99-lcus-relay.rules
# → Ajouter la règle udev
sudo udevadm control --reload-rules
sudo udevadm trigger

# 5. Tester
python3 test_lcus.py

# 6. Vérifier dans Docker (si applicable)
docker exec homeassistant ls -l /dev/lcus_relay
```

---

## 🆘 Dépannage

### Problème 1 : Aucun /dev/ttyUSB* détecté

```bash
# Vérifier que le module USB est bien détecté par le système
lsusb
# Si le module n'apparaît pas → problème matériel ou USB

# Vérifier les modules kernel
lsmod | grep -E 'ch341|ftdi|cp210|pl2303'
# Si vide, charger le module:
sudo modprobe ch341  # ou ftdi_sio, cp210x, pl2303
```

### Problème 2 : Permission denied

```bash
# Vérifier le groupe
ls -l /dev/ttyUSB0
# Si groupe "dialout", ajouter l'utilisateur:
sudo usermod -aG dialout $USER
# Se déconnecter et reconnecter

# Solution temporaire:
sudo chmod 666 /dev/ttyUSB0
```

### Problème 3 : Port change au redémarrage

```bash
# Créer une règle udev (voir Étape 5)
# Le lien symbolique /dev/lcus_relay restera stable
```

### Problème 4 : Module non accessible dans Docker

```bash
# Vérifier le docker-compose.yml
grep -A 5 "devices:" docker-compose.yml

# Doit contenir:
# devices:
#   - /dev/ttyUSB0:/dev/ttyUSB0
#   # OU
#   - /dev/lcus_relay:/dev/lcus_relay

# Redéployer si modifié:
docker-compose up -d --force-recreate
```

---

## 📚 Fichiers de référence

- **Configuration Docker** : [docker-compose.yaml.example](docker-compose.yaml.example)
- **Guide Docker complet** : [DOCKER_SETUP.md](DOCKER_SETUP.md)
- **Configuration USB** : [CONFIGURATION_USB.md](CONFIGURATION_USB.md)

---

## ✅ Checklist finale

- [ ] Connexion SSH au serveur Linux établie
- [ ] Port USB détecté (`/dev/ttyUSB0` ou similaire)
- [ ] Permissions configurées (groupe `dialout`)
- [ ] Nom persistant créé (`/dev/lcus_relay`) - optionnel mais recommandé
- [ ] Test Python réussi
- [ ] Docker mapping configuré (si applicable)
- [ ] Test depuis le conteneur réussi (si applicable)

Une fois toutes ces étapes validées, votre module LCUS est prêt pour l'intégration Home Assistant ! 🎉
