import random
from config import TAMANIO_POR_DIFICULTAD, NAVES_POR_DIFICULTAD

def generar_tablero(dificultad):
    dificultad = dificultad.lower().strip()
    if dificultad not in TAMANIO_POR_DIFICULTAD:
        raise ValueError(f"Dificultad desconocida: {dificultad}")

    tam = TAMANIO_POR_DIFICULTAD[dificultad]
    tablero = [[0 for _ in range(tam)] for _ in range(tam)]
    naves_por_tipo = NAVES_POR_DIFICULTAD[dificultad]

    id_nave = 1

    for largo_nave, cantidad in naves_por_tipo.items():
        for _ in range(cantidad):
            colocado = False
            intentos = 0
            while not colocado and intentos < 1000:
                orientacion = random.choice(["horizontal", "vertical"])
                if orientacion == "horizontal":
                    fila = random.randint(0, tam - 1)
                    col = random.randint(0, tam - largo_nave)
                    if puede_colocar(tablero, fila, col, largo_nave, orientacion):
                        for i in range(largo_nave):
                            tablero[fila][col + i] = id_nave
                        colocado = True
                else:
                    fila = random.randint(0, tam - largo_nave)
                    col = random.randint(0, tam - 1)
                    if puede_colocar(tablero, fila, col, largo_nave, orientacion):
                        for i in range(largo_nave):
                            tablero[fila + i][col] = id_nave
                        colocado = True
                intentos += 1
            if colocado:
                id_nave += 1
            else:
                print(f"No se pudo colocar nave de largo {largo_nave}")
    return tablero

def puede_colocar(tablero, fila, col, largo, orientacion):
    tam = len(tablero)
    for i in range(largo):
        f = fila + i if orientacion == "vertical" else fila
        c = col + i if orientacion == "horizontal" else col
        if tablero[f][c] != 0:
            return False
    return True
