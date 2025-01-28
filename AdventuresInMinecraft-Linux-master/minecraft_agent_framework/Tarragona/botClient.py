import mcpi.minecraft as minecraft

class MinecraftBot:
    def __init__(self, player_name):
        # Conexión al servidor de Minecraft (se espera que esté corriendo localmente)
        self.mc = minecraft.Minecraft.create()
        self.player_name = player_name

    def send_welcome_message(self):
        # Enviar un mensaje de bienvenida al chat
        self.mc.postToChat(f"{self.player_name} se ha conectado correctamente al servidor. Vamos a comenzar a construir el Anfiteatro Romano de Tarragona!")

# Ejecución local
if __name__ == "__main__":
    player_name = input("Introduce tu nombre de jugador en Minecraft: ")  # Pedir el nombre del jugador
    bot = MinecraftBot(player_name)  # Crear la instancia del bot con el nombre del jugador
    bot.send_welcome_message()  # Enviar el mensaje de bienvenida
