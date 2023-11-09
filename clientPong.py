import pygame as py
import socket as suck
from pygame.locals import QUIT

#background
VENTANA_HORI = 1350 
VENTANA_VERT = 700 
FPS = 60
NEGRO = (0, 0, 0) 

def main():
    py.init()

    ventana = py.display.set_mode((VENTANA_HORI, VENTANA_VERT))
    py.display.set_caption("Ping Pong")

    cliente_socket = suck.socket(suck.AF_INET, suck.SOCK_STREAM)
    cliente_socket.connect(('localhost', 12345))
    
    jugando = True
    while jugando:
        ventana.fill(NEGRO)

        for event in py.event.get():
            if event.type == QUIT:
                jugando = False

        py.display.flip()
        py.time.Clock().tick(FPS)
    
    datos = "Datos del juego"
    cliente_socket.send(datos.encode())

    cliente_socket.close()

    py.quit()


if __name__ == "__main__":
    main()

