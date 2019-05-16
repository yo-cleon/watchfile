# Watchfile

Aplicación para monitorizar la creación o modificación de archivos en un
determinado directorio.

## Requerimientos:
+ Python 3.7
+ Watchdog: https://github.com/gorakhargosh/watchdog
+ pyTelegramBotAPI: https://github.com/eternnoir/pyTelegramBotAPI

## Uso:
Clonar o descargar el proyecto: `git clone https://github.com/yo-cleon/watchfile`

Ejecutar de forma manual por primera vez el script con el comando:
<pre><code>python watchfyle.py</code></pre>

Este paso es necesario para que se cree el archivo de configuración. Durante su creación,
deberemos indicar el directorio a monitorizar, el tipo de envío del aviso y del archivo 
a utilizar y los parámetros requeridos para el envío.

## Mejoras:
- [x] Añadir logs en los scrpts para revisar funcionamiento y problemas.
- [ ] Permitir encriptado de información en el archivo de configuracion
