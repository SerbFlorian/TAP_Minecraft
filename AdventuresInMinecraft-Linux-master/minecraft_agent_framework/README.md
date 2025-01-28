# Minecraft Agent Framework

En este framework he implementado un entorno de desarrollo con Python diseñado para facilitar la creación, implementación y gestión de agentes automatizados que interactúan con el servidor Minecraft. Este framework nos permite crear agentes que pueden realizar una variedad de acciones en el chat de Minecraft.</br>
También tenemos la opción de interactuar de forma remota con el chat de Minecraft, gracias a Pyro4.</br>
Seguidamente, tenemos una actividad educativa con el Anfiteatro Romano de Tarragona, en el que los usuarios que se conecten tienen el reto de replicar la construcción del anfiteatro Romano, mientras que en el chat se explica un poco de la historia del Anfiteatro.</br>
A todo esto, todas las implementaciones están cubiertas por tests unitarios, que cubren completamente el código.

---

## Estructura del proyecto

- Agents
  - Insult Bot
  - Ollama IA Bot
  - Oracle Bot
  - Tnt Bot
  - Zombi Bot
- Pyro4
  - Bot Server
  - Bot Client
- Tarragona
  - Anfiteatro Romano
  - Bot Server
  - Bot Client
- Tests
  - Test Insult Bot
  - Test Ollama IA Bot
  - Test Oracle Bot
  - Test Pyro4
  - Test Tarragona
  - Test Tnt Bot
  - Test Zombi Bot

---

### Agents

En la implementación de estos agentes se ha utilizado patrones de diseño, en mi caso los patrones de diseño que más se ajustaban a lo que quería implementar son: `Command, Strategy y Observer`.</br>
Como he comentado anteriormente, tenemos una seria de agentes que interactúan con el mundo de Minecraft, veamos qué tipo de agentes tenemos:</br>
_*los ficheros .json son necesarios para los agentes, ya que adquieren módulos de patrones de diseño*_

> Previamente debemos ejecutar el `./StartServer` que esta en la ruta `TAP_MINECRAFT/AdventuresInMinecraft-Linux-master`</br>

#### Insult Bot

Este agent, genera tres bots a nuestro alrededor(en el chat) y estos se están insultando entre sí, haciendo el efecto que estos usuarios se están insultando cerca de nosotros, si ejecutamos el insultBot.py y vamos al mundo de Minecraft, podremos ver como aparecen mensajes de insultos que se están enviando estos bots, estos bots están limitados en enviar 10 insultos cada uno, cuando estos terminen de mandar los 10 insultos este finaliza automáticamente. El usuario que se conecta al mundo de Minecraft, en este caso no debe enviar ningún mensaje, ya que estos bots envían insultos de una lista predefinida, adquieren los insultos de ahí y de forma aleatoria se mandan los mensajes en el chat(al ser un random, está claro que estos mensajes se pueden repetir).

> Passos para ejecutar `insultBot.py`</br>
> Primeramente nos debemos ubicar en la ruta de `TAP_MINECRAFT/AdventuresInMinecraft-Linux-master/minecraft_agent_framework/agents`</br>
> Seguidamente podemos ejecutar el fichero de la siguiente forma: `python insultBot.py`</br>

#### Ollama IA Bot

En este agent, el usuario que se ha conectado al mundo de Minecraft, estará interactuando con una IA mediante el chat, de tal forma que el usuario puede añadir mensajes en el chat y le estará respondiendo una IA de la API Ollama(mensajes en el chat en Inglés). Está limitado a tres mensajes para realizar pruebas, si se quiere se modifica esta sección del código: `def listen_for_chat(self, max_messages=3):` se cambia el 3 por X número de interacciones.

> Pasos para ejecutar `ollamaIABot.py`</br>
> Primeramente nos debemos ubicar en la ruta de `TAP_MINECRAFT/AdventuresInMinecraft-Linux-master/minecraft_agent_framework/agents`</br>
> Seguidamente podemos ejecutar el fichero de la siguiente forma: `python ollamaIABot.py`</br>

#### Oracle Bot

Este agent, responde todo lo que le escriba en el chat el usuario, este a contraparte del OllamaIABot, este tiene una lista de frases predefinida y responde de forma aleatoria, tal que, independientemente de lo que escriba el usuario este bot va a mostrar un mensaje aleatorio de la lista predefinida. Si el usuario ya no quiere interactuar con este bot, puede finalizar haciendo un `ctrl+c` y sé para el bot.

> Pasos para ejecutar `oracleBot.py`</br>
> Primeramente nos debemos ubicar en la ruta de `TAP_MINECRAFT/AdventuresInMinecraft-Linux-master/minecraft_agent_framework/agents`</br>
> Seguidamente podemos ejecutar el fichero de la siguiente forma: `python oracleBot.py`</br>

#### Tnt Bot

