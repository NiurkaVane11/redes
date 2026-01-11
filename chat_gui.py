import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog

class ChatGUI:
    def __init__(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectado = False
        
        # Configuración de la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Chat Cliente")
        self.ventana.geometry("500x600")
        self.ventana.configure(bg="#2c3e50")
        
        # Frame superior para información
        frame_superior = tk.Frame(self.ventana, bg="#34495e", height=50)
        frame_superior.pack(fill=tk.X, padx=10, pady=5)
        
        self.label_estado = tk.Label(
            frame_superior, 
            text="● Desconectado", 
            fg="#e74c3c",
            bg="#34495e",
            font=("Arial", 10, "bold")
        )
        self.label_estado.pack(pady=10)
        
        # Área de mensajes
        frame_chat = tk.Frame(self.ventana, bg="#2c3e50")
        frame_chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(
            frame_chat, 
            text="Mensajes:", 
            bg="#2c3e50", 
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W)
        
        self.area_mensajes = scrolledtext.ScrolledText(
            frame_chat,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#2c3e50",
            state=tk.DISABLED
        )
        self.area_mensajes.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Frame inferior para entrada de mensajes
        frame_inferior = tk.Frame(self.ventana, bg="#2c3e50")
        frame_inferior.pack(fill=tk.X, padx=10, pady=5)
        
        self.entrada_mensaje = tk.Entry(
            frame_inferior,
            font=("Arial", 11),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        self.entrada_mensaje.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entrada_mensaje.bind("<Return>", lambda e: self.enviar_mensaje())
        
        self.boton_enviar = tk.Button(
            frame_inferior,
            text="Enviar",
            command=self.enviar_mensaje,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            width=10,
            cursor="hand2"
        )
        self.boton_enviar.pack(side=tk.RIGHT)
        
        # Frame de botones de conexión
        frame_botones = tk.Frame(self.ventana, bg="#2c3e50")
        frame_botones.pack(fill=tk.X, padx=10, pady=5)
        
        self.boton_conectar = tk.Button(
            frame_botones,
            text="Conectar",
            command=self.conectar,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15,
            cursor="hand2"
        )
        self.boton_conectar.pack(side=tk.LEFT, padx=5)
        
        self.boton_desconectar = tk.Button(
            frame_botones,
            text="Desconectar",
            command=self.desconectar,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.boton_desconectar.pack(side=tk.LEFT, padx=5)
        
        # Deshabilitar entrada y botón de enviar inicialmente
        self.entrada_mensaje.config(state=tk.DISABLED)
        self.boton_enviar.config(state=tk.DISABLED)
        
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        
    def mostrar_mensaje(self, mensaje):
        """Muestra un mensaje en el área de chat"""
        self.area_mensajes.config(state=tk.NORMAL)
        self.area_mensajes.insert(tk.END, mensaje + "\n")
        self.area_mensajes.see(tk.END)
        self.area_mensajes.config(state=tk.DISABLED)
        
    def conectar(self):
        """Conecta al servidor de chat"""
        # Solicitar datos de conexión
        host = simpledialog.askstring("Conexión", "Ingresa la IP del servidor:", 
                                      initialvalue="127.0.0.1")
        if not host:
            return
            
        puerto = simpledialog.askinteger("Conexión", "Ingresa el puerto:", 
                                         initialvalue=5555, minvalue=1024, maxvalue=65535)
        if not puerto:
            return
            
        self.nombre_usuario = simpledialog.askstring("Nombre", "Ingresa tu nombre de usuario:")
        if not self.nombre_usuario:
            return
        
        try:
            self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente.connect((host, puerto))
            self.conectado = True
            
            # Enviar nombre de usuario
            self.cliente.send(self.nombre_usuario.encode('utf-8'))
            
            # Actualizar interfaz
            self.label_estado.config(text=f"● Conectado como {self.nombre_usuario}", fg="#27ae60")
            self.boton_conectar.config(state=tk.DISABLED)
            self.boton_desconectar.config(state=tk.NORMAL)
            self.entrada_mensaje.config(state=tk.NORMAL)
            self.boton_enviar.config(state=tk.NORMAL)
            self.entrada_mensaje.focus()
            
            # Iniciar hilo para recibir mensajes
            hilo_recibir = threading.Thread(target=self.recibir_mensajes, daemon=True)
            hilo_recibir.start()
            
            self.mostrar_mensaje("=== Conectado al servidor ===")
            
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar al servidor:\n{str(e)}")
            self.conectado = False
            
    def recibir_mensajes(self):
        """Recibe mensajes del servidor continuamente"""
        while self.conectado:
            try:
                mensaje = self.cliente.recv(1024).decode('utf-8')
                if mensaje:
                    self.mostrar_mensaje(mensaje)
                else:
                    break
            except:
                break
        
        if self.conectado:
            self.mostrar_mensaje("=== Desconectado del servidor ===")
            self.desconectar()
            
    def enviar_mensaje(self):
        """Envía un mensaje al servidor"""
        mensaje = self.entrada_mensaje.get().strip()
        if mensaje and self.conectado:
            try:
                self.cliente.send(mensaje.encode('utf-8'))
                self.entrada_mensaje.delete(0, tk.END)
            except:
                messagebox.showerror("Error", "No se pudo enviar el mensaje")
                self.desconectar()
                
    def desconectar(self):
        """Desconecta del servidor"""
        if self.conectado:
            self.conectado = False
            try:
                self.cliente.close()
            except:
                pass
            
            # Actualizar interfaz
            self.label_estado.config(text="● Desconectado", fg="#e74c3c")
            self.boton_conectar.config(state=tk.NORMAL)
            self.boton_desconectar.config(state=tk.DISABLED)
            self.entrada_mensaje.config(state=tk.DISABLED)
            self.boton_enviar.config(state=tk.DISABLED)
            self.mostrar_mensaje("=== Desconectado ===")
            
    def cerrar_ventana(self):
        """Maneja el cierre de la ventana"""
        self.desconectar()
        self.ventana.destroy()
        
    def ejecutar(self):
        """Inicia la interfaz gráfica"""
        self.ventana.mainloop()

if __name__ == "__main__":
    app = ChatGUI()
    app.ejecutar()