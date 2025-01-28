import Pyro4

# URI del objeto remoto BotControl
uri = "PYRO:obj_339bf2cc5cec425da204bb44e92e9e63@localhost:59330"  # URI del servidor BotControl

# Funciones puras que representan las acciones del bot
def build(bot_control):
    """Función para construir un bloque."""
    return bot_control.build()

def destroy(bot_control):
    """Función para destruir un bloque."""
    return bot_control.destroy()

def hello(bot_control):
    """Función para saludar al bot."""
    return bot_control.hello()

def send_message(bot_control, message):
    """Función para enviar un mensaje al servidor."""
    return bot_control.send_chat_message(message)

# Función que mapea el comando a la acción correspondiente
def action_map(command, bot_control):
    """Mapea el comando recibido a una función y ejecuta la acción correspondiente."""
    actions = {
        "build": build,
        "destroy": destroy,
        "hello": hello
    }

    # Si el comando está en el mapeo, ejecutar la acción correspondiente
    if command in actions:
        return actions[command](bot_control)
    
    # Si el comando no está en el mapeo, enviamos el mensaje como texto
    return send_message(bot_control, command)

# Función para enviar el mensaje y ejecutar el comando
def send_chat_message(message):
    """Función para enviar mensajes al servidor remoto BotControl y ejecutar comandos."""
    try:
        # Obtener el proxy del servidor BotControl
        bot_control = Pyro4.Proxy(uri)

        # Ejecutar la acción basada en el mensaje
        response = action_map(message, bot_control)

        # Imprimir la respuesta del servidor
        print(f"Response from server: {response}")
    
    except Pyro4.errors.CommunicationError as e:
        # Si ocurre un error en la comunicación
        print(f"Error al conectar con el servidor: {e}")
    except Exception as e:
        # Captura de errores generales
        print(f"Ocurrio un error inesperado: {e}")

# Se envían varios mensajes para probar las diferentes funcionalidades del servidor BotControl
if __name__ == "__main__":
    # Lista de ejemplos de mensajes
    commands = ["build", "destroy", "hello", "Hola desde el cliente!"]
    
    # Mapear y ejecutar cada comando
    for command in commands:
        send_chat_message(command)
