# Programación en Redes

Sistema de chat cliente-servidor con Python usando sockets y threading.

## Archivos

**Básico**
- `servidor.py` - Servidor simple que recibe un mensaje
- `cliente.py` - Cliente que envía un mensaje

**Chat Multi-Cliente**
- `servidor_chat.py` - Servidor que maneja múltiples usuarios simultáneamente
- `cliente_chat.py` - Cliente de chat con envío/recepción asíncrona

## Uso
```bash
# Iniciar servidor
python servidor_chat.py

# Conectar clientes (varias terminales)
python cliente_chat.py
```

Escribe `/salir` para desconectarte.

## Conceptos

- Sockets TCP (AF_INET, SOCK_STREAM)
- Threading para múltiples clientes
- Broadcast de mensajes
- Codificación UTF-8