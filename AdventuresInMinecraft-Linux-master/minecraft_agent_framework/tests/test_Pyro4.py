import unittest
import Pyro4

class TestBotControl(unittest.TestCase):
    """Clase de pruebas unitarias para comprobar la interacción con el servidor Pyro4 y la clase BotControl."""

    def setUp(self):
        """Configuración antes de cada test."""
        # Conectarse al servidor de nombres de Pyro4 y obtener la URI del objeto remoto
        try:
            self.ns = Pyro4.locateNS()  # Localiza el servidor de nombres
            self.uri = self.ns.lookup("BotControl")  # Busca el nombre registrado para obtener la URI
        except Pyro4.errors.PyroError as e:
            self.fail(f"Error al obtener la URI desde el servidor de nombres: {e}")

    def test_connection(self):
        """Probar que la conexión con el servidor Pyro4 está activa y el objeto BotControl responde."""
        try:
            # Obtener el proxy del servidor BotControl usando la URI dinámica
            bot_control = Pyro4.Proxy(self.uri)
            
            # Verificamos si el objeto responde al método 'hello'
            response = bot_control.hello()
            self.assertEqual(response, "Hola desde el servidor de BotControl!")  

        except Pyro4.errors.CommunicationError as e:
            # Si ocurre un error de comunicación con el servidor, se falla la prueba
            self.fail(f"Error de comunicación con el servidor: {e}")
        except Exception as e:
            # Capturamos cualquier otro error inesperado
            self.fail(f"Ocurrió un error inesperado al conectar: {e}")

    def test_build(self):
        """Probar que el comando 'build' funciona correctamente."""
        try:
            # Obtener el proxy del servidor BotControl usando la URI dinámica
            bot_control = Pyro4.Proxy(self.uri)
            
            # Llamamos al método 'build'
            response = bot_control.build()
            print(f"Respuesta del servidor build: {response}")  # Imprimir la respuesta del servidor
            # Comprobamos que la respuesta del servidor sea la esperada
            self.assertEqual(response, "Construccion realizada.") 

        except Exception as e:
            # Si ocurre cualquier error al ejecutar el comando, la prueba falla
            self.fail(f"Error al ejecutar el comando build: {e}")

    def test_destroy(self):
        """Probar que el comando 'destroy' funciona correctamente."""
        try:
            # Obtener el proxy del servidor BotControl usando la URI dinámica
            bot_control = Pyro4.Proxy(self.uri)
            
            # Llamamos al método 'destroy'
            response = bot_control.destroy()
            print(f"Respuesta del servidor destroy: {response}")  # Imprimir la respuesta del servidor
            # Comprobamos que la respuesta del servidor sea la esperada
            self.assertEqual(response, "Destruccion realizada.") 

        except Exception as e:
            # Si ocurre cualquier error al ejecutar el comando, la prueba falla
            self.fail(f"Error al ejecutar el comando destroy: {e}")

    def test_send_chat_message(self):
        """Probar el envío de un mensaje personalizado al chat de Minecraft."""
        test_message = "Mensaje de prueba desde el cliente"
        try:
            # Obtener el proxy del servidor BotControl usando la URI dinámica
            bot_control = Pyro4.Proxy(self.uri)
            
            # Llamamos al método 'send_chat_message' con un mensaje personalizado
            response = bot_control.send_chat_message(test_message)
            
            # Comprobamos que la respuesta del servidor sea la esperada
            self.assertEqual(response, f"Mensaje enviado: {test_message}")  

        except Exception as e:
            # Si ocurre cualquier error al ejecutar el comando, la prueba falla
            self.fail(f"Error al ejecutar el comando send_chat_message: {e}")

    def tearDown(self):
        """Limpieza después de cada test (no es necesario aquí, pero útil si hay algo que limpiar)."""
        pass

if __name__ == '__main__':
    # Ejecutar los tests
    unittest.main()
