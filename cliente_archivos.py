import socket
import os

class ClienteArchivos:
    def __init__(self, host='127.0.0.1', puerto=6666):
        self.host = host
        self.puerto = puerto
        self.carpeta_descargas = "descargas"
        
        # Crear carpeta para descargas
        if not os.path.exists(self.carpeta_descargas):
            os.makedirs(self.carpeta_descargas)
            
    def conectar(self):
        """Crea una nueva conexión al servidor"""
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cliente.connect((self.host, self.puerto))
            return cliente
        except Exception as e:
            print(f"[ERROR] No se pudo conectar al servidor: {e}")
            return None
            
    def enviar_archivo(self, ruta_archivo):
        """Envía un archivo al servidor"""
        if not os.path.exists(ruta_archivo):
            print(f"[ERROR] Archivo no encontrado: {ruta_archivo}")
            return False
            
        cliente = self.conectar()
        if not cliente:
            return False
            
        try:
            # Enviar operación
            cliente.send(b"ENVIAR")
            
            # Enviar nombre del archivo
            nombre_archivo = os.path.basename(ruta_archivo)
            cliente.send(nombre_archivo.encode('utf-8'))
            cliente.recv(1024)  # Esperar confirmación
            
            # Enviar tamaño del archivo
            tamano = os.path.getsize(ruta_archivo)
            cliente.send(str(tamano).encode('utf-8'))
            cliente.recv(1024)  # Esperar confirmación
            
            print(f"[ENVIANDO] {nombre_archivo} ({tamano} bytes)")
            
            # Enviar archivo
            bytes_enviados = 0
            with open(ruta_archivo, 'rb') as archivo:
                while True:
                    datos = archivo.read(4096)
                    if not datos:
                        break
                    cliente.send(datos)
                    bytes_enviados += len(datos)
                    
                    # Mostrar progreso
                    porcentaje = (bytes_enviados / tamano) * 100
                    print(f"Progreso: {porcentaje:.1f}%", end='\r')
            
            # Esperar confirmación final
            respuesta = cliente.recv(1024).decode('utf-8')
            
            if respuesta == "COMPLETO":
                print(f"\n✓ Archivo enviado correctamente")
                return True
            else:
                print(f"\n✗ Error al enviar archivo")
                return False
                
        except Exception as e:
            print(f"\n[ERROR] {e}")
            return False
        finally:
            cliente.close()
            
    def recibir_archivo(self, nombre_archivo):
        """Descarga un archivo del servidor"""
        cliente = self.conectar()
        if not cliente:
            return False
            
        try:
            # Enviar operación
            cliente.send(b"RECIBIR")
            
            # Enviar nombre del archivo
            cliente.send(nombre_archivo.encode('utf-8'))
            
            # Verificar si existe
            respuesta = cliente.recv(1024).decode('utf-8')
            if respuesta == "NO_EXISTE":
                print(f"[ERROR] El archivo '{nombre_archivo}' no existe en el servidor")
                return False
            
            cliente.send(b"OK")
            
            # Recibir tamaño
            tamano = int(cliente.recv(1024).decode('utf-8'))
            cliente.send(b"OK")
            
            print(f"[DESCARGANDO] {nombre_archivo} ({tamano} bytes)")
            
            # Recibir archivo
            ruta_completa = os.path.join(self.carpeta_descargas, nombre_archivo)
            bytes_recibidos = 0
            
            with open(ruta_completa, 'wb') as archivo:
                while bytes_recibidos < tamano:
                    datos = cliente.recv(4096)
                    if not datos:
                        break
                    archivo.write(datos)
                    bytes_recibidos += len(datos)
                    
                    # Mostrar progreso
                    porcentaje = (bytes_recibidos / tamano) * 100
                    print(f"Progreso: {porcentaje:.1f}%", end='\r')
            
            print(f"\n✓ Archivo descargado: {ruta_completa}")
            return True
            
        except Exception as e:
            print(f"\n[ERROR] {e}")
            return False
        finally:
            cliente.close()
            
    def listar_archivos(self):
        """Obtiene la lista de archivos disponibles en el servidor"""
        cliente = self.conectar()
        if not cliente:
            return []
            
        try:
            # Enviar operación
            cliente.send(b"LISTAR")
            
            # Recibir lista
            respuesta = cliente.recv(4096).decode('utf-8')
            
            if respuesta == "VACIO":
                print("[INFO] No hay archivos en el servidor")
                return []
            elif respuesta == "ERROR":
                print("[ERROR] No se pudo obtener la lista")
                return []
            else:
                archivos = respuesta.split('\n')
                return archivos
                
        except Exception as e:
            print(f"[ERROR] {e}")
            return []
        finally:
            cliente.close()
            
    def menu(self):
        """Menú interactivo del cliente"""
        print("=" * 60)
        print("CLIENTE DE TRANSFERENCIA DE ARCHIVOS")
        print("=" * 60)
        
        while True:
            print("\n--- MENÚ ---")
            print("1. Enviar archivo al servidor")
            print("2. Descargar archivo del servidor")
            print("3. Listar archivos en el servidor")
            print("4. Salir")
            
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == "1":
                ruta = input("Ruta del archivo a enviar: ").strip()
                self.enviar_archivo(ruta)
                
            elif opcion == "2":
                # Primero mostrar archivos disponibles
                print("\n[ARCHIVOS DISPONIBLES]")
                archivos = self.listar_archivos()
                if archivos:
                    for i, archivo in enumerate(archivos, 1):
                        print(f"{i}. {archivo}")
                    nombre = input("\nNombre del archivo a descargar: ").strip()
                    self.recibir_archivo(nombre)
                    
            elif opcion == "3":
                print("\n[ARCHIVOS DISPONIBLES EN EL SERVIDOR]")
                archivos = self.listar_archivos()
                if archivos:
                    for i, archivo in enumerate(archivos, 1):
                        print(f"{i}. {archivo}")
                        
            elif opcion == "4":
                print("¡Hasta luego!")
                break
                
            else:
                print("Opción inválida")

if __name__ == "__main__":
    # Puedes cambiar el host y puerto según tu configuración
    cliente = ClienteArchivos(host='127.0.0.1', puerto=6666)
    cliente.menu()