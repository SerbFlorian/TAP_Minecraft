from mcpi.minecraft import Minecraft
import time
import random
import signal
import sys
from abc import ABC, abstractmethod

# Conexión al servidor de Minecraft
mc = Minecraft.create()

# Lista de insultos comunes que el bot detectará
insultos_comunes = [
    "payaso", "bobo", "tonto", "estupido", "idiota", "imbecil", "loco", "mierda", "basura", "pedo", "pelotudo", "necio"
]

# Interfaz Observer (patrón de diseño) que obliga a las clases derivadas a implementar el método `update`
class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

# Observador que registra los mensajes en consola
class LoggerObserver(Observer):
    def update(self, message: str):
        print(f"Logger: {message}")

# Observador que cuenta los insultos detectados
class CounterObserver(Observer):
    def __init__(self, bot):
        self.insultos_recibidos = 0  # contador de insultos
        self.bot = bot  # Referencia al bot para interactuar con él si se excede el límite

    def update(self, message: str):
        # Comprueba si el mensaje contiene algún insulto de la lista
        if any(insulto in message.lower() for insulto in insultos_comunes):
            self.insultos_recibidos += 1  # Incrementa el contador de insultos
            print(f"Contador de insultos: {self.insultos_recibidos} insultos recibidos.")
            # Si se supera el límite, activa el mecanismo de TNT en el bot
            if self.insultos_recibidos >= 3:
                self.bot.activate_tnt()

# Clase principal del bot
class ZombiBot:
    def __init__(self, mc, name, player_name="florian"):
        self.mc = mc  # Referencia al servidor de Minecraft
        self.name = name  # Nombre del bot
        self.player_name = player_name  # Nombre del jugador con el que interactúa el bot
        self.observers = []  # Lista de observadores registrados

    # Método para añadir observadores al bot
    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    # Notifica a todos los observadores cuando se recibe un mensaje
    def notify_observers(self, message: str):
        for observer in self.observers:
            observer.update(message)

    # Método principal para iniciar la interacción del bot
    def run(self):
        """Este método inicia el bot y le permite escuchar mensajes del chat en tiempo real."""
        try:
            self.mc.postToChat(f"{self.name} ha comenzado a interactuar con el jugador {self.player_name}. Vamos a jugar!")
            print(f"{self.name} ha comenzado a interactuar con el jugador {self.player_name}.")  # Mensaje en consola

            while True:
                # Escucha los mensajes del chat de Minecraft
                messages = self.mc.events.pollChatPosts()
                for message in messages:
                    self.handle_message(message)  # Procesa cada mensaje recibido
                time.sleep(1)  # Intervalo de espera entre cada chequeo
        except KeyboardInterrupt:
            self.stop()  # Detiene el bot si se recibe Ctrl+C

    # Maneja los mensajes del chat
    def handle_message(self, message):
        self.notify_observers(message.message)  # Notifica a los observadores

        # Responde a los insultos detectados
        if any(insulto in message.message.lower() for insulto in insultos_comunes):
            self.mc.postToChat(f"{self.name}: Oye, no me insultes!")
            print(f"{self.name}: Recibido insulto: {message.message}")
        else:
            # Responde con un mensaje aleatorio si no hay insultos
            response = random.choice(["Yes", "No"])
            self.mc.postToChat(f"{self.name}: {response}")
            print(f"{self.name}: {response}")

    # Método para activar el mecanismo de TNT si se detectan demasiados insultos
    def activate_tnt(self):
        self.mc.postToChat(f"{self.name}: Has insultado demasiadas veces! Activando TNT...")
        for i in range(5, 0, -1):
            self.mc.postToChat(f"{self.name}: TNT activado... {i} segundos hasta la explosion.")
            time.sleep(1)
        self.mc.postToChat(f"{self.name}: BOOOOOOOMMM! Explote y te moriste tambien!")
        self.stop()

    # Detiene el bot y cierra su ejecución
    def stop(self):
        self.mc.postToChat(f"{self.name} ha terminado su tarea. Desactivando bot.")
        print(f"{self.name} ha terminado su tarea.")
        sys.exit(0)

# Función para manejar la señal de interrupción (Ctrl+C)
def signal_handler(signal, frame):
    print("Deteniendo el bot...")
    bot.stop()  # Llama al método de detener el bot
    sys.exit(0)

# Registrar la señal para manejar Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Crear el bot y los observadores
bot = ZombiBot(mc, name="ZombiBot", player_name="florian")
logger = LoggerObserver()  # Observador que registra mensajes en consola
counter = CounterObserver(bot)  # Observador que cuenta insultos

# Añadir observadores al bot
bot.add_observer(logger)
bot.add_observer(counter)

# Este bloque solo se ejecutará si se invoca explícitamente el programa
def start_bot():
    print("Presiona Ctrl+C para detener el programa...")
    bot.run()

if __name__ == "__main__":
    start_bot()  # Inicia el bot
