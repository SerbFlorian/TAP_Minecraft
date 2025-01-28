import Pyro4
import mcpi.minecraft as minecraft

# Utilizando el patrón Strategy para permitir cambios de comportamiento dinámicos en el bot

# Clase base para las acciones del bot. Define un método abstracto que debe ser implementado por todas las subclases.
class BotAction:
    """Clase base para las acciones del bot"""
    def execute(self, mc):
        """Método que debe ser implementado por las subclases"""
        raise NotImplementedError("Debe implementar el método execute.")

# Acción para construir un bloque en la posición actual del jugador
class BuildAction(BotAction):
    def execute(self, mc):
        """Construir un bloque en la posición actual del jugador"""
        mc.postToChat("Construccion realizada.")
        return "Construccion realizada."

# Acción para destruir un bloque en la posición actual del jugador
class DestroyAction(BotAction):
    def execute(self, mc):
        """Destruir un bloque en la posición actual del jugador"""
        mc.postToChat("Destruccion realizada.")
        return "Destruccion realizada."

# Acción para enviar un saludo al chat de Minecraft
class HelloAction(BotAction):
    def execute(self, mc):
        """Enviar un saludo al chat"""
        mc.postToChat("Hola desde el servidor de BotControl!")
        return "Hola desde el servidor de BotControl!"

# Acción para enviar un mensaje personalizado al chat de Minecraft
class SendChatMessageAction(BotAction):
    def __init__(self, message):
        self.message = message
    
    def execute(self, mc):
        """Enviar un mensaje proporcionado al chat de Minecraft"""
        mc.postToChat(self.message)
        return f"Mensaje enviado: {self.message}"

# Clase que maneja el control de bots, utilizando patrones funcionales y de diseño
@Pyro4.expose  # Este decorador hace que la clase BotControl sea accesible remotamente
class BotControl:
    def __init__(self):
        """Inicializa la conexión a Minecraft"""
        try:
            # Intenta conectar a la instancia local de Minecraft
            self.mc = minecraft.Minecraft.create()  
            print("Conexión a Minecraft exitosa.")
        except Exception as e:
            # Si ocurre un error, imprime un mensaje y asigna None a la conexión
            print(f"Error al conectar con Minecraft: {e}")
            self.mc = None  # Si no se puede conectar, dejamos la conexión como None

        # Mapa de acciones disponibles que pueden ser ejecutadas por el bot
        self.actions = {
            'build': BuildAction(),
            'destroy': DestroyAction(),
            'hello': HelloAction(),
        }

    def _handle_action(self, action_name, *args):
        """Maneja la ejecución de las acciones con reflexión y manejo dinámico de comportamientos"""
        # Recupera la acción asociada al nombre de la acción
        action = self.actions.get(action_name)
        if action:
            # Si la acción existe, la ejecuta
            return action.execute(self.mc)
        else:
            # Si la acción no existe, se intenta enviar un mensaje personalizado
            action = SendChatMessageAction(action_name)
            return action.execute(self.mc)

    # Métodos públicos que facilitan la interacción con el bot
    def build(self):
        """Construir un bloque en la posición actual del jugador."""
        return self._handle_action("build")

    def destroy(self):
        """Destruir un bloque en la posición actual del jugador."""
        return self._handle_action("destroy")

    def hello(self):
        """Enviar un mensaje de saludo."""
        return self._handle_action("hello")

    def send_chat_message(self, message):
        """Enviar un mensaje personalizado al chat de Minecraft."""
        return self._handle_action(message)

# Configuración de Pyro4 para permitir la comunicación remota
daemon = Pyro4.Daemon()  # Inicia un servidor Pyro4 que escuchará las peticiones remotas
ns = Pyro4.locateNS()  # Localiza el servidor de nombres de Pyro4 (donde se registran los objetos remotos)

# Registra la clase BotControl en el servidor Pyro4 y obtiene la URI (Identificador único del objeto)
uri = daemon.register(BotControl)

# Registrar el objeto remoto en el servidor de nombres para que los clientes puedan acceder a él
# Aquí 'BotControl' es el nombre que se usará para acceder a la clase remota
ns.register("BotControl", uri)

print(f"BotControl Server is running. URI: {uri}")  # Imprimimos la URI del objeto remoto para que los clientes puedan utilizarla

# El servidor comienza a escuchar para peticiones remotas
# Esto mantiene el servidor Pyro4 en ejecución y acepta solicitudes hasta que se detenga
daemon.requestLoop() 
