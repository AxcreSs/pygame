import pygame
from config import *
from tablero import generar_tablero
from puntajes import guardar_puntaje

AREA_JUEGO = 550

class Game:
    def __init__(self, dificultad="facil"):
        self.dificultad = dificultad.lower().strip()
        self.fuente = pygame.font.SysFont("consolas", 24)
        self.ancho_pantalla = ANCHO
        self.alto_pantalla = ALTO
        self.pantalla = pygame.display.set_mode((self.ancho_pantalla, self.alto_pantalla))
        pygame.display.set_caption("Batalla Naval - Jugando")
        self.reloj = pygame.time.Clock()
        self.boton_reiniciar = pygame.Rect(650, 570, 120, 25)
        self.reiniciar_juego()

    def reiniciar_juego(self):
        self.tablero = generar_tablero(self.dificultad)
        self.tamano = len(self.tablero)
        self.TAM_CASILLA = AREA_JUEGO // self.tamano
        self.disparos = [[False for _ in range(self.tamano)] for _ in range(self.tamano)]
        self.puntaje = 0

    def procesar_disparo(self, fila, col):
        if self.disparos[fila][col]:
            return
        self.disparos[fila][col] = True
        valor = self.tablero[fila][col]
        if valor == 0:
            self.puntaje -= 1
        else:
            self.puntaje += 5
            if self.nave_hundida(valor):
                partes = sum(row.count(valor) for row in self.tablero)
                self.puntaje += 10 * partes

    def nave_hundida(self, id_nave):
        for f in range(self.tamano):
            for c in range(self.tamano):
                if self.tablero[f][c] == id_nave and not self.disparos[f][c]:
                    return False
        return True

    def dibujar_tablero(self):
        for fila in range(self.tamano):
            for col in range(self.tamano):
                x = col * self.TAM_CASILLA + 25
                y = fila * self.TAM_CASILLA + 25
                rect = pygame.Rect(x, y, self.TAM_CASILLA, self.TAM_CASILLA)
                pygame.draw.rect(self.pantalla, COLOR_NEGRO, rect, 1)

                if self.disparos[fila][col]:
                    valor = self.tablero[fila][col]
                    color = COLOR_VERDE if valor > 0 else COLOR_AZUL
                    pygame.draw.rect(self.pantalla, color, rect)

    def dibujar_puntaje(self):
        texto = self.fuente.render(f"Puntaje: {self.puntaje:04}", True, COLOR_BLANCO)
        self.pantalla.blit(texto, (20, 570))

    def dibujar_boton_reiniciar(self):
        pygame.draw.rect(self.pantalla, (0, 0, 128), self.boton_reiniciar)
        texto = self.fuente.render("Reiniciar", True, COLOR_BLANCO)
        self.pantalla.blit(texto, (
            self.boton_reiniciar.x + (self.boton_reiniciar.width - texto.get_width()) // 2,
            self.boton_reiniciar.y + (self.boton_reiniciar.height - texto.get_height()) // 2
        ))

    def juego_terminado(self):
        for f in range(self.tamano):
            for c in range(self.tamano):
                if self.tablero[f][c] > 0 and not self.disparos[f][c]:
                    return False
        return True

    def pedir_nick(self):
        pygame.font.init()
        fuente = pygame.font.SysFont("arial", 32)
        input_text = ""
        activo = True
        clock = pygame.time.Clock()

        while activo:
            self.pantalla.fill((0, 0, 0))
            texto_instr = fuente.render("Ingrese su Nick:", True, (255, 255, 255))
            self.pantalla.blit(texto_instr, (50, 100))
            texto_input = fuente.render(input_text, True, (255, 255, 255))
            self.pantalla.blit(texto_input, (50, 150))
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    activo = False
                    pygame.quit()
                    exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN and len(input_text) > 0:
                        activo = False
                    elif evento.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if len(input_text) < 10 and evento.unicode.isalnum():
                            input_text += evento.unicode
            clock.tick(30)

        return input_text

    def run(self):
        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.boton_reiniciar.collidepoint(evento.pos):
                        self.reiniciar_juego()
                    else:
                        x, y = evento.pos
                        fila = (y - 25) // self.TAM_CASILLA
                        col = (x - 25) // self.TAM_CASILLA
                        if 0 <= fila < self.tamano and 0 <= col < self.tamano:
                            self.procesar_disparo(fila, col)

            self.pantalla.fill((30, 30, 30))
            self.dibujar_tablero()
            self.dibujar_puntaje()
            self.dibujar_boton_reiniciar()
            pygame.display.flip()
            self.reloj.tick(FPS)

            if self.juego_terminado():
                corriendo = False

        nick = self.pedir_nick()
        if nick:
            guardar_puntaje(nick, self.puntaje)
