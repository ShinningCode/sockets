import pygame as py
import socket as suck
import random as rnd
from pygame.locals import QUIT

# background
VENTANA_HORI = 1350
VENTANA_VERT = 700
FPS = 60
NEGRO = (0, 0, 0)

class Pong_ball:
    def __init__(self, fichero_imagen):
        # --- Atributos de la Clase ---

        # Imagen de la Pelota
        self.imagen = py.image.load(fichero_imagen).convert_alpha()

        # Nuevas dimensiones de la Pelota
        self.ancho, self.alto = 20, 20  # Ajusta las dimensiones
        # Tamaño de pelotita
        self.imagen = py.transform.scale(self.imagen, (self.ancho, self.alto))

        # Posición de la Pelota
        random = rnd.randint(0, VENTANA_HORI - self.ancho)
        self.x = VENTANA_HORI / random - self.ancho / random  # Valor aleatorio dentro del ancho de la ventana
        self.y = VENTANA_VERT / random - self.alto / random  # Valor aleatorio dentro del alto de la ventana

        # Dirección de movimiento de la Pelota
        self.dir_x = rnd.choice([-5, 5])
        self.dir_y = rnd.choice([-5, 5])

    def mover(self):
        self.x += self.dir_x
        self.y += self.dir_y

    def rebotar(self):
        if self.y <= 0:
            self.dir_y = -self.dir_y
        elif self.y + self.alto >= VENTANA_VERT:
            self.reiniciar()
        elif self.x <= -self.ancho or self.x >= VENTANA_HORI:
            self.dir_x = -self.dir_x

    def reiniciar(self):
        self.x = rnd.randint(0, VENTANA_HORI - self.ancho)
        self.y = rnd.randint(0, VENTANA_VERT - self.alto)
        self.dir_x = -self.dir_x
        self.dir_y = rnd.choice([-5, 5])
        return f"{self.x}\t|\t{self.y}"  # Devuelve la posición al reiniciar

class Pong_paleta:
    def __init__(self):
        # Imagen de la paleta
        self.imagen = py.image.load("raqueta.png").convert_alpha()
        self.ancho, self.alto = 100, 60  # Ajusta las dimensiones de la paleta
        self.imagen = py.transform.scale(self.imagen, (self.ancho, self.alto))
        self.x = VENTANA_HORI // 2 - self.ancho // 2  # Centrar la paleta horizontalmente
        self.y = VENTANA_VERT - self.alto  # Colocar la paleta en la parte inferior

    def golpear(self, pelota):
        if (
            pelota.x < self.x + self.ancho
            and pelota.x > self.x
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x + self.ancho
    
    def golpear_ia(self, pelota):
        if (
            pelota.x + pelota.ancho > self.x
            and pelota.x < self.x + self.ancho
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x - pelota.ancho
    
def main():
    py.init()

    ventana = py.display.set_mode((VENTANA_HORI, VENTANA_VERT))
    py.display.set_caption("Ping Pong")
    pelota = Pong_ball("pelota-pong.png")
    paleta = Pong_paleta()

    cliente_socket = suck.socket(suck.AF_INET, suck.SOCK_STREAM)
    cliente_socket.connect(('localhost', 12345))

    jugando = True
    while jugando:
        for event in py.event.get():
            if event.type == QUIT:
                jugando = False

        ventana.fill(NEGRO)
        ventana.blit(pelota.imagen, (pelota.x, pelota.y))
        ventana.blit(paleta.imagen, (paleta.x, paleta.y))  # Dibuja la paleta

        pelota.mover()
        pelota.rebotar()
        paleta.golpear(pelota)
        paleta.golpear_ia(pelota)

        py.display.flip()
        py.time.Clock().tick(FPS)

    datos = pelota.reiniciar()

    cliente_socket.send(datos.encode())
    # datos = "Datos del juego"
    # cliente_socket.send(f"{pelota.dir_x,pelota.dir_y}".encode())

    cliente_socket.close()

    py.quit()

if __name__ == "__main__":
    main()
