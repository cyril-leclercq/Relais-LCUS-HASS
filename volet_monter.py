#!/usr/bin/env python3
"""Commande pour monter le volet roulant"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from relais import bouger

if __name__ == '__main__':
    # Durée par défaut ou passée en argument
    duree = float(sys.argv[1]) if len(sys.argv) > 1 else 30
    bouger('montee', duree)
    print(f"Volet monté pendant {duree}s")
