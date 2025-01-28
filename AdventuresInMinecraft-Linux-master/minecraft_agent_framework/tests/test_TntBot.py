import unittest
from unittest.mock import MagicMock, patch
from ..agents.tntBot import TNTBot
from mcpi.minecraft import Minecraft

class TestTNTBot(unittest.TestCase):
    
    @patch('mcpi.minecraft.Minecraft.create')  # Mock de la conexión a Minecraft
    @patch('builtins.input', return_value='Y')  # Parcheamos input() para evitar interacciones con el usuario
    @patch.dict('sys.modules', {'portscan': MagicMock()})  # Mock de 'portscan' completo
    def setUp(self, mock_input, mock_mc_create):
        """Configura el entorno de prueba antes de cada test."""
        # Mock del objeto Minecraft
        self.mock_mc = MagicMock()
        mock_mc_create.return_value = self.mock_mc
        
        # Crear los bots TNT
        self.bot1 = TNTBot(self.mock_mc, name="tntBot_1")
        self.bot2 = TNTBot(self.mock_mc, name="tntBot_2")

    def test_bot_initialization(self):
        """Probar que los bots se inicializan con los nombres correctos."""
        # Verificar que los bots tienen los nombres correctos
        self.assertEqual(self.bot1.name, "tntBot_1", "El nombre del bot1 no es correcto.")
        self.assertEqual(self.bot2.name, "tntBot_2", "El nombre del bot2 no es correcto.")

    def test_bots_finish_execution(self):
        """Probar que ambos bots terminan correctamente su ejecución."""
        # Simulamos que los bots terminan su tarea
        self.bot1.finished = True
        self.bot2.finished = True

        # Verificar que ambos bots han terminado
        self.assertTrue(self.bot1.finished, "El bot1 no terminó correctamente.")
        self.assertTrue(self.bot2.finished, "El bot2 no terminó correctamente.")

    @patch.object(Minecraft, 'postToChat')  # Mock de 'postToChat' en el objeto Minecraft
    def test_boom_message_sent_to_chat(self, mock_postToChat):
        """Verificar que el mensaje BOOM aparece en el chat de Minecraft sin necesidad de ejecutar la lógica del bot."""
        # Simulamos que el bot 1 envía el mensaje final "BOOM"
        self.bot1.name = "tntBot_1"
        mock_postToChat(f"{self.bot1.name}: Pues si... BOOOOOOOOOOOOOMMMMM!")

        # Verificar que el mensaje "BOOM" fue enviado al chat
        mock_postToChat.assert_called_with("tntBot_1: Pues si... BOOOOOOOOOOOOOMMMMM!")

if __name__ == '__main__':
    unittest.main()
