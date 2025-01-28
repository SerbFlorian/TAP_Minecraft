import unittest
from unittest.mock import MagicMock, patch  # Asegúrate de que MagicMock esté importado
from ..agents.zombiBot import CounterObserver, LoggerObserver, ZombiBot
from mcpi.minecraft import Minecraft

class TestZombiBot(unittest.TestCase):
    @patch('builtins.input', return_value='Y')  # Parcheamos input() para evitar EOFError
    @patch('mcpi.minecraft.Minecraft.create')  # Mock de la conexión a Minecraft
    @patch.dict('sys.modules', {'portscan': MagicMock()})  # Mock de portscan para evitar la llamada a input() en ese módulo
    def setUp(self, mock_mc_create, mock_input):
        """
        Configura el entorno de prueba antes de cada test.
        - Se crea un mock para simular la conexión con Minecraft.
        - Se configura el ZombiBot con observadores (Logger y Counter).
        """
        # Simular la conexión con Minecraft usando MagicMock
        self.mc_mock = MagicMock(spec=Minecraft) 
        mock_mc_create.return_value = self.mc_mock
        
        # Crear el bot con un nombre de jugador ficticio
        self.bot = ZombiBot(self.mc_mock, name="ZombiBot", player_name="florian")
        
        # Crear los observadores (Logger y Counter)
        self.logger = LoggerObserver()
        self.counter = CounterObserver(self.bot) 

        # Agregar los observadores al bot
        self.bot.add_observer(self.logger)
        self.bot.add_observer(self.counter)

        # Evitar que el bot entre en un bucle infinito sobrescribiendo su método `run`
        self.bot.run = lambda: None  # Sobrescribimos para que no se quede en un bucle infinito

    def test_handle_message_normal(self):
        """
        Prueba que el bot maneja mensajes normales correctamente.
        - Verifica que responde con "Yes" o "No".
        - Asegura que no se contabilicen insultos cuando no se envían.
        """
        # Simular mensajes normales
        message = MagicMock()
        normal_messages = ["Qué tal", "Cómo estás"] 
        expected_responses = {"ZombiBot: Yes", "ZombiBot: No"}  

        for message_content in normal_messages:
            message.message = message_content  # Configurar el contenido del mensaje
            self.bot.handle_message(message)  # Manejar el mensaje
            
            # Verificar que el bot respondió con una de las respuestas esperadas
            called_response = self.mc_mock.postToChat.call_args[0][0]
            self.assertIn(called_response, expected_responses)
        
        # Verificar que no se registraron insultos
        self.assertEqual(self.counter.insultos_recibidos, 0)

    @patch('sys.exit')  # Mock de sys.exit para evitar que el proceso se cierre durante el test
    def test_activate_tnt_with_insults(self, mock_exit):
        """
        Verifica que el bot activa el TNT después de recibir 3 insultos.
        - Asegura que los mensajes normales no incrementan el contador de insultos.
        - Valida que la cuenta regresiva y el mensaje de explosión se envíen correctamente.
        - Confirma que `sys.exit` se llama al finalizar.
        """
        message = MagicMock()
        
        # Enviar mensajes normales y verificar que no activan insultos
        normal_messages = ["Qué tal", "Cómo estás"]
        for message_content in normal_messages:
            message.message = message_content
            self.bot.handle_message(message)
        
        # Confirmar que el contador de insultos sigue siendo 0
        self.assertEqual(self.counter.insultos_recibidos, 0)

        # Enviar 3 insultos para activar el TNT
        insultos = ["bobo", "bobo", "bobo"]
        for insulto in insultos:
            message.message = insulto  # Configurar el mensaje como un insulto
            self.bot.handle_message(message)  # Manejar el mensaje
        
        # Confirmar que el contador de insultos llegó a 3
        self.assertEqual(self.counter.insultos_recibidos, 3)
        
        # Verificar que se envió el mensaje de activación del TNT
        self.mc_mock.postToChat.assert_any_call("ZombiBot: Has insultado demasiadas veces! Activando TNT...")

        # Verificar que los mensajes de cuenta regresiva se enviaron correctamente
        for i in range(5, 0, -1):
            self.mc_mock.postToChat.assert_any_call(f"ZombiBot: TNT activado... {i} segundos hasta la explosion.")
        
        # Verificar que se envió el mensaje de explosión final
        self.mc_mock.postToChat.assert_any_call("ZombiBot: BOOOOOOOMMM! Explote y te moriste tambien!")
        
        # Confirmar que `sys.exit` se llamó al finalizar el proceso
        mock_exit.assert_called_once()

if __name__ == "__main__":
    # Ejecutar las pruebas de manera automática
    unittest.main(argv=[''], exit=False)
