import socket
import threading
import sys

class ClienteChat:
    def __init__(self, host='localhost', puerto=5555):
        self.host = host
        self.puerto = puerto
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nombre = ""
        
    def recibir_mensajes(self):
        """Recibe mensajes del servidor continuamente"""
        while True:
            try:
                mensaje = self.cliente.recv(1024).decode('utf-8')
                if mensaje:
                    print(f"\n{mensaje}")
                    print(f"{self.nombre}> ", end='', flush=True)
                else:
                    break
            except:
                print("\n[ERROR] Conexión perdida con el servidor")
                self.cliente.close()
                break
    
    def enviar_mensajes(self):
        """Envía mensajes al servidor"""
        while True:
            try:
                mensaje = input(f"{self.nombre}> ")
                if mensaje.lower() == '/salir':
                    print("Saliendo del chat...")
                    self.cliente.close()
                    sys.exit(0)
                elif mensaje.strip():
                    self.cliente.send(mensaje.encode('utf-8'))
            except:
                break
    
    def conectar(self):
        """Conecta al servidor"""
        try:
            self.cliente.connect((self.host, self.puerto))
            
            # Enviar nombre de usuario
            self.nombre = input("Ingresa tu nombre: ")
            self.cliente.send(self.nombre.encode('utf-8'))
            
            print(f"\n¡Conectado al chat! Escribe '/salir' para desconectarte\n")
            
            # Thread para recibir mensajes
            thread_recibir = threading.Thread(target=self.recibir_mensajes)
            thread_recibir.daemon = True
            thread_recibir.start()
            
            # Enviar mensajes (thread principal)
            self.enviar_mensajes()
            
        except Exception as e:
            print(f"[ERROR] No se pudo conectar al servidor: {e}")

if __name__ == "__main__":
    cliente = ClienteChat()
    cliente.conectar()
    