#!/usr/bin/python

import configparser
import sys
import telebot
import time
from watchfile import configuracion

#DATOS DEL FICHERO DE CONFIGURACION
parametros = configuracion['PARAMETROS']
primerEnvio = parametros['PrimerEnvio']
archivo = parametros['fichero']
print("Inicio del envio del fichero: ",archivo)

# CONFIGURACIÓN DEL BOT
# Indicar el Token generado con el @BotFather
TOKEN = '839692217:AAEQGp5SRG5jRXyemf4pEf5RAqd-5GmhKiM' 
# Combinamos la declaración del Token con la función de la API
tb = telebot.TeleBot(TOKEN)

#ENVIO DEL MENSAJE
def env_archivo(f):
	tb.send_message('-365936829', "Actualizado cuadre")
	doc = open(f, 'rb')
	tb.send_document('-365936829', doc)

#ANALIZAR SI HAY QUE REALIZAR EL ENVIO
if (primerEnvio.upper() == 'SI'):
	configuracion.set('PARAMETROS','PrimerEnvio','NO')
	with open('.\config.ini', 'w+') as archivoConfig:
		configuracion.write(archivoConfig)
	horaEnvio = round(time.time())
	with open("reg.txt","w") as file:
		file.write(str(horaEnvio))
	env_archivo(archivo)
	print("Mensaje enviado")	
else:
	with open("reg.txt") as file:
		linea = file.readline()
		if len(linea) > 0:
			ultimoEnvio = int(linea)
		else:
			ultimoEnvio = 0
	actualEnvio = round(time.time())
	tiempo = actualEnvio-ultimoEnvio
	print("diferencia con el último envio: ",tiempo)
	if (tiempo > 25):
		with open("reg.txt","w") as file:
			file.write(str(actualEnvio))
		env_archivo(archivo)		
	else:
		print("no ha pasado tiempo suficiente")
	
	