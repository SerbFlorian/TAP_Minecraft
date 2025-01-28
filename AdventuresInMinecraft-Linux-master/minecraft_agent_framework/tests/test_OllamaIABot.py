import unittest
from unittest.mock import patch, MagicMock
import time  
from ..agents.ollamaIABot import MinecraftChatBot, OllamaResponseStrategy

# Espera activa para asegurar que el bot ha procesado los mensajes
def wait_for_responses(mock_mc, expected_responses, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if mock_mc.postToChat.call_count >= expected_responses:
            return True
        time.sleep(0.1)  
    return False

class TestMinecraftChatBot(unittest.TestCase):

    @patch('mcpi.minecraft.Minecraft.create')
    def test_iniciar_bot(self, mock_create):
        """Verifica que el bot se inicializa correctamente."""
        mock_mc = MagicMock()
        mock_create.return_value = mock_mc
        
        # Instanciamos el bot con la estrategia Ollama
        strategy = OllamaResponseStrategy('https://api-inference.huggingface.co/models/ollama/llama2', 'test_api_key')
        bot = MinecraftChatBot(strategy)
        
        # Verificamos que la conexión con Minecraft se haya establecido correctamente
        mock_mc.postToChat.assert_not_called() 

    @patch('mcpi.minecraft.Minecraft.create')
    def test_responder_mensajes(self, mock_create):
        """Verifica que el bot responde correctamente a un mensaje."""
        mock_mc = MagicMock()
        mock_create.return_value = mock_mc
        
        # Instanciamos el bot con la estrategia Ollama
        strategy = OllamaResponseStrategy('https://api-inference.huggingface.co/models/ollama/llama2', 'test_api_key')
        bot = MinecraftChatBot(strategy)

        # Simulamos un mensaje de pregunta
        mock_mc.events.pollChatPosts.return_value = [MagicMock(body='?How are you?')]  # El mensaje debe estar en inglés
        
        # Llamamos a la función que debería procesar el mensaje
        bot.listen_for_chat()

        # Esperamos a que el bot haya intentado enviar una respuesta
        self.assertTrue(wait_for_responses(mock_mc, 1))  
        
        # Verificamos que el bot haya intentado enviar una respuesta
        mock_mc.postToChat.assert_called_with('IA responde: Hubo un error al obtener la respuesta de la IA.') 

    @patch('mcpi.minecraft.Minecraft.create')
    def test_finalizar_programa_correctamente(self, mock_create):
        """Test que asegura que el programa se detiene correctamente después de procesar 3 mensajes."""
        mock_mc = MagicMock()
        mock_create.return_value = mock_mc
        
        # Instanciamos el bot con la estrategia Ollama
        strategy = OllamaResponseStrategy('https://api-inference.huggingface.co/models/ollama/llama2', 'test_api_key')
        bot = MinecraftChatBot(strategy)

        # Simulamos tres mensajes en el chat
        mock_mc.events.pollChatPosts.return_value = [
            MagicMock(body='?How are you?'),
            MagicMock(body='?What time is it?'),
            MagicMock(body='?What is love?')
        ]
        
        # Llamamos a la función que procesa los mensajes
        bot.listen_for_chat(max_messages=3)  # Límite de 3 mensajes

        # Verificamos que el bot haya intentado enviar tres respuestas
        self.assertTrue(wait_for_responses(mock_mc, 3))  # Esperar 3 respuestas
        
        # Verifica que se hayan enviado 3 mensajes
        self.assertEqual(mock_mc.postToChat.call_count, 3)

if __name__ == '__main__':
    unittest.main()
