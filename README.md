# TAP_MINECRAFT

## .github/workflows

- Primeramente, tengo un fichero `requirements.txt`, aquí tengo todos los programas que se deben instalar previamente, de tal forma el code coverage funcionara correctamente, ya que tendrá instalados los programas necesarios para poder procesar los tests.

- A continuación debemos configurar el `test.yml`, este fichero es la guía que va a seguir el Code coverage de GitHub por este motivo está en la raíz del repositorio y además tiene el nombre `.github`, en este fichero he configurado de forma secuencial todo lo que se tiene que instalar de tal forma que los test se puedan pasar de forma correcta, esta es la guía que va a seguir de ejecución:
  - Va a utilizar la misma versión de Python que yo tengo, 3.11.9.
  - Instalara las dependencias definidas en el fichero `requirements.txt`.
  - Ejecutara el servidor de Minecraft, con el comando `./StartServer &`(& para ejecutarse en segundo plano y que pueda seguir ejecutándose los demás test), se hace una espera de 20 segundos antes de pasar al próximo test de tal forma le da tiempo a ejecutarse de forma correcta.
  - Seguidamente, se ejecuta el servidor de nombres de Pyro4, con el comando `python -m Pyro4.naming`, se da un tiempo de 5 segundos para que le dé tiempo a ejecutarse.
  - A continuación se ejecuta el servidor de Pyro4, con el comando `python botServer.py`, se da un tiempo de 5 segundos para que le dé tiempo a ejecutarse
  - Ahora se empieza a ejecutar todos los test que tenemos dentro del directorio tests, estos ficheros deben de tener el prefijo de `test\_` para que el codecov pueda detectarlos, se le da 3 minutos para que termine de ejecutarse(en mi caso tarda un minuto y medio).
  - Seguidamente, se para todos los servidores.
  - Comprobamos que el test cubre todos los ficheros.
  - Por último se sube el resultado en Codecov y nos mostrará el % de éxito.

## Ejecutar el proyecto

Este proyecto se recomienda ejecutarlo desde la terminal de Visual Studio Code y utilizar la `Git bash`.

- Una vez que estemos en `Git bash`, vamos a la ruta `TAP_MINECRAFT/AdventuresInMinecraft-Linux-master`, y ejecutamos el `./StartServer.py` de tal forma podremos acceder a nuestro mundo local de Minecraft y podremos jugar y ejecutar el test general de code coverage.
- Seguidamente, abrimos otra dos terminales de `bash`, tal que podremos ejecutar el test general de codecov:
- Una para ejecutar Pyro4.naming `python -m Pyro4.naming`
- Una para ejecutar `botServer.py` para que se genere la URI y el test pueda conectarse de forma automática.

## Code coverage en local

- Para ejecutar el codecov en local, desde la ruta `TAP_MINECRAFT`, ejecutamos este comando:
  `pytest AdventuresInMinecraft-Linux-master/minecraft_agent_framework/tests/ --cov=AdventuresInMinecraft-Linux-master/minecraft_agent_framework --cov-report=xml`

- Si queremos ejecutar un comando más al detalle, tipo solamente de un test\_ en específico,
  primero nos ponemos en esta ruta: `cd TAP_MINECRAFT/AdventuresInMinecraft-Linux-master/minecraft_agent_framework/`
  podemos utilizar este comando: `pytest --cov=minecraft_agent_framework tests/test_ZombiBot.py`
