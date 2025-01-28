from mcpi.minecraft import Minecraft
import time
import random
import threading
import sys

# Conectar al servidor de Minecraft
mc = Minecraft.create()

# Lista de insultos que los bots pueden decir
insults = [
    "Que miras bobo!",
    "Pinche pendejo, andate a la ve*a!",
    "Tira paya bobo!",
    "Mamahuevo!",
    "Estas tonto o k lo k haces?",
    "Payaso!"
]

# Función para manejar la interrupción del programa con Ctrl+C
def signal_handler(sig, frame):
    print("\n¡Deteniendo el programa!")  # Mensaje al detenerse el programa
    # Detener todos los bots antes de cerrar el programa
    for bot in bots:
        bot.stop_insulting()  # Detener el comportamiento de insultar de todos los bots
    mc.postToChat("El insulto ha sido detenido. Los bots permanecen en el juego.")  # Mensaje de detención
    sys.exit(0)  # Salir del programa de forma controlada

# Comando base para el patrón Command
class Command:
    def execute(self):
        pass  # Este método será sobrecargado por las clases derivadas

# Comando para que el bot comience a insultar
class InsultCommand(Command):
    def __init__(self, bot):
        self.bot = bot  # Asociar el comando con el bot específico
    
    def execute(self):
        # Ejecutar el comando, haciendo que el bot comience a insultar
        self.bot.start_insulting()

# Comando para que el bot deje de insultar
class StopInsultCommand(Command):
    def __init__(self, bot):
        self.bot = bot  # Asociar el comando con el bot específico
    
    def execute(self):
        # Ejecutar el comando, haciendo que el bot deje de insultar
        self.bot.stop_insulting()

# Bot que insultará a intervalos
class InsultBot:
    def __init__(self, mc, name, insults):
        self.mc = mc  # Conexión al servidor de Minecraft
        self.name = name  # Nombre del bot
        self.insults = insults  # Lista de insultos
        self.insult_count = 0  # Contador de insultos enviados
        self.max_insults = 10  # Número máximo de insultos antes de detenerse
        self.running = True  # Flag para controlar si el bot debe seguir insultando
        self.command = None  # Comando asignado al bot (por ejemplo, empezar o detener)

    def insult(self):
        # Método que hace que el bot insulte a intervalos
        while self.running and self.insult_count < self.max_insults:
            time.sleep(5)  # Espera 5 segundos entre insultos
            insult = random.choice(self.insults)  # Elegir un insulto aleatorio
            self.insult_count += 1
            # Publicar el insulto en el chat de Minecraft
            self.mc.postToChat(f"{self.name}: {insult}")
        
        if self.insult_count >= self.max_insults:
            # Si el bot ha alcanzado el máximo de insultos, se detiene
            self.mc.postToChat(f"{self.name} ha insultado 10 veces y se ha detenido.")

    def start_insulting(self):
        # Inicia el proceso de insultar en un hilo separado para no bloquear el programa
        insult_thread = threading.Thread(target=self.insult)
        insult_thread.start()

    def stop_insulting(self):
        # Detiene el comportamiento de insultar
        self.running = False
        self.mc.postToChat(f"{self.name} ha dejado de insultar.")

    def set_command(self, command: Command):
        """Método para asignar un comando al bot"""
        self.command = command

    def execute_command(self):
        """Método para ejecutar el comando asignado"""
        if self.command:
            self.command.execute()

# Crear y lanzar los bots (sin necesidad de posiciones ni NPCs)
npc_count = 3  # Número de bots a crear
bots = []  # Lista para almacenar los bots

# Crear el invocador de comandos, que se encargará de ejecutar las acciones
invoker = []  # Lista para almacenar los comandos

# Crear y poner en marcha los bots
for i in range(npc_count):
    bot_name = f"InsultBot_{i+1}"  # Nombre del bot
    bot = InsultBot(mc, name=bot_name, insults=insults)  # Crear el bot con la lista de insultos
    
    # Crear los comandos correspondientes a cada bot
    insult_command = InsultCommand(bot)  # Comando para que el bot comience a insultar
    stop_insult_command = StopInsultCommand(bot)  # Comando para que el bot deje de insultar
    
    # Asignar el comando de insultar al bot
    bot.set_command(insult_command)
    
    # Agregar el comando de insultar al invocador (lista de comandos)
    invoker.append(insult_command)
    
    # Agregar el bot a la lista de bots
    bots.append(bot)

# Confirmación de que los bots han comenzado a insultar
mc.postToChat(f"{npc_count} InsultBots estan insultando cerca de ti!")

# Iniciar la ejecución de los comandos
for command in invoker:
    command.execute()  # Ejecutar todos los comandos de "insultar" para cada bot
