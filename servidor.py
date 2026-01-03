import socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('localhost', 8080))
servidor.listen(5)
print("Servidor escuchando en el puerto 5555...")

conexion, direccion = servidor.accept()
print(f"Conexión establecida con {direccion}")
mensaje = conexion.recv(1024).decode('utf-8')


print(f"Mensaje recibido: {mensaje}")

respuesta = "Mensaje recibido correctamente"
conexion.send(respuesta.encode('utf-8'))
conexion.close()
servidor.close()











