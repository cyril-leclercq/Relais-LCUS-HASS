# Relais

Contrôle de relais via port série USB pour systèmes de mouvement (montée/descente).

## Prérequis

- Python 3
- pyserial

## Installation

```bash
pip install pyserial
```

## Utilisation

Le script contrôle un module de relais via USB pour gérer deux canaux :
- Canal 1 : montée
- Canal 2 : descente

Fonctions disponibles :
- `bouger(direction, duree)` : Active le relais dans la direction spécifiée pendant une durée donnée
- `arreter()` : Arrête tous les relais
- `stop_tout()` : Coupe tous les canaux

## Configuration

Modifier la variable `USB` dans le script selon votre système :
- macOS : `/dev/tty.usbserial-1110`
- Linux : `/dev/ttyUSB0`