Este agent, el usuario está jugando en el mundo de Minecraft y de repente se acerca un bot con un TNT en las manos, este usuario tiene 5 segundos para matar al bot o para correr y que no explote a su lado(ya que lo mataría), en este caso lo tenemos todo dentro del chat y tenemos dos bots con TNT en las manos, entonces en este caso el usuario puede ver como aparecen los mensajes de los bots por el chat y como va disminuyendo la cuenta regresiva y finalmente explota.(es un poco trol, ya que no explota inmediatamente, y produce un poco de intriga en el jugador)

> Pasos para ejecutar `tntBot.py`</br>
> Primeramente nos debemos ubicar en la ruta de `TAP_MINECRAFT/AdventuresInMinecraft-Linux-master/minecraft_agent_framework/agents`</br>
> Seguidamente podemos ejecutar el fichero de la siguiente forma: `python tntBot.py`</br>

#### Zombi Bot

Este agent, en este caso tenemos un agente que es un zombi, este es un poco diferente a los demás, el zombi va a estar respondiendo a cualquier pregunta del usuario, en este caso el zombi solamente va a responder con Yes o No(de forma aleatoria, 50% yes, 50% no), si el usuario introduce algún insulto de la lista este bot le pedirá que no le insulte, si el usuario no hace caso y sigue insultando, al tercer insulto este bot detonará un TNT que se sacó del bolsillo y este usuario va a tener 5 segundos para disculparse con el bot, pero finalmente va a morir a causa de la explosión. Este bot se puede interrumpir la ejecución con la combinación de teclas `ctrl+c`.

> Pasos para ejecutar `zombiBot.py`</br>
> Primeramente nos debemos ubicar en la ruta de `TAP_MINECRAFT/AdventuresInMinecraft-Linux-master/minecraft_agent_framework/agents`</br>
> Seguidamente podemos ejecutar el fichero de la siguiente forma: `python zombiBot.py`</br>

---

### Pyro4

Pyro4 es una biblioteca de Python que facilita la creación de sistemas distribuidos, permitiendo que objetos en diferentes máquinas (o procesos) se comuniquen de manera remota. Entonces en mi framework he utilizado Pyro4, para que se puedan conectar usuarios de otros ordenadores a mi mundo de Minecraft, de tal forma puedan interactuar y jugar en mi mundo, cuando el cliente se conecte a mi servidor, en el chat de Minecraft vamos a recibir unos mensajes un poco diferentes para identificar que se ha conectado un usuario externo. Todo esto en pyro es posible con la URI, esta es un clave que genera el botServer y que nos da acceso para poder conectarnos al servidor local.</br>
Primeramente debemos ejecutar el servidor de Minecraft obvio y luego los servidores de naming y de pyro4 para poder interactuar luego con el cliente y con el test.

> Pasos para ejecutar `zombiBot.py`</br>
> Previamente debemos ejecutar el `./StartServer` que está en la ruta `TAP_MINECRAFT/AdventuresInMinecraft-Linux-master`</br>
> Primeramente nos debemos ubicar en la ruta de `TAP_MINECRAFT/AdventuresInMinecraft-Linux-master/minecraft_agent_framework/Pyro4`</br>
> Ejecutamos el servidor de nombres de pyro4: `python -m Pyro4.naming`</br>
> En otra terminal:</br>
> Ejecutamos el fichero del servidor: `python botServer.py`</br>

#### Bot Server

El `botServer.py`, debemos ejecutar el servidor de nombres y el servidor que genera la URI, de tal forma cualquier usuario que conozca el nombre del servidor y la URI podrán conectarse a mi mundo de Minecraft.(la URI es una clave de acceso para poder acceder al servidor de nombres y este nos da acceso directo al servidor de Minecraft local)</br>
En botServer he implementado reflexión(reflexión en Python se refiere a la capacidad de inspeccionar y modificar el comportamiento de los objetos en tiempo de ejecución), de tal forma que, aplico indirectamente a través de la ejecución dinámica de acciones basadas en el nombre de la acción proporcionada (el parámetro action_name), de esta manera estoy permitiendo que el código maneje diferentes comportamientos de forma dinámica en función del nombre de la acción.

> Pasos para ejecutar `botServer.py`</br>
> Ejecutamos el fichero del servidor: `python botServer.py`</br>
> En ejecutar botServer, nos generará un URI, esta la tenemos que añadir en el cliente, en esta parte del código: `uri = "PYRO:obj_b1b0f20e0f254855b197b9b23bc1e79a@localhost:51182"`

#### Bot Client

El `botClient.py`, debe añadir la URI generada por botServer, y una vez ya tiene la clave de acceso podremos acceder al servidor local de Minecraft y una vez dentro veremos que los mensajes que ha enviado el usuario remoto, los veremos que se han recibido correctamente.(de la misma forma pasaría, si se estuviera conectando una persona a mi servidor local)

> Pasos para ejecutar `zombiBot.py`</br>
> Primeramente nos debemos ubicar en la ruta de `TAP_MINECRAFT/AdventuresInMinecraft-Linux-master/minecraft_agent_framework/Pyro4`</br>
> Seguidamente podemos ejecutar el fichero de la siguiente forma: `python botClient.py`</br>

---

### Tarragona

En esta sección, se ha implementado un ejercicio educativo, de tal forma este ejercicio se pueda dar en escuelas de secundaria y los jóvenes/niños puedan jugar y aprender un poco de historia del Anfiteatro Romano de Tarragona.</br>
El funcionamiento de este mini proyectos es tal que así:

- Seguidamente, generaremos el anfiteatro y los jugadores deberán replicarlo, previamente de la ejecución debemos configurar las coordenadas de donde queremos generar el anfiteatro, ahora ejecutaremos el `anfiteatroRomano.py`.
- Seguidamente, tenemos el botServer, en el que este mostrara una breve introducción a los jugadores de la historia del anfiteatro, seguidamente les indicara a los jugadores que ya pueden empezar a replicarlo, y cada 5 minutos(actualmente está en 1 segundo por los tests) se mostrara una curiosidad del anfiteatro, una curiosidad de historia, de cultura de esta estructura. Para ejecutar el botServer hacemos `botServer.py`.
- Por último ejecutamos al botClient, en el que previamente nos pedirá el nombre del usuario y justo después se conectara al servidor, una vez conectado, este usuario puede leer los mensajes y empezar a jugar, mientras el usuario está leyendo los mensajes del chat, se le depositara los materiales necesarios en el inventario para que este pueda construir en Anfiteatro Romano. Para ejecutar el botClient hacemos `botClient.py`.

#### Anfiteatro Romano

A continuación generamos toda la estructura de ejemplo que deben seguir los jugadores(una imagen vale más que mil palabras), de tal forma pueden investigar la estructura y empezar a jugar.

> Pasos para ejecutar `anfiteatroRomano.py`</br>
> Primeramente nos debemos ubicar en la ruta de `TAP_MINECRAFT/AdventuresInMinecraft-Linux-master/minecraft_agent_framework/Tarragona`</br>
> Seguidamente podemos ejecutar el fichero de la siguiente forma: `python anfiteatroRomano.py`</br>

#### Bot Server

En el server, inicialmente mostraremos un mensaje introductorio, seguidamente cada 5 minutos mostraremos una curiosidad y le indicamos al usuario que ya puede empezar a construir y de mientras construye le va apareciendo mensajes por el chat de curiosidades.

> Pasos para ejecutar `botServer.py`</br>
> Primeramente nos debemos ubicar en la ruta de `TAP_MINECRAFT/AdventuresInMinecraft-Linux-master/minecraft_agent_framework/Tarragona`</br>
> Seguidamente podemos ejecutar el fichero de la siguiente forma: `python botServer.py`</br>

#### Bot Client

El cliente introduce el nombre del usuario que va a construir el anfiteatro y le conecta al servidor.(muestra un mensaje conforme se ha conectado)

> Pasos para ejecutar `botClient.py`</br>
> Primeramente nos debemos ubicar en la ruta de `TAP_MINECRAFT/AdventuresInMinecraft-Linux-master/minecraft_agent_framework/Tarragona`</br>
> Seguidamente podemos ejecutar el fichero de la siguiente forma: `python botClient.py`</br>

---

### Tests

En esta sección, tenemos todos los test, que cubren todo el framework.

#### Test Insult Bot

Secciones de código que cubre él `test_InsultBot.py`:

- test_insult_bot_starts_insulting
- test_stop_insulting_command
- test_insult_command_starts_insulting
- test_set_command

#### Test Ollama IA Bot

Secciones de código que cubre él `test_OllamaIABot.py`:

- test_iniciar_bot
- test_responder_mensajes
- test_finalizar_programa_correctamente

#### Test Oracle Bot

Secciones de código que cubre él `test_OracleBot.py`:

- test_iniciar_programa
- test_enviar_mensaje_inicial
- test_listen_and_respond
- test_stop
- test_random_response_strategy

#### Test Pyro4

Secciones de código que cubre él `test_Pyro4.py`:

- test_connection
- test_build
- test_destroy
- test_send_chat_message

#### Test Tarragona

Secciones de código que cubre él `test_Tarragona.py`:

- test_generate_reference_structure
- test_create_flat_zone
- test_guide_for_amphitheater
- test_build_ellipse
- test_build_levels
- test_build_walls
- test_build_entrances
- test_build_roof
- test_build_interior
- test_give_materials_to_player
- test_send_welcome_message

#### Test Tnt Bot

Secciones de código que cubre él `test_TntBot.py`:

- test_bot_initialization
- test_bots_finish_execution
- test_boom_message_sent_to_chat

#### Test Zombi Bot

Secciones de código que cubre él `test_ZombiBot.py`:

- test_handle_message_normal
- test_activate_tnt_with_insults
