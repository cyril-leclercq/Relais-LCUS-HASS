#!/usr/bin/env python3
"""Commande pour arrêter le volet roulant"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from relais import arreter

if __name__ == '__main__':
    arreter()
    print("Volet arrêté")
