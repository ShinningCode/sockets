import socket

# Inicializar el socket
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_socket.bind(('localhost', 12345))
servidor_socket.listen(1)  # Un cliente

print("Esperando conexión del juego...")

cliente, direccion = servidor_socket.accept()
print(f"Conexión establecida con Pong en direccion: {direccion}")


while True:
    # Recibir datos del juego (por ejemplo, posición de la pelota)
    datos = cliente.recv(1024).decode()

    # Procesar datos, actualizar el juego y el puntaje
    # ...

cliente.close()
