import socket

# Inicializar el socket
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_socket.bind(('localhost', 12345))
servidor_socket.listen(1)  # Un cliente

print("Esperando conexión del juego...")

cliente, direccion = servidor_socket.accept()
print(f"Conexion con Pong en direccion IP: {direccion}")

print("Posicion de Pelota:\n")
print("X\t|\tY\n")
while True:
    # Recibir datos del juego (por ejemplo, posición de la pelota)
    datos = cliente.recv(1024).decode()
    
    # dir_x = cliente.recv(1024).decode()
    # dir_y = cliente.recv(1024).decode()
    
    print(f"{datos}")

cliente.close()
