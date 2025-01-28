import mcpi.minecraft as minecraft
import time

# Clase BotControl para interactuar con el servidor de Minecraft
class BotControl:
    def __init__(self):
        self.mc = minecraft.Minecraft.create()  # Conexión al servidor
        self.sent_messages = {}  # Para registrar las estructuras a las que ya se les ha enviado un mensaje histórico
    
    # Enviar mensaje histórico sobre el Anfiteatro Romano
    def send_historical_message(self, structure_name):
        history_messages = {
            "Anfiteatro Romano de Tarragona": (
                "Introduccion: "
                "El anfiteatro de Tarraco es un edificio romano construido muy cerca del mar, tras la muralla de la ciudad de Tarraco, "
                "capital de la provincia romana Hispania Citerior Tarraconensis. Es una de las localizaciones del lugar Patrimonio de la Humanidad llamado -Conjunto arqueologico en Tarraco-."
                "Fue construido a finales del siglo II d. C., en un espacio que habia sido un area funeraria."
            )
        }
        
        # Enviar la historia en intervalos
        for key, message in history_messages.items():
            if key not in self.sent_messages:
                self.mc.postToChat(message)
                self.sent_messages[key] = True  # Evitar enviar el mismo mensaje repetidamente
                time.sleep(2)  # Pausa de 2 segundos para dar tiempo entre mensajes
    
    def send_curious_messages(self):
        """Enviar mensajes de curiosidades cada 5 minutos."""
        curiosities = [
            "Curiosidad 1: Durante el imperio de Heliogabalo, a del siglo III d. C., en el anfiteatro se llevaron a cabo diversas reformas. En conmemoracion de este hecho, el podium se corono con una gran inscripcion monumental, de la que se conservan numerosos fragmentos.",
            "Curiosidad 2: El 21 de enero del ano 259, en el marco de las persecuciones contra los cristianos en epoca del emperador Valeriano, fueron quemados vivos en la arena del anfiteatro el obispo de la ciudad, Fructuoso y sus diaconos, Augurio y Eulogio.",
            "Curiosidad 3: Durante el siglo V, y como consecuencia de la politica religiosa de los primeros emperadores cristianos, el anfiteatro fue perdiendo sus funciones originarias. Un siglo despues se aprovecharon las piedras de este, sobre todo los sillares de la graderia, "
            "para construir una basilica cristiana de tres naves que conmemoro el lugar del martirio de los tres santos de la Iglesia tarraconense. Alrededor del templo se construyo un cementerio con tumbas excavadas en la arena y mausoleos funerarios adosados a la iglesia.",
            "Curiosidad 4: La invasion islamica abrio un periodo de abandono del conjunto hasta que, en el siglo XII, se erigio sobre los cimientos de la basilica visigotica un nuevo templo bajo la advocacion de Santa Maria del Milagro. De estilo romanico y planta de cruz latina, una sola nave y un abside cuadrangular. La iglesia se mantuvo en pie hasta 1915."
        ]
        
        for curiosity in curiosities:
            self.mc.postToChat(curiosity)  # Enviar el mensaje de curiosidad
            time.sleep(1)  # Espera de 5 minutos (300 segundos)

    # Función para guiar al jugador mientras replica el anfiteatro
    def guide_for_amphitheater(self, player_id):
        # Enviar los mensajes históricos
        self.send_historical_message("Anfiteatro Romano de Tarragona")
        
        # Generar las dos zonas: estructura de referencia y zona plana
        self.generate_reference_structure()
        self.create_flat_zone()
        
        # Iniciar el proceso en el chat con instrucciones
        self.mc.postToChat(f"Vamos a empezar, {player_id}! Aqui esta la estructura del Anfiteatro Romano.")
        self.mc.postToChat("Vamos a trabajar juntos para reconstruir este monumento historico!")
        
        # Ciclo para seguir enviando curiosidades cada 5 minutos
        self.send_curious_messages()

    def generate_reference_structure(self):
        # Lógica para generar la estructura de referencia (no implementada)
        pass
    
    def create_flat_zone(self):
        # Lógica para crear una zona plana (no implementada)
        pass

# Inicializar el servidor y bots
bot_control = BotControl()

# Simulación de interacción
try:
    player_id = 1  # Ejemplo de ID del jugador
    bot_control.guide_for_amphitheater(player_id)
except KeyboardInterrupt:
    print("El programa ha sido interrumpido por el usuario.")
