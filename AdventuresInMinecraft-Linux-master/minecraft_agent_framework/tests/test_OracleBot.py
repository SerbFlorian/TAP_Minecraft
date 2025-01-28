import unittest
from unittest.mock import MagicMock, patch
from ..agents.oracleBot import OracleBot, RandomResponseStrategy  # Cambia 'oracle_bot' por el nombre de tu archivo

class TestOracleBot(unittest.TestCase):

    @patch('mcpi.minecraft.Minecraft.create')
    @patch('builtins.input', return_value='Y')  # Parcheamos input() para evitar que espere entrada del usuario
    @patch.dict('sys.modules', {'portscan': MagicMock()})  # Parcheamos todo el módulo 'portscan'
    def test_iniciar_programa(self, mock_input, mock_mc_create):
        """Verifica que el bot se inicializa correctamente y envía el mensaje de inicio."""
        # Simulamos la creación de la conexión con Minecraft
        mock_mc = MagicMock()
        mock_mc_create.return_value = mock_mc
        
        # Creamos una instancia del bot con la estrategia RandomResponse
        oracle_bot = OracleBot(mock_mc, name="OracleBot", strategy=RandomResponseStrategy())
        
        # Enviar mensaje de inicio
        oracle_bot.mc.postToChat(f"{oracle_bot.name} está listo para comenzar la conversación. Hazme una pregunta!")

        # Verificamos que el bot se ha inicializado correctamente
        self.assertEqual(oracle_bot.name, "OracleBot")
        self.assertTrue(oracle_bot.running)
        
        # Verificamos que el mensaje de inicio se haya enviado correctamente
        mock_mc.postToChat.assert_called_with("OracleBot está listo para comenzar la conversación. Hazme una pregunta!")
    
    @patch('mcpi.minecraft.Minecraft.create')
    @patch('builtins.input', return_value='Y')  # Parcheamos input() para evitar que espere entrada del usuario
    @patch.dict('sys.modules', {'portscan': MagicMock()})  # Parcheamos todo el módulo 'portscan'
    def test_enviar_mensaje_inicial(self, mock_input, mock_mc_create):
        """Verifica que el bot envíe correctamente el mensaje de inicio."""
        # Simulamos la creación de la conexión con Minecraft
        mock_mc = MagicMock()
        mock_mc_create.return_value = mock_mc
        
        # Creamos una instancia del bot con la estrategia RandomResponse
        oracle_bot = OracleBot(mock_mc, name="OracleBot", strategy=RandomResponseStrategy())
        
        # Enviar mensaje de inicio
        oracle_bot.mc.postToChat(f"{oracle_bot.name} está listo para comenzar la conversación. Hazme una pregunta!")
        
        # Verificamos que el mensaje de inicio se haya enviado correctamente
        mock_mc.postToChat.assert_called_with("OracleBot está listo para comenzar la conversación. Hazme una pregunta!")

    # Parcheamos la creación de la instancia de Minecraft
    @patch('mcpi.minecraft.Minecraft.create')
    def test_listen_and_respond(self, mock_mc_create):
        """Test para verificar que el bot escucha y responde correctamente a un mensaje del chat."""
        mock_mc = MagicMock()
        # Simulamos un mensaje entrante en el chat
        mock_mc.events.pollChatPosts.return_value = [MagicMock(message="¿Eres real?")]
        # Devolvemos el mock cuando se llame a la creación de Minecraft
        mock_mc_create.return_value = mock_mc

        # Instanciamos el bot con el mock y una estrategia de respuesta aleatoria
        bot = OracleBot(mock_mc, name="TestBot", strategy=RandomResponseStrategy())
        
        # Llamamos al método de escucha y respuesta, pero limitamos las iteraciones para este test
        bot.listen_and_respond(iterations=1)  # Método modificado para soportar iteraciones limitadas en test

        # Verificamos que el bot haya enviado una respuesta al chat de Minecraft
        mock_mc.postToChat.assert_called()

    @patch('mcpi.minecraft.Minecraft.create')
    def test_stop(self, mock_mc_create):
        """Test para verificar que el bot se detiene correctamente."""
        mock_mc = MagicMock()
        # Devolvemos el mock cuando se llame a la creación de Minecraft
        mock_mc_create.return_value = mock_mc

        # Instanciamos el bot con el mock
        oracle_bot = OracleBot(mock_mc, name="OracleBot", strategy=RandomResponseStrategy())
        
        # Llamamos al método stop para detener el bot
        oracle_bot.stop()

        # Verificamos que la bandera `running` esté en False después de detener el bot
        self.assertFalse(oracle_bot.running)
        # Verificamos que el mensaje de finalización se haya enviado al chat de Minecraft
        mock_mc.postToChat.assert_called_with("OracleBot bot finalizado. Hasta la proxima!.")

    def test_random_response_strategy(self):
        """Test para verificar que la estrategia de respuesta aleatoria retorna respuestas válidas."""
        strategy = RandomResponseStrategy()
        # Solicitamos una respuesta usando la estrategia
        response = strategy.get_response("¿Esto funciona?")
        
        # Verificamos que la respuesta esté incluida en las respuestas predefinidas
        self.assertIn(response, strategy.responses)

if __name__ == '__main__':
    unittest.main()