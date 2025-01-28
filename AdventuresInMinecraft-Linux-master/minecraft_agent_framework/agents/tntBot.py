import time
import threading
from mcpi.minecraft import Minecraft
from abc import ABC, abstractmethod

# Conexión al servidor de Minecraft
mc = Minecraft.create()

# Interfaz del Observer
class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

# Implementación de un Observer para registrar mensajes en consola
class LoggerObserver(Observer):
    def update(self, message: str):
        print(f"Logger: {message}") 

# Clase TNTBot que es el "subject" que notifica a los observadores
class TNTBot:
    def __init__(self, mc, name="TNTBot"):
        # Inicialización del bot TNT con el servidor de Minecraft, nombre y tiempo de explosión
        self.mc = mc
        self.name = name
        self.explosion_time = 10  # segundos antes de la explosión
        self.observers = []  # Lista de observadores
        self.finished = False  # Variable para indicar si el bot ha terminado su acción

    # Método para agregar un observador
    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    # Método para notificar a los observadores
    def notify_observers(self, message: str):
        # Recorrer la lista de observadores y enviarles el mensaje
        for observer in self.observers:
            observer.update(message)

    def countdown_and_explode(self):
        # Contar hacia atrás desde 5 segundos hasta la explosión
        for i in range(5, -1, -1): 
            message = f"{self.name}: En {i} segundos rebiento..."
            self.mc.postToChat(message)  # Enviar mensaje al chat de Minecraft
            self.notify_observers(message)  # Notificar a los observadores del mensaje
            time.sleep(1)  # Esperar 1 segundo entre cada mensaje

        # Pausa de 5 segundos antes de la explosión para aumentar la tensión
        time.sleep(5)

        # Mensaje final antes de la explosión
        message = f"{self.name}: Te pensabas que si..."
        self.mc.postToChat(message)
        self.notify_observers(message)  # Notificar a los observadores
        time.sleep(5)  # Pausa de 5 segundos antes de mostrar el mensaje de explosión
        
        # Mensaje de la explosión
        message = f"{self.name}: Pues si... BOOOOOOOOOOOOOMMMMM!"
        self.mc.postToChat(message)  # Enviar mensaje de explosión al chat
        self.notify_observers(message)  # Notificar a los observadores
        
        # Mensaje final confirmando que el bot ha explotado
        self.mc.postToChat(f"{self.name} ha explotado.")  

        # Marcar que el bot ha terminado su acción
        self.finished = True

    def start(self):
        # Iniciar el proceso de cuenta atrás y explosión en un hilo separado para no bloquear el flujo principal
        thread = threading.Thread(target=self.countdown_and_explode)
        thread.start()  # El hilo comienza su ejecución
        return thread  # Devuelve el hilo para su posterior manejo

# Crear el observador Logger que registrará los mensajes
logger = LoggerObserver()

# Crear los bots TNT, cada uno con un nombre diferente
bot1 = TNTBot(mc, name="tntBot_1")
bot2 = TNTBot(mc, name="tntBot_2")

# Agregar el observador a ambos bots para que registren los mensajes
bot1.add_observer(logger)
bot2.add_observer(logger)

# Iniciar la cuenta atrás para ambos bots en hilos separados
thread1 = bot1.start()  # Ya inicia el hilo dentro de 'start'
thread2 = bot2.start()  # Ya inicia el hilo dentro de 'start'

# Esperar a que ambos hilos terminen antes de finalizar el programa
while not bot1.finished or not bot2.finished:
    time.sleep(1)  # Esperar mientras los bots siguen funcionando

# Mostrar mensaje de finalización del programa
print("Ambos bots han explotado. El programa ha finalizado exitosamente.")

# Finalizar el programa con una pequeña pausa
time.sleep(1)
