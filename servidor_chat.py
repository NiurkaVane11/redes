
import socket
import threading

class ServidorChat:
    def __init__(self, host='localhost', puerto=5555):
        self.host = host
        self.puerto = puerto
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientes = []
        self.nombres = {}
        
    def broadcast(self, mensaje, remitente=None):
        """Envía mensaje a todos los clientes excepto al remitente"""
        for cliente in self.clientes:
            if cliente != remitente:
                try:
                    cliente.send(mensaje)
                except:
                    self.clientes.remove(cliente)
    
    def manejar_cliente(self, cliente):
        """Maneja la comunicación con cada cliente"""
        try:
            # Recibir nombre del usuario
            nombre = cliente.recv(1024).decode('utf-8')
            self.nombres[cliente] = nombre
            
            bienvenida = f"{nombre} se ha unido al chat!".encode('utf-8')
            self.broadcast(bienvenida, cliente)
            print(f"[SERVIDOR] {nombre} conectado desde {cliente.getpeername()}")
            
            while True:
                mensaje = cliente.recv(1024)
                if mensaje:
                    texto = f"{nombre}: {mensaje.decode('utf-8')}"
                    print(f"[MENSAJE] {texto}")
                    self.broadcast(texto.encode('utf-8'), cliente)
                else:
                    break
                    
        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            if cliente in self.clientes:
                self.clientes.remove(cliente)
                nombre = self.nombres.get(cliente, "Usuario")
                despedida = f"{nombre} ha salido del chat.".encode('utf-8')
                self.broadcast(despedida)
                del self.nombres[cliente]
            cliente.close()
    
    def iniciar(self):
        """Inicia el servidor"""
        self.servidor.bind((self.host, self.puerto))
        self.servidor.listen()
        print(f"[SERVIDOR] Escuchando en {self.host}:{self.puerto}")
        
        while True:
            cliente, direccion = self.servidor.accept()
            self.clientes.append(cliente)
            
            # Crear thread para cada cliente
            thread = threading.Thread(target=self.manejar_cliente, args=(cliente,))
            thread.start()
            print(f"[CONEXIONES ACTIVAS] {threading.active_count() - 1}")

if __name__ == "__main__":
    servidor = ServidorChat()
    servidor.iniciar()