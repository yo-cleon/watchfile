#!/usr/bin/python

import configparser
import sys
import telebot
import time
from bin.watchfile import configuracion
from bin.watchfile import fc

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
print("Inicio del envio del fichero: ", archivo)
if primerEnvio.upper() == 'SI':
    configuracion.set('GENERAL', 'PrimerEnvio', 'NO')
    with open(fc, 'w+') as archivoConfig:
        configuracion.write(archivoConfig)
    horaEnvio = round(time.time())
    with open("reg.txt", "w") as registro:
        registro.write(str(horaEnvio))
    env_archivo(archivo)
    print("Mensaje enviado")
else:
    with open("reg.txt") as registro:
        linea = registro.readline()
        if len(linea) > 0:
            ultimoEnvio = int(linea)
        else:
            ultimoEnvio = 0
    actualEnvio = round(time.time())
    tiempo = actualEnvio - ultimoEnvio
    print("diferencia con el último envio: ", tiempo)
    if tiempo > 25:
        with open("reg.txt", "w") as registro:
            registro.write(str(actualEnvio))
        env_archivo(archivo)
    else:
        print("no ha pasado tiempo suficiente")
