# Configuraciones generales

ANCHO = 800
ALTO = 600
FPS = 60

COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_VERDE = (0, 200, 0)
COLOR_AZUL = (0, 0, 255)

TAMANIO_POR_DIFICULTAD = {
    "facil": 10,
    "medio": 20,
    "dificil": 40
}

NAVES_POR_DIFICULTAD = {
    "facil": {
        1: 4,  # Submarinos
        2: 3,  # Destructores
        3: 2,  # Cruceros
        4: 1   # Acorazado
    },
    "medio": {
        1: 8,
        2: 6,
        3: 4,
        4: 2
    },
    "dificil": {
        1: 12,
        2: 9,
        3: 6,
        4: 3
    }
}
