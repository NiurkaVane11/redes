import socket
import os
import mimetypes
from datetime import datetime

class ServidorHTTP:
    def __init__(self, host='0.0.0.0', puerto=8080):
        self.host = host
        self.puerto = puerto
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.directorio_web = "www"
        
        # Crear directorio web si no existe
        if not os.path.exists(self.directorio_web):
            os.makedirs(self.directorio_web)
            self.crear_pagina_ejemplo()
            
    def crear_pagina_ejemplo(self):
        """Crea una página HTML de ejemplo"""
        html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Servidor HTTP - Día 5</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 2.5em;
        }
        p {
            color: #555;
            line-height: 1.8;
            margin-bottom: 15px;
            font-size: 1.1em;
        }
        .info {
            background: #f0f4ff;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #667eea;
        }
        .info strong {
            color: #667eea;
        }
        .links {
            margin-top: 30px;
        }
        .links a {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 12px 25px;
            text-decoration: none;
            border-radius: 8px;
            margin: 5px;
            transition: all 0.3s;
        }
        .links a:hover {
            background: #764ba2;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .emoji {
            font-size: 3em;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">🚀</div>
        <h1>¡Servidor HTTP Funcionando!</h1>
        <p>Felicidades, has creado tu propio servidor HTTP desde cero usando Python y sockets.</p>
        
        <div class="info">
            <p><strong>📅 Día 5:</strong> Programación de Redes</p>
            <p><strong>🌐 Servidor:</strong> HTTP/1.1</p>
            <p><strong>⚡ Estado:</strong> Activo</p>
        </div>
        
        <p>Este servidor puede:</p>
        <ul style="margin-left: 30px; color: #555; line-height: 2;">
            <li>Servir páginas HTML</li>
            <li>Manejar archivos estáticos (CSS, JS, imágenes)</li>
            <li>Procesar peticiones GET</li>
            <li>Responder con códigos de estado HTTP</li>
        </ul>
        
        <div class="links">
            <a href="/about.html">Acerca de</a>
            <a href="/contact.html">Contacto</a>
            <a href="/api/info">API Info</a>
        </div>
    </div>
</body>
</html>"""
        
        with open(os.path.join(self.directorio_web, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
            
        # Crear página about
        about_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Acerca de</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #667eea; }
        a { color: #667eea; text-decoration: none; }
    </style>
</head>
<body>
    <h1>Acerca del Servidor</h1>
    <p>Este es un servidor HTTP simple construido con Python y sockets.</p>
    <p><a href="/">← Volver al inicio</a></p>
</body>
</html>"""
        
        with open(os.path.join(self.directorio_web, "about.html"), "w", encoding="utf-8") as f:
            f.write(about_html)
            
    def iniciar(self):
        """Inicia el servidor HTTP"""
        try:
            self.servidor.bind((self.host, self.puerto))
            self.servidor.listen(5)
            print("=" * 70)
            print(f"🌐 SERVIDOR HTTP INICIADO")
            print("=" * 70)
            print(f"📍 Dirección: http://{self.host if self.host != '0.0.0.0' else 'localhost'}:{self.puerto}")
            print(f"📁 Directorio: {os.path.abspath(self.directorio_web)}/")
            print(f"⏰ Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 70)
            print("Presiona Ctrl+C para detener el servidor\n")
            
            while True:
                cliente_socket, direccion = self.servidor.accept()
                self.manejar_peticion(cliente_socket, direccion)
                
        except KeyboardInterrupt:
            print("\n\n[SERVIDOR] Detenido por el usuario")
        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            self.servidor.close()
            
    def manejar_peticion(self, cliente_socket, direccion):
        """Maneja una petición HTTP"""
        try:
            # Recibir petición
            peticion = cliente_socket.recv(4096).decode('utf-8')
            
            if not peticion:
                return
                
            # Parsear petición
            lineas = peticion.split('\n')
            primera_linea = lineas[0].strip()
            
            print(f"[{direccion[0]}] {primera_linea}")
            
            # Extraer método y ruta
            partes = primera_linea.split()
            if len(partes) < 2:
                return
                
            metodo = partes[0]
            ruta = partes[1]
            
            # Manejar según el método
            if metodo == "GET":
                self.manejar_get(cliente_socket, ruta)
            else:
                self.enviar_respuesta(cliente_socket, 405, "Method Not Allowed")
                
        except Exception as e:
            print(f"[ERROR] {direccion[0]}: {e}")
        finally:
            cliente_socket.close()
            
    def manejar_get(self, cliente_socket, ruta):
        """Maneja peticiones GET"""
        # Ruta raíz
        if ruta == "/":
            ruta = "/index.html"
            
        # API endpoint de ejemplo
        if ruta.startswith("/api/"):
            self.manejar_api(cliente_socket, ruta)
            return
            
        # Construir ruta completa
        ruta_archivo = os.path.join(self.directorio_web, ruta.lstrip('/'))
        
        # Verificar si el archivo existe
        if not os.path.exists(ruta_archivo):
            self.enviar_respuesta(cliente_socket, 404, "Not Found",
                                 "<h1>404 - Página No Encontrada</h1>")
            return
            
        # Leer y enviar archivo
        try:
            with open(ruta_archivo, 'rb') as archivo:
                contenido = archivo.read()
                
            # Determinar tipo MIME
            tipo_mime, _ = mimetypes.guess_type(ruta_archivo)
            if tipo_mime is None:
                tipo_mime = "application/octet-stream"
                
            self.enviar_respuesta(cliente_socket, 200, "OK", contenido, tipo_mime)
            
        except Exception as e:
            print(f"[ERROR] Leyendo archivo: {e}")
            self.enviar_respuesta(cliente_socket, 500, "Internal Server Error")
            
    def manejar_api(self, cliente_socket, ruta):
        """Maneja peticiones a la API"""
        if ruta == "/api/info":
            info = {
                "servidor": "HTTP Simple",
                "version": "1.0",
                "timestamp": datetime.now().isoformat(),
                "uptime": "activo"
            }
            import json
            contenido = json.dumps(info, indent=2)
            self.enviar_respuesta(cliente_socket, 200, "OK", contenido, "application/json")
        else:
            self.enviar_respuesta(cliente_socket, 404, "Not Found",
                                 '{"error": "Endpoint no encontrado"}', "application/json")
            
    def enviar_respuesta(self, cliente_socket, codigo, mensaje, contenido="", tipo_mime="text/html"):
        """Envía una respuesta HTTP"""
        # Convertir contenido a bytes si es string
        if isinstance(contenido, str):
            contenido = contenido.encode('utf-8')
        elif not contenido:
            contenido = f"<h1>{codigo} - {mensaje}</h1>".encode('utf-8')
            
        # Construir encabezados
        respuesta = f"HTTP/1.1 {codigo} {mensaje}\r\n"
        respuesta += f"Content-Type: {tipo_mime}; charset=utf-8\r\n"
        respuesta += f"Content-Length: {len(contenido)}\r\n"
        respuesta += "Connection: close\r\n"
        respuesta += "\r\n"
        
        # Enviar respuesta
        cliente_socket.send(respuesta.encode('utf-8'))
        cliente_socket.send(contenido)

if __name__ == "__main__":
    servidor = ServidorHTTP(host='0.0.0.0', puerto=8080)
    servidor.iniciar()