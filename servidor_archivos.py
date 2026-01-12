import socket
import os
import threading

class ServidorArchivos:
    def __init__(self, host='0.0.0.0', puerto=6666):
        self.host = host
        self.puerto = puerto
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.carpeta_recepcion = "archivos_recibidos"
        
        # Crear carpeta para archivos recibidos
        if not os.path.exists(self.carpeta_recepcion):
            os.makedirs(self.carpeta_recepcion)
            
    def iniciar(self):
        """Inicia el servidor de archivos"""
        try:
            self.servidor.bind((self.host, self.puerto))
            self.servidor.listen(5)
            print(f"[SERVIDOR] Escuchando en {self.host}:{self.puerto}")
            print(f"[SERVIDOR] Archivos se guardarán en: {self.carpeta_recepcion}/")
            print("-" * 60)
            
            while True:
                cliente_socket, direccion = self.servidor.accept()
                print(f"[NUEVA CONEXIÓN] {direccion[0]}:{direccion[1]}")
                
                # Crear hilo para manejar el cliente
                hilo_cliente = threading.Thread(
                    target=self.manejar_cliente,
                    args=(cliente_socket, direccion),
                    daemon=True
                )
                hilo_cliente.start()
                
        except KeyboardInterrupt:
            print("\n[SERVIDOR] Detenido por el usuario")
        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            self.servidor.close()
            
    def manejar_cliente(self, cliente_socket, direccion):
        """Maneja la conexión de un cliente"""
        try:
            # Recibir operación (enviar o recibir)
            operacion = cliente_socket.recv(1024).decode('utf-8')
            
            if operacion == "ENVIAR":
                self.recibir_archivo(cliente_socket, direccion)
            elif operacion == "RECIBIR":
                self.enviar_archivo(cliente_socket, direccion)
            elif operacion == "LISTAR":
                self.listar_archivos(cliente_socket, direccion)
            else:
                print(f"[{direccion[0]}] Operación desconocida: {operacion}")
                
        except Exception as e:
            print(f"[ERROR] {direccion[0]}: {e}")
        finally:
            cliente_socket.close()
            print(f"[DESCONEXIÓN] {direccion[0]}:{direccion[1]}")
            
    def recibir_archivo(self, cliente_socket, direccion):
        """Recibe un archivo del cliente"""
        try:
            # Recibir nombre del archivo
            nombre_archivo = cliente_socket.recv(1024).decode('utf-8')
            cliente_socket.send(b"OK")
            
            # Recibir tamaño del archivo
            tamano = int(cliente_socket.recv(1024).decode('utf-8'))
            cliente_socket.send(b"OK")
            
            print(f"[{direccion[0]}] Recibiendo: {nombre_archivo} ({tamano} bytes)")
            
            # Recibir datos del archivo
            ruta_completa = os.path.join(self.carpeta_recepcion, nombre_archivo)
            bytes_recibidos = 0
            
            with open(ruta_completa, 'wb') as archivo:
                while bytes_recibidos < tamano:
                    datos = cliente_socket.recv(4096)
                    if not datos:
                        break
                    archivo.write(datos)
                    bytes_recibidos += len(datos)
                    
                    # Mostrar progreso
                    porcentaje = (bytes_recibidos / tamano) * 100
                    print(f"[{direccion[0]}] Progreso: {porcentaje:.1f}%", end='\r')
            
            print(f"\n[{direccion[0]}] ✓ Archivo guardado: {ruta_completa}")
            cliente_socket.send(b"COMPLETO")
            
        except Exception as e:
            print(f"\n[ERROR] Recibiendo archivo: {e}")
            cliente_socket.send(b"ERROR")
            
    def enviar_archivo(self, cliente_socket, direccion):
        """Envía un archivo al cliente"""
        try:
            # Recibir nombre del archivo solicitado
            nombre_archivo = cliente_socket.recv(1024).decode('utf-8')
            ruta_completa = os.path.join(self.carpeta_recepcion, nombre_archivo)
            
            # Verificar si el archivo existe
            if not os.path.exists(ruta_completa):
                cliente_socket.send(b"NO_EXISTE")
                print(f"[{direccion[0]}] Archivo no encontrado: {nombre_archivo}")
                return
            
            # Enviar confirmación y tamaño
            tamano = os.path.getsize(ruta_completa)
            cliente_socket.send(b"EXISTE")
            cliente_socket.recv(1024)  # Esperar confirmación
            
            cliente_socket.send(str(tamano).encode('utf-8'))
            cliente_socket.recv(1024)  # Esperar confirmación
            
            print(f"[{direccion[0]}] Enviando: {nombre_archivo} ({tamano} bytes)")
            
            # Enviar archivo
            bytes_enviados = 0
            with open(ruta_completa, 'rb') as archivo:
                while True:
                    datos = archivo.read(4096)
                    if not datos:
                        break
                    cliente_socket.send(datos)
                    bytes_enviados += len(datos)
                    
                    # Mostrar progreso
                    porcentaje = (bytes_enviados / tamano) * 100
                    print(f"[{direccion[0]}] Progreso: {porcentaje:.1f}%", end='\r')
            
            print(f"\n[{direccion[0]}] ✓ Archivo enviado correctamente")
            
        except Exception as e:
            print(f"\n[ERROR] Enviando archivo: {e}")
            
    def listar_archivos(self, cliente_socket, direccion):
        """Envía la lista de archivos disponibles al cliente"""
        try:
            archivos = os.listdir(self.carpeta_recepcion)
            
            if not archivos:
                cliente_socket.send(b"VACIO")
            else:
                lista = "\n".join(archivos)
                cliente_socket.send(lista.encode('utf-8'))
                
            print(f"[{direccion[0]}] Listado de archivos enviado ({len(archivos)} archivos)")
            
        except Exception as e:
            print(f"[ERROR] Listando archivos: {e}")
            cliente_socket.send(b"ERROR")

if __name__ == "__main__":
    servidor = ServidorArchivos(host='0.0.0.0', puerto=6666)
    servidor.iniciar()