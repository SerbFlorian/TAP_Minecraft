import unittest
from unittest.mock import patch
import time
from ..agents.insultBot import InsultBot, InsultCommand, StopInsultCommand

# Clase simulada para reemplazar la conexión real con Minecraft durante las pruebas.
class MockMinecraft:
    def __init__(self):
        self.chat_messages = []  # Lista para almacenar los mensajes enviados al chat.
    
    # Método simulado para publicar mensajes en el chat.
    def postToChat(self, message):
        self.chat_messages.append(message)

# Helper: Espera a que haya mensajes en el chat, con un timeout configurable.
def wait_for_messages(mc, timeout=10):
    """
    Espera hasta `timeout` segundos para que el mock de Minecraft reciba mensajes.
    Devuelve True si llegan mensajes antes del timeout; de lo contrario, False.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if len(mc.chat_messages) > 0:
            return True
        time.sleep(0.1)
    return False

# Clase de pruebas para InsultBot
class TestInsultBot(unittest.TestCase):
    
    # Configuración inicial antes de cada prueba.
    def setUp(self):
        # Crear un MockMinecraft para simular interacciones con el servidor.
        self.mc = MockMinecraft()
        
        # Lista de insultos que el bot usará durante las pruebas.
        self.insults = [
            "Que miras bobo!",
            "Pinche pendejo, andate a la ve*a!",
            "Tira paya bobo!",
            "Mamahuevo!",
            "Estas tonto o k lo k haces?",
            "Payaso!"
        ]
        
        # Instancia del bot con el MockMinecraft.
        self.bot = InsultBot(self.mc, name="TestBot", insults=self.insults)

    @patch('builtins.input', return_value='Y')  # Simula que el usuario responde 'Y' en los inputs.
    def test_insult_bot_starts_insulting(self, mock_input):
        """
        Verifica que el bot comienza a insultar correctamente.
        """
        self.bot.start_insulting()  # Inicia el ciclo de insultos.
        self.assertTrue(wait_for_messages(self.mc))  # Asegura que hay mensajes en el chat.
        self.assertTrue(self.mc.chat_messages)  # Verifica que la lista de mensajes no esté vacía.
        self.assertIn("TestBot:", self.mc.chat_messages[0])  # Comprueba que los mensajes están etiquetados correctamente.

    @patch('builtins.input', return_value='Y') 
    def test_stop_insulting_command(self, mock_input):
        """
        Verifica que el comando `StopInsultCommand` detiene al bot de insultar.
        """
        self.bot.start_insulting()  # Inicia el ciclo de insultos.
        time.sleep(6)  # Espera unos segundos para que se envíen insultos.
        
        # Ejecuta el comando para detener los insultos.
        stop_command = StopInsultCommand(self.bot)
        stop_command.execute()
        time.sleep(2)  # Espera un momento para procesar la detención.
        
        # Verifica que el mensaje de detención se haya enviado.
        self.assertIn("TestBot ha dejado de insultar.", self.mc.chat_messages)
        
        # Asegura que se haya enviado al menos un insulto antes de detenerse.
        self.assertEqual(self.bot.insult_count, 1)

    @patch('builtins.input', return_value='Y') 
    def test_insult_command_starts_insulting(self, mock_input):
        """
        Verifica que el comando `InsultCommand` inicia los insultos correctamente.
        """
        # Ejecuta el comando para iniciar los insultos.
        insult_command = InsultCommand(self.bot)
        insult_command.execute()
        
        self.assertTrue(wait_for_messages(self.mc))  # Asegura que hay mensajes en el chat.
        self.assertTrue(self.mc.chat_messages)  # Verifica que la lista de mensajes no esté vacía.
        self.assertIn("TestBot:", self.mc.chat_messages[0])  # Comprueba que el mensaje está etiquetado correctamente.

    @patch('builtins.input', return_value='Y') 
    def test_set_command(self, mock_input):
        """
        Verifica que el bot puede ejecutar comandos dinámicamente a través de `set_command`.
        """
        # Configura un comando para el bot y lo ejecuta.
        insult_command = InsultCommand(self.bot)
        self.bot.set_command(insult_command)  # Asigna el comando al bot.
        self.bot.execute_command()  # Ejecuta el comando asignado.
        
        self.assertTrue(wait_for_messages(self.mc))  # Asegura que hay mensajes en el chat.
        self.assertTrue(self.mc.chat_messages)  # Verifica que la lista de mensajes no esté vacía.
        self.assertIn("TestBot:", self.mc.chat_messages[0])  # Comprueba que el mensaje está etiquetado correctamente.

# Punto de entrada para ejecutar las pruebas.
if __name__ == '__main__':
    unittest.main()
