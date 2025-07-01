import os

RUTA_PUNTAJES = "data/puntajes.txt"

def guardar_puntaje(nick, puntaje):
    os.makedirs(os.path.dirname(RUTA_PUNTAJES), exist_ok=True)
    with open(RUTA_PUNTAJES, "a") as archivo:
        archivo.write(f"{nick},{puntaje}\n")

def cargar_puntajes():
    if not os.path.exists(RUTA_PUNTAJES):
        return []
    with open(RUTA_PUNTAJES, "r") as archivo:
        lineas = archivo.readlines()
    puntajes = []
    for linea in lineas:
        try:
            nick, punt = linea.strip().split(",")
            puntajes.append((nick, int(punt)))
        except:
            continue
    return sorted(puntajes, key=lambda x: x[1], reverse=True)