import serial, time

CANAL = {'montee': 1, 'descente': 2}
DUREE_MAX = 40  # secondes — mets une marge au-dessus de ta course réelle mesurée
USB = '/dev/tty.usbserial-1110'
#USB = '/dev/ttyUSB0'

port = serial.Serial(USB, 9600, timeout=1)


def relais(canal, etat):
    trame = bytes([0xA0, canal, 1 if etat else 0,
                    (0xA0 + canal + (1 if etat else 0)) & 0xFF])
    port.write(trame)

def stop_tout():
    relais(CANAL['montee'], False)
    relais(CANAL['descente'], False)

def bouger(direction, duree):
    stop_tout()          # coupe l'autre canal au cas où
    time.sleep(0.1)       # petite marge avant d'enchaîner
    try:
        relais(CANAL[direction], True)
        time.sleep(min(duree, DUREE_MAX))
    finally:
        relais(CANAL[direction], False)  # coupe toujours, même en cas d'erreur/Ctrl-C

def arreter():
    stop_tout()


bouger('descente', 10)