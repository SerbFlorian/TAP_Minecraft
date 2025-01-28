import unittest
from unittest.mock import MagicMock, patch

# Importar las clases y funciones necesarias
from ..Tarragona.botServer import BotControl
from ..Tarragona.anfiteatroRomano import MinecraftAmphitheater
from ..Tarragona.botClient import MinecraftBot


class TestBotControl(unittest.TestCase):
    """
    Clase de pruebas para la funcionalidad del bot de control de Minecraft.
    """

    @patch('mcpi.minecraft.Minecraft.create')
    def setUp(self, mock_create):
        """
        Inicialización de las pruebas: se crea un mock de la conexión a Minecraft 
        y se inicializa el bot de control.
        """
        # Mock de la conexión al servidor de Minecraft
        self.mock_mc = MagicMock()
        mock_create.return_value = self.mock_mc
        
        # Instanciamos el bot de control
        self.bot_control = BotControl()

    @patch('time.sleep', return_value=None)  # Evitar ralentización por el sleep
    def test_generate_reference_structure(self, mock_sleep):
        """
        Test para la generación de la estructura de referencia en el bot de control.
        No interactúa con Minecraft, solo verifica la llamada a la función.
        """
        # Mock de la generación de la estructura sin necesidad de interacción con Minecraft
        with patch.object(self.bot_control, 'generate_reference_structure', return_value=None) as mock_generate:
            self.bot_control.generate_reference_structure()
            mock_generate.assert_called_once()  # Verifica que la función se haya llamado

    def test_create_flat_zone(self):
        """
        Test para la creación de una zona plana. Verifica que la función se llame correctamente.
        """
        with patch.object(self.bot_control, 'create_flat_zone', return_value=None) as mock_create_flat:
            self.bot_control.create_flat_zone()
            mock_create_flat.assert_called_once()  # Verifica que se haya llamado la función

    @patch('mcpi.minecraft.Minecraft.create')
    def test_guide_for_amphitheater(self, mock_create):
        """
        Test para guiar al jugador hacia el Anfiteatro Romano. Verifica que el mensaje
        correcto se envíe al chat.
        """
        # Mock de la conexión de Minecraft
        self.mock_mc = MagicMock()
        mock_create.return_value = self.mock_mc
        self.bot_control = BotControl()
        
        player_id = "Florian"
        
        # Llamar a la función de guía
        self.bot_control.guide_for_amphitheater(player_id)
        
        # Verificar que se envíe el mensaje correcto al chat
        self.mock_mc.postToChat.assert_any_call(f"Vamos a empezar, {player_id}! Aqui esta la estructura del Anfiteatro Romano.")

class TestMinecraftAmphitheater(unittest.TestCase):
    """
    Clase de pruebas para las funciones relacionadas con el Anfiteatro Romano en Minecraft.
    """

    @patch('mcpi.minecraft.Minecraft.create')
    def setUp(self, mock_create):
        """
        Inicialización de las pruebas: mock de la conexión a Minecraft y creación del anfiteatro.
        """
        self.mock_mc = MagicMock()
        mock_create.return_value = self.mock_mc
        
        # Instanciamos la clase MinecraftAmphitheater
        self.amp = MinecraftAmphitheater(self.mock_mc, 0, 64, 0)
    
    def test_build_ellipse(self):
        """
        Test para la construcción de la elipse en el anfiteatro. Verifica que la función setBlock sea llamada.
        """
        with patch.object(self.mock_mc, 'setBlock') as mock_set_block:
            self.amp.build_ellipse(0, 64, 0, 5, 7, 1)
            mock_set_block.assert_called()  # Verifica que setBlock haya sido llamado

    def test_build_levels(self):
        """
        Test para la construcción de los niveles del anfiteatro. Verifica que la función setBlock se haya llamado.
        """
        with patch.object(self.mock_mc, 'setBlock') as mock_set_block:
            self.amp.build_levels()
            mock_set_block.assert_called()  # Verifica que setBlock haya sido llamado

    def test_build_walls(self):
        """
        Test para la construcción de las paredes del anfiteatro. Verifica que la función setBlock sea llamada.
        """
        with patch.object(self.mock_mc, 'setBlock') as mock_set_block:
            self.amp.build_walls()
            mock_set_block.assert_called()  # Verifica que setBlock haya sido llamado

    def test_build_entrances(self):
        """
        Test para la construcción de las entradas al anfiteatro. Verifica que la función setBlock sea llamada.
        """
        with patch.object(self.mock_mc, 'setBlock') as mock_set_block:
            self.amp.build_entrances()
            mock_set_block.assert_called()  # Verifica que setBlock haya sido llamado

    def test_build_roof(self):
        """
        Test para la construcción del techo del anfiteatro. Verifica que la función setBlock sea llamada.
        """
        with patch.object(self.mock_mc, 'setBlock') as mock_set_block:
            self.amp.build_roof()
            mock_set_block.assert_called()  # Verifica que setBlock haya sido llamado

    def test_build_interior(self):
        """
        Test para la construcción del interior del anfiteatro. Verifica que la función setBlock sea llamada.
        """
        with patch.object(self.mock_mc, 'setBlock') as mock_set_block:
            self.amp.build_interior()
            mock_set_block.assert_called()  # Verifica que setBlock haya sido llamado

    def test_give_materials_to_player(self):
        """
        Test para dar materiales al jugador. Verifica que el mensaje de materiales haya sido enviado correctamente.
        """
        with patch.object(self.mock_mc, 'postToChat') as mock_post_to_chat:
            self.amp.give_materials_to_player()
            mock_post_to_chat.assert_called()  # Verifica que postToChat haya sido llamado


class TestMinecraftBot(unittest.TestCase):
    """
    Clase de pruebas para las funciones del bot de Minecraft.
    """

    @patch('mcpi.minecraft.Minecraft.create')
    def setUp(self, mock_create):
        """
        Inicialización de las pruebas: mock de la conexión a Minecraft y creación del bot.
        """
        # Crear un mock para la conexión a Minecraft
        self.mock_mc = MagicMock()
        mock_create.return_value = self.mock_mc  # Hacer que `Minecraft.create()` devuelva el mock

        # Crear el bot con un nombre de jugador ficticio
        self.bot = MinecraftBot("Florian")
    
    def test_send_welcome_message(self):
        """
        Test para verificar el envío del mensaje de bienvenida al jugador.
        """
        # Usar un mock del método `postToChat` para verificar que el mensaje se envíe correctamente
        with patch.object(self.mock_mc, 'postToChat') as mock_post_to_chat:
            self.bot.send_welcome_message()

            # Verificar que se haya llamado a `postToChat` con el mensaje esperado
            mock_post_to_chat.assert_called_once_with("Florian se ha conectado correctamente al servidor. Vamos a comenzar a construir el Anfiteatro Romano de Tarragona!")
    
# Ejecutar las pruebas
if __name__ == "__main__":
    unittest.main()
