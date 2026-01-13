import socket
import re

class ClienteHTTP:
    def __init__(self):
        self.puerto_default = 80
        
    def parsear_url(self, url):
        """Parsea una URL y extrae host, puerto y ruta"""
        # Remover http:// o https://
        url = re.sub(r'^https?://', '', url)
        
        # Extraer host, puerto y ruta
        if '/' in url:
            host_puerto, ruta = url.split('/', 1)
            ruta = '/' + ruta
        else:
            host_puerto = url
            ruta = '/'
            
        # Extraer puerto si existe
        if ':' in host_puerto:
            host, puerto = host_porto.split(':')
            puerto = int(puerto)
        else:
            host = host_puerto
            puerto = self.puerto_default
            
        return host, puerto, ruta
        
    def realizar_peticion(self, url, metodo='GET', mostrar_encabezados=False):
        """Realiza una petición HTTP"""
        try:
            # Parsear URL
            host, puerto, ruta = self.parsear_url(url)
            
            print(f"🌐 Conectando a {host}:{puerto}")
            print(f"📄 Solicitando: {ruta}")
            print("-" * 60)
            
            # Crear socket
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.settimeout(10)
            
            # Conectar
            cliente.connect((host, puerto))
            
            # Construir petición HTTP
            peticion = f"{metodo} {ruta} HTTP/1.1\r\n"
            peticion += f"Host: {host}\r\n"
            peticion += "User-Agent: ClienteHTTP-Python/1.0\r\n"
            peticion += "Connection: close\r\n"
            peticion += "\r\n"
            
            # Enviar petición
            cliente.send(peticion.encode('utf-8'))
            
            # Recibir respuesta
            respuesta = b""
            while True:
                datos = cliente.recv(4096)
                if not datos:
                    break
                respuesta += datos
                
            cliente.close()
            
            # Decodificar respuesta
            respuesta_str = respuesta.decode('utf-8', errors='ignore')
            
            # Separar encabezados y cuerpo
            if '\r\n\r\n' in respuesta_str:
                encabezados, cuerpo = respuesta_str.split('\r\n\r\n', 1)
            else:
                encabezados = respuesta_str
                cuerpo = ""
                
            # Extraer código de estado
            primera_linea = encabezados.split('\r\n')[0]
            codigo_estado = primera_linea.split()[1] if len(primera_linea.split()) > 1 else "???"
            
            print(f"✅ Respuesta: {primera_linea}")
            print(f"📊 Código: {codigo_estado}")
            print(f"📦 Tamaño: {len(cuerpo)} bytes")
            print("-" * 60)
            
            # Mostrar encabezados si se solicita
            if mostrar_encabezados:
                print("\n📋 ENCABEZADOS:")
                print(encabezados)
                print("-" * 60)
                
            # Mostrar cuerpo
            print("\n📄 CONTENIDO:")
            if len(cuerpo) > 500:
                print(cuerpo[:500])
                print(f"\n... ({len(cuerpo) - 500} bytes más)")
            else:
                print(cuerpo)
                
            return codigo_estado, encabezados, cuerpo
            
        except socket.timeout:
            print("❌ ERROR: Tiempo de espera agotado")
        except socket.gaierror:
            print("❌ ERROR: No se pudo resolver el nombre del host")
        except ConnectionRefusedError:
            print("❌ ERROR: Conexión rechazada (¿servidor corriendo?)")
        except Exception as e:
            print(f"❌ ERROR: {e}")
            
        return None, None, None
        
    def descargar_archivo(self, url, nombre_archivo):
        """Descarga un archivo desde una URL"""
        try:
            host, puerto, ruta = self.parsear_url(url)
            
            print(f"⬇️  Descargando: {url}")
            print(f"💾 Guardando en: {nombre_archivo}")
            
            # Crear socket
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.settimeout(30)
            cliente.connect((host, puerto))
            
            # Construir petición
            peticion = f"GET {ruta} HTTP/1.1\r\n"
            peticion += f"Host: {host}\r\n"
            peticion += "Connection: close\r\n"
            peticion += "\r\n"
            
            cliente.send(peticion.encode('utf-8'))
            
            # Recibir respuesta
            respuesta = b""
            while True:
                datos = cliente.recv(4096)
                if not datos:
                    break
                respuesta += datos
                
            cliente.close()
            
            # Separar encabezados y cuerpo
            separador = b'\r\n\r\n'
            if separador in respuesta:
                _, cuerpo = respuesta.split(separador, 1)
            else:
                cuerpo = respuesta
                
            # Guardar archivo
            with open(nombre_archivo, 'wb') as archivo:
                archivo.write(cuerpo)
                
            print(f"✅ Archivo descargado: {len(cuerpo)} bytes")
            return True
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
            
    def menu(self):
        """Menú interactivo"""
        print("=" * 70)
        print("🌐 CLIENTE HTTP - DÍA 5")
        print("=" * 70)
        
        while True:
            print("\n--- MENÚ ---")
            print("1. Realizar petición GET")
            print("2. Realizar petición con encabezados")
            print("3. Descargar archivo")
            print("4. Probar servidor local (localhost:8080)")
            print("5. Salir")
            
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == "1":
                url = input("URL: ").strip()
                if url:
                    self.realizar_peticion(url)
                    
            elif opcion == "2":
                url = input("URL: ").strip()
                if url:
                    self.realizar_peticion(url, mostrar_encabezados=True)
                    
            elif opcion == "3":
                url = input("URL del archivo: ").strip()
                nombre = input("Nombre para guardar: ").strip()
                if url and nombre:
                    self.descargar_archivo(url, nombre)
                    
            elif opcion == "4":
                print("\n🔍 Probando servidor local...")
                self.realizar_peticion("http://localhost:8080")
                
            elif opcion == "5":
                print("¡Hasta luego!")
                break
                
            else:
                print("❌ Opción inválida")

if __name__ == "__main__":
    cliente = ClienteHTTP()
    cliente.menu()