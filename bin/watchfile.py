#!/usr/bin/python
# -*- coding: utf-8 -*-

# Script original de http://brunorocha.org/python/watching-a-directory-for-file-changes-with-python.html

import os
import time
import configparser
import subprocess
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from utils import mylogger

fc = "./config.ini"
logger = mylogger.getLogger()

# CREACION ARCHIVO CONFIGURACION DE LA APLIACIÓN SI NO EXISTE
if not os.path.exists(fc):
    try:
        subprocess.call('python creaConfig.py')
    except subprocess.CalledProcessError as e:
        # print("Ha habido un error al crear el archivo de configuración: \n", e.output)
        logger.error("Error al crear el archivo de configuración: ", e.output)

# LEER ARCHIVO DE CONFIGURACIÓN PARA LOCALIZAR EL DIRECTORIO A MONITORIZAR
configuracion = configparser.ConfigParser()
configuracion.read(fc)
confGeneral = configuracion['GENERAL']
dir = confGeneral['Directorio']
tipoEnvio = confGeneral['TipoEnvio']

# VERIFICAR EXISTENCIA ARCHIVO AUXILIAR DE REGISTRO
if not os.path.isfile("reg.txt"):
    f = open("reg.txt", "w")


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.pdf", "*.xls", "*.xlsx"]

    # def process(self, event):
    # 	"""
    # 	event.event_type
    # 	'modified' | 'created' | 'moved' | 'deleted'
    # 	event.is_directory
    # 	True | False
    # 	event.src_path
    # 	path/to/observed/file
    # 	"""
    # 	# the file will be processed there
    # 	print (event.src_path, event.event_type)  print now only for debug

    def on_modified(self, event):
        # self.process(event)
        archivo = event.src_path
        # print("Se ha modificado el archivo: ", archivo)
        logger.warning("Archivo modificado: %s", archivo)
        configuracion.set('GENERAL', 'Fichero', archivo)
        with open(fc, 'w+') as archivoConfig:
            configuracion.write(archivoConfig)
        if tipoEnvio == 'T':
            result = subprocess.call('python enviaTelegram.py')
            if result == 0:
                # print("Script ejecutado")
                logger.info("Enviado archivo correctamente por Telegram.")
            else:
                # print("problemas con el script")
                logger.error("Error al enviar el archivo por Telegram: ", result)
        elif tipoEnvio == 'F':
            result = subprocess.call('python enviaFtp.py')
            if result == 0:
                # print("Script ejecutado")
                logger.info("Subido archivo mediante FTP correctamente.")
            else:
                # print("problemas con el script")
                logger.error("Error al subir archivo mediante FTP: ", result)
        # print("archivo modificado: ", event)

    def on_created(self, event):
        # self.process(event)
        archivo = event.src_path
        # print("Se ha creado el archivo: ", archivo)
        logger.warning("Archivo creado: ", archivo)
        configuracion.set('GENERAL', 'Fichero', archivo)
        with open(fc, 'w+') as archivoConfig:
            configuracion.write(archivoConfig)
        if tipoEnvio.upper == 'T':
            result = subprocess.call('python enviaTelegram.py')
            if result == 0:
                # print("Script ejecutado")
                logger.info("Finalizado proceso de envío.")
            else:
                # print("problemas con el script")
                logger.error("Error al enviar el archivo por Telegram: ", result)
        elif tipoEnvio.upper == 'F':
            result = subprocess.call('python enviaFtp.py')
            if result == 0:
                # print("Script ejecutado")
                logger.info("Finalizado proceso de envío.")
            else:
                # print("problemas con el script")
                logger.error("Error al subir archivo mediante FTP: ", result)


if __name__ == '__main__':
    # args = sys.argv[1:]
    observer = Observer()
    # observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.schedule(MyHandler(), dir)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    # print("Script finalizado.")
    logger.info("Se ha detenido manualmente la ejecución de watchfile.py")

    observer.join()
