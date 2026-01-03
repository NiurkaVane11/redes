import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('localhost', 5555))

mensaje = "Hola desde el cliente!"
cliente.send(mensaje.encode())

respuesta = cliente.recv(1024).decode()
print(f"Respuesta del servidor: {respuesta}")

cliente.close()