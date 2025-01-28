import random
import time
from mcpi.minecraft import Minecraft
from abc import ABC, abstractmethod

# Definir la interfaz de la estrategia de respuesta
class ResponseStrategy(ABC):
    @abstractmethod
    def get_response(self, message: str) -> str:
        pass

# Estrategia de respuesta aleatoria (con las frases definidas)
class RandomResponseStrategy(ResponseStrategy):
    def __init__(self):
        self.responses = [
            "Si, absolutamente!",
            "No, ni en un millon de anos.",
            "Pregunta de nuevo mas tarde.",
            "Es cierto.",
            "Muy dudoso.",
            "Las estrellas dicen que no.",
            "Sin lugar a dudas.",
            "No tengo ni idea."
        ]

    def get_response(self, message: str) -> str:
        # Escoge una respuesta de forma aleatoria
        return random.choice(self.responses)

# Clase principal del bot
class OracleBot:
    def __init__(self, mc, name, strategy: ResponseStrategy):
        # Inicializa el bot con la conexión de Minecraft, el nombre y la estrategia de respuesta
        self.mc = mc
        self.name = name
        self.strategy = strategy  # La estrategia es pasada al constructor
        self.running = True  # Variable de control para detener el bot

    def listen_and_respond(self, iterations=None):
        count = 0
        while self.running:
            # Si iterations no es None, limita las iteraciones
            if iterations is not None and count >= iterations:
                break
            # Obtiene los mensajes del chat
            messages = self.mc.events.pollChatPosts()
            for message in messages:
                print(f"Mensaje recibido: {message.message}")  # Imprime el mensaje recibido
                # Usa la estrategia para obtener la respuesta
                response = self.strategy.get_response(message.message)
                # Enviar la respuesta al chat de Minecraft
                self.mc.postToChat(f"{self.name}: {response}")
                print(f"Enviando respuesta: {self.name}: {response}")  # Imprime la respuesta enviada
            count += 1
            time.sleep(1)

    def stop(self):
        # Detiene el bot y muestra un mensaje de despedida
        print(f"Deteniendo {self.name}...")
        self.mc.postToChat(f"{self.name} bot finalizado. Hasta la proxima!.")
        self.running = False  # Cambia el estado para detener el bot

# Conectar al servidor de Minecraft
mc = Minecraft.create()

# Crear la instancia del bot con la estrategia de respuesta aleatoria
oracle_bot = OracleBot(mc, name="OracleBot", strategy=RandomResponseStrategy())

# Enviar mensaje de inicio para que los usuarios sepan que el bot está activo
mc.postToChat(f"{oracle_bot.name} esta listo para comenzar la conversacion. Hazme una pregunta!")

# Iniciar el bot
if __name__ == "__main__":
    oracle_bot.listen_and_respond()