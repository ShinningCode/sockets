import pygame as py
import socket as suck
import random as rnd
from pygame.locals import QUIT

#background
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
        self.ancho, self.alto = 20, 20  # Ajusta las dimensiones según lo que desees

         # Escala la imagen a las nuevas dimensiones
        self.imagen = py.transform.scale(self.imagen, (self.ancho, self.alto))

        # Posición de la Pelota
        random = rnd.randint(0, VENTANA_HORI - self.ancho) 
        self.x = VENTANA_HORI / random - self.ancho / random  # Valor aleatorio dentro del ancho de la ventana
        self.y = VENTANA_VERT / random - self.alto / random   # Valor aleatorio dentro del alto de la ventana

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

def main():
    py.init()

    ventana = py.display.set_mode((VENTANA_HORI, VENTANA_VERT))
    py.display.set_caption("Ping Pong")
    pelota = Pong_ball("pelota-pong.png")

    cliente_socket = suck.socket(suck.AF_INET, suck.SOCK_STREAM)
    cliente_socket.connect(('localhost', 12345))
    
    jugando = True
    while jugando:
        pelota.mover()
        pelota.rebotar()

        ventana.fill(NEGRO)
        ventana.blit(pelota.imagen, (pelota.x, pelota.y))

        for event in py.event.get():
            if event.type == QUIT:
                jugando = False

        py.display.flip()
        py.time.Clock().tick(FPS)
        
    
    datos = pelota.reiniciar()

    if datos != 0:
        cliente_socket.send(datos.encode())
    # datos = "Datos del juego"
    # cliente_socket.send(f"{pelota.dir_x,pelota.dir_y}".encode())
    
    cliente_socket.close()

    py.quit()


if __name__ == "__main__":
    main()

