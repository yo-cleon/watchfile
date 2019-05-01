#!/usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import sys
import telebot
import time
from watchfile import configuracion
from watchfile import fc
from utils import mylogger

logger = mylogger.getLogger()

# DATOS DEL FICHERO DE CONFIGURACION
config = configuracion['GENERAL']
primerEnvio = config['PrimerEnvio']
archivo = config['fichero']
parametros = configuracion['TELEGRAM']
Token = parametros['Token']
groupId = parametros['Id']

# Combinamos la declaración del Token con la función de la API
tb = telebot.TeleBot(Token)


# ENVIO DEL MENSAJE
def env_archivo(f):
    tb.send_message(groupId, "Actualizado cuadre")
    doc = open(f, 'rb')
    tb.send_document(groupId, doc)


# PROCESO DE ENVIO DEL ARCHIVO
# print("Inicio del envio del fichero: ", archivo)
logger.info("enviaTelegram: inicio del proceso de envío por Telegram del archivo: %s", archivo)
if primerEnvio.upper() == 'SI':
    configuracion.set('GENERAL', 'PrimerEnvio', 'NO')
    with open(fc, 'w+') as archivoConfig:
        configuracion.write(archivoConfig)
    horaEnvio = round(time.time())
    with open("reg.txt", "w") as registro:
        registro.write(str(horaEnvio))
    env_archivo(archivo)
    # print("Mensaje enviado")
    logger.info("enviaTelegram: Primer envío. Archivo enviado correctamente.")
else:
    with open("reg.txt") as registro:
        linea = registro.readline()
        if len(linea) > 0:
            ultimoEnvio = int(linea)
        else:
            ultimoEnvio = 0
    actualEnvio = round(time.time())
    difTiempo = actualEnvio - ultimoEnvio
    # print("diferencia con el último envio: ", tiempo)
    logger.info("enviaTelegram: Diferencia de tiempo con el último envío: %s", difTiempo)
    if difTiempo > 25:
        with open("reg.txt", "w") as registro:
            registro.write(str(actualEnvio))
        env_archivo(archivo)
        logger.info("enviaTelegram: Archivo subido correctamente.")
    else:
        # print("no ha pasado tiempo suficiente")
        logger.warning("enviaTelegram: no ha pasado tiempo suficiente entre envíos. Envío anulado.")
