import pygame
from game import Game
from puntajes import cargar_puntajes

# Constantes
ANCHO, ALTO = 800, 600
FPS = 60

# Colores
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_AZUL = (0, 0, 255)
COLOR_VERDE = (0, 200, 0)
COLOR_ROJO = (200, 0, 0)

class Menu:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Batalla Naval - Menú")

        # Cargar fondo y sonido
        try:
            self.fondo = pygame.image.load("assets/fondo.jpg")
            self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
        except pygame.error as e:
            print(f"No se pudo cargar la imagen de fondo: {e}")
            self.fondo = None

        try:
            pygame.mixer.music.load("assets/sonido_fondo.wav")
            pygame.mixer.music.play(-1)
            self.sonido_activado = True
        except pygame.error as e:
            print(f"No se pudo cargar el sonido: {e}")
            self.sonido_activado = False

        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("consolas", 30)
        self.fuente_pequena = pygame.font.SysFont("consolas", 24)

        self.estado = "menu_principal"
        self.dificultad = "facil"

        # Botones menú principal
        self.botones_menu = {
            "nivel": pygame.Rect(300, 150, 200, 50),
            "jugar": pygame.Rect(300, 230, 200, 50),
            "puntajes": pygame.Rect(300, 310, 200, 50),
            "sonido": pygame.Rect(300, 390, 200, 50),  # botón nuevo
            "salir": pygame.Rect(300, 470, 200, 50),
        }

        self.botones_niveles = {
            "facil": pygame.Rect(250, 200, 120, 50),
            "medio": pygame.Rect(440, 200, 120, 50),
            "dificil": pygame.Rect(345, 270, 120, 50),
            "volver": pygame.Rect(320, 350, 160, 50),
        }

        self.boton_volver_puntajes = pygame.Rect(320, 500, 160, 50)

    def dibujar_texto_centrado(self, texto, y, fuente, color=COLOR_BLANCO):
        superficie = fuente.render(texto, True, color)
        x = (ANCHO - superficie.get_width()) // 2
        self.pantalla.blit(superficie, (x, y))

    def dibujar_boton(self, rect, texto, color_fondo=COLOR_AZUL, color_texto=COLOR_BLANCO):
        pygame.draw.rect(self.pantalla, color_fondo, rect)
        texto_surf = self.fuente_pequena.render(texto, True, color_texto)
        x = rect.x + (rect.width - texto_surf.get_width()) // 2
        y = rect.y + (rect.height - texto_surf.get_height()) // 2
        self.pantalla.blit(texto_surf, (x, y))

    def manejar_eventos(self, evento):
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos = evento.pos
            if self.estado == "menu_principal":
                if self.botones_menu["nivel"].collidepoint(pos):
                    self.estado = "elegir_nivel"
                elif self.botones_menu["jugar"].collidepoint(pos):
                    juego = Game(self.dificultad)
                    juego.run()
                    self.estado = "menu_principal"
                elif self.botones_menu["puntajes"].collidepoint(pos):
                    self.estado = "ver_puntajes"
                elif self.botones_menu["sonido"].collidepoint(pos):
                    # Alternar sonido
                    if self.sonido_activado:
                        pygame.mixer.music.pause()
                        self.sonido_activado = False
                    else:
                        pygame.mixer.music.unpause()
                        self.sonido_activado = True
                elif self.botones_menu["salir"].collidepoint(pos):
                    pygame.quit()
                    exit()

            elif self.estado == "elegir_nivel":
                if self.botones_niveles["facil"].collidepoint(pos):
                    self.dificultad = "facil"
                elif self.botones_niveles["medio"].collidepoint(pos):
                    self.dificultad = "medio"
                elif self.botones_niveles["dificil"].collidepoint(pos):
                    self.dificultad = "dificil"
                elif self.botones_niveles["volver"].collidepoint(pos):
                    self.estado = "menu_principal"

            elif self.estado == "ver_puntajes":
                if self.boton_volver_puntajes.collidepoint(pos):
                    self.estado = "menu_principal"

    def dibujar_menu_principal(self):
        if self.fondo:
            self.pantalla.blit(self.fondo, (0, 0))
        else:
            self.pantalla.fill(COLOR_NEGRO)

        self.dibujar_texto_centrado("BATALLA NAVAL", 50, self.fuente, COLOR_VERDE)

        for clave, rect in self.botones_menu.items():
            texto = clave.capitalize()
            # Para el botón sonido, mostrar estado
            if clave == "sonido":
                texto = f"Sonido: {'ON' if self.sonido_activado else 'OFF'}"
            self.dibujar_boton(rect, texto)

        texto_dificultad = f"Dificultad actual: {self.dificultad.capitalize()}"
        texto_surf = self.fuente_pequena.render(texto_dificultad, True, COLOR_BLANCO)
        self.pantalla.blit(texto_surf, (20, 560))

    def dibujar_elegir_nivel(self):
        self.pantalla.fill(COLOR_NEGRO)
        self.dibujar_texto_centrado("Elegir Nivel de Dificultad", 100, self.fuente, COLOR_VERDE)

        for clave, rect in self.botones_niveles.items():
            color = COLOR_AZUL
            if clave == self.dificultad:
                color = COLOR_VERDE
            texto = clave.capitalize()
            if clave == "volver":
                texto = "Volver"
            self.dibujar_boton(rect, texto, color)

    def dibujar_ver_puntajes(self):
        self.pantalla.fill(COLOR_NEGRO)
        self.dibujar_texto_centrado("TOP 3 PUNTAJES", 50, self.fuente, COLOR_VERDE)

        puntajes = cargar_puntajes()
        puntajes_ordenados = sorted(puntajes, key=lambda x: x[1], reverse=True)[:3]

        y = 150
        for i, (nick, puntaje) in enumerate(puntajes_ordenados, 1):
            texto = f"{i}. {nick}: {puntaje}"
            texto_surf = self.fuente_pequena.render(texto, True, COLOR_BLANCO)
            self.pantalla.blit(texto_surf, (ANCHO // 2 - texto_surf.get_width() // 2, y))
            y += 50

        self.dibujar_boton(self.boton_volver_puntajes, "Volver", COLOR_ROJO)

    def run(self):
        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                self.manejar_eventos(evento)

            if self.estado == "menu_principal":
                self.dibujar_menu_principal()
            elif self.estado == "elegir_nivel":
                self.dibujar_elegir_nivel()
            elif self.estado == "ver_puntajes":
                self.dibujar_ver_puntajes()

            pygame.display.flip()
            self.reloj.tick(FPS)

if __name__ == "__main__":
    menu = Menu()
    menu.run()

