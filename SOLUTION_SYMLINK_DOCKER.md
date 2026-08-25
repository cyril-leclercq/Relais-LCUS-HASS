# 🔧 Solution simple : /dev/serial/by-id/

## 🎯 Problème résolu

- Le port USB change de nom : `ttyUSB0` → `ttyUSB1`
- Besoin d'un nom stable sans créer de règles udev personnalisées

---

## ✅ SOLUTION SIMPLE : Utiliser /dev/serial/by-id/

Linux crée **automatiquement** des liens symboliques stables dans `/dev/serial/by-id/`.

### 1️⃣ Trouver votre device (sur l'HÔTE)

```bash
ls -l /dev/serial/by-id/

# Résultat exemple:
# usb-1a86_USB_Serial-if00-port0 -> ../../ttyUSB1
```

### 2️⃣ Configuration docker-compose.yml

```yaml
services:
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:2026.4.4
    privileged: true
    
    devices:
      # Docker crée /dev/lcus_relay dans le conteneur
      - /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0:/dev/lcus_relay
```

### 3️⃣ Redémarrer le conteneur

```bash
docker-compose down && docker-compose up -d
```

### 4️⃣ Vérifier

```bash
# Le device doit être visible dans le conteneur
docker exec homeassistant ls -l /dev/lcus_relay

# Tester la connexion
docker exec homeassistant python3 -c "
import serial
s = serial.Serial('/dev/lcus_relay', 9600, timeout=1)
print('✓ Connexion OK!')
s.close()
"
```

---

## 🔄 Avantages

✅ **Automatique** : `/dev/serial/by-id/` créé par le système  
✅ **Stable** : Même si le port change (ttyUSB0 → ttyUSB1)  
✅ **Simple** : Aucune règle udev personnalisée requise  
✅ **Propre** : Docker crée `/dev/lcus_relay` directement dans le conteneur  

---

## 📋 Pourquoi ça fonctionne ?

`/dev/serial/by-id/` contient des liens symboliques créés automatiquement par `udev` basés sur :
- Vendor ID (idVendor)
- Product ID (idProduct)
- Numéro de série (si disponible)

Docker peut **mapper directement** ces liens et les créer dans le conteneur sous le nom de votre choix (`/dev/lcus_relay`).

---

## ✅ Configuration complète

```yaml
services:
  homeassistant:
    image: ghcr.io/home-assistant/home-assistant:2026.4.4
    container_name: homeassistant
    restart: unless-stopped
    privileged: true
    network_mode: host
    
    volumes:
      - /opt/docker/hass/config:/config
      - /etc/localtime:/etc/localtime:ro
    
    devices:
      # Remplacer par votre ID trouvé avec: ls -l /dev/serial/by-id/
      - /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0:/dev/lcus_relay
```

**Dans Home Assistant** : Port USB = `/dev/lcus_relay` ✓

---

## 🎉 Résultat

```bash
# Sur l'HÔTE
cyril@odroid-m1s:~$ ls -l /dev/serial/by-id/
usb-1a86_USB_Serial-if00-port0 -> ../../ttyUSB1

# Dans le CONTENEUR
cyril@odroid-m1s:~$ docker exec homeassistant ls -l /dev/lcus_relay
crw-rw-rw- 1 root dialout 188, 1 Aug 25 19:45 /dev/lcus_relay

# Test connexion
cyril@odroid-m1s:~$ docker exec homeassistant python3 -c "import serial; s=serial.Serial('/dev/lcus_relay', 9600); print('✓ OK'); s.close()"
✓ OK
```

**Le port USB peut changer de ttyUSB0 → ttyUSB1, tout fonctionnera !** 🚀
