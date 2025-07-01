import pygame

def reproducir_musica():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sonido_fondo.wav")
        pygame.mixer.music.play(-1)  # bucle infinito
        pygame.mixer.music.set_volume(0.3)
    except pygame.error as e:
        print("Error al reproducir música:", e)

def detener_musica():
    pygame.mixer.music.stop()