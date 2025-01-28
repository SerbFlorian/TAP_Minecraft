from transformers import AutoModelForCausalLM, AutoTokenizer # type: ignore
import torch # type: ignore
from mcpi.minecraft import Minecraft
import requests # type: ignore
import time
import sys
import os
sys.path.append(os.path.abspath('../minecraft_agent_framework'))

# Conectar con el servidor de Minecraft (asumiendo que es local)
mc = Minecraft.create()

# URL de la API de Ollama en Hugging Face (modelo de IA)
ollama_url = 'https://api-inference.huggingface.co/models/ollama/llama2'  # Actualiza con el modelo correcto en Hugging Face
api_key = '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' 

class ResponseStrategy:
    """Interfaz para las estrategias de respuesta."""
    def get_response(self, message: str) -> str:
        """Método que obtiene la respuesta dada una entrada (mensaje)."""
        raise NotImplementedError

class OllamaResponseStrategy(ResponseStrategy):
    """Estrategia que utiliza Ollama (API de Hugging Face) para obtener respuestas."""
    
    def __init__(self, api_url: str, api_key: str):
        # Inicializa la URL de la API y la clave de la API
        self.api_url = api_url
        self.api_key = api_key

    def get_response(self, message: str) -> str:
        """Obtiene la respuesta de Ollama mediante una solicitud POST."""
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}  # Configuración de los encabezados con la clave API
            response = requests.post(self.api_url, json={"inputs": message}, headers=headers, timeout=10)  # Enviar la solicitud POST

            if response.status_code == 200:
                # Si la solicitud fue exitosa, devolvemos el texto generado por Ollama
                return response.json().get('generated_text', 'Lo siento, no pude obtener una respuesta.')
            else:
                return "Hubo un error al obtener la respuesta de la IA."
        except requests.exceptions.Timeout:
            return "La solicitud a Ollama excedió el tiempo de espera."
        except Exception as e:
            # Manejo de excepciones en caso de errores durante la solicitud
            print(f"Error al hacer la solicitud a Ollama: {e}")
            return "Error al comunicarse con la IA."

class DialoGPTResponseStrategy(ResponseStrategy):
    """Estrategia que utiliza DialoGPT (modelo local) para generar respuestas."""
    
    def __init__(self, model_name: str):
        # Cargar el modelo DialoGPT y el tokenizador
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.chat_history_ids = None  # Inicializar historial de conversación

    def get_response(self, message: str) -> str:
        """Genera una respuesta utilizando el modelo DialoGPT."""
        # Codificar la entrada del usuario y agregar el token de fin de oración
        new_user_input_ids = self.tokenizer.encode(message + self.tokenizer.eos_token, return_tensors='pt')

        # Crear la máscara de atención (1 para tokens válidos, 0 para padding)
        attention_mask = torch.ones(new_user_input_ids.shape, device=new_user_input_ids.device)

        # Añadir los nuevos tokens al historial de conversación
        if self.chat_history_ids is not None:
            bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1)
            attention_mask = torch.cat([attention_mask.new_zeros(self.chat_history_ids.shape), attention_mask], dim=-1)
        else:
            bot_input_ids = new_user_input_ids

        # Generar la respuesta con un límite de longitud de 1000 tokens en total
        self.chat_history_ids = self.model.generate(bot_input_ids, max_length=1000, attention_mask=attention_mask, pad_token_id=self.tokenizer.eos_token_id)

        # Decodificar la respuesta generada y convertirla a texto
        bot_response = self.tokenizer.decode(self.chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        
        # Limpiar el historial si es necesario para evitar desbordamientos de memoria
        if len(self.chat_history_ids[0]) > 1000:
            self.chat_history_ids = self.chat_history_ids[:, -1000:]

        return bot_response


# --- CLASE PRINCIPAL PARA ESCUCHAR LOS MENSAJES ---

class MinecraftChatBot:
    """Clase que escucha los mensajes del chat en Minecraft y responde con una estrategia definida."""
    
    def __init__(self, strategy: ResponseStrategy):
        # Inicializar el bot de Minecraft con una estrategia de respuesta
        self.strategy = strategy
        self.mc = Minecraft.create()  # Conectar con Minecraft

    def listen_for_chat(self, max_messages=3):
        """Escucha los mensajes en el chat y responde usando la estrategia."""
        message_count = 0  # Contador para mensajes procesados

        while message_count < max_messages:
            try:
                # Obtener los mensajes del chat de Minecraft
                messages = self.mc.events.pollChatPosts()

                for message in messages:
                    if message_count >= max_messages:
                        break  # Salir del bucle si hemos alcanzado el máximo de mensajes

                    # Imprimir el mensaje recibido en la consola
                    print(f"Mensaje recibido: {message}")

                    # Intentar acceder al texto del mensaje, ya sea como 'body' o 'text'
                    if hasattr(message, 'body'):
                        chat_message = message.body  # Si tiene 'body', acceder a él
                    elif hasattr(message, 'text'):
                        chat_message = message.text  # Si tiene 'text', acceder a él
                    else:
                        chat_message = str(message)  # Si no tiene ni 'body' ni 'text', imprimir todo el objeto
                    
                    # Verificar si el mensaje es una pregunta (empieza con '?')
                    if chat_message.startswith('?'):
                        question = chat_message[1:].strip()  # Eliminar el "?" al principio
                        print(f"Pregunta recibida: {question}")
                        # Obtener la respuesta usando la estrategia definida
                        response = self.strategy.get_response(question)
                        # Enviar la respuesta al chat de Minecraft
                        self.mc.postToChat(f"IA responde: {response}")
                    elif chat_message and not chat_message.startswith('?'):
                        # Si no es una pregunta, generar una respuesta normal
                        response = self.strategy.get_response(chat_message)
                        self.mc.postToChat(f"iaBot: {response}")
                    
                    message_count += 1  # Incrementar el contador de mensajes procesados

            except Exception as e:
                # Manejo de errores durante la escucha del chat
                print(f"Error al obtener los mensajes del chat: {e}")

            time.sleep(1)  # Esperar 1 segundo antes de revisar el chat nuevamente

# --- EJECUCIÓN PRINCIPAL ---

if __name__ == "__main__":
    try:
        print("Presiona Ctrl+C para detener el programa...")
        # Selecciona la estrategia de respuesta
        dialoGPT_strategy = DialoGPTResponseStrategy("microsoft/DialoGPT-medium")
        
        # Crear una instancia del chatbot usando una estrategia específica
        chat_bot = MinecraftChatBot(dialoGPT_strategy) 
        
        # Iniciar el proceso de escuchar el chat
        chat_bot.listen_for_chat()

    except KeyboardInterrupt:
        # Este bloque captura la interrupción del teclado (Ctrl+C) y permite cerrar el programa limpiamente
        print("\nPrograma detenido por el usuario. Saliendo...")
