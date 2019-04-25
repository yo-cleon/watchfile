#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import os

print("Es necesario crear el archivo de configuración...")

ruta = input("Introduce la ruta del directorio a monitorizar:")
token = input("¿Cuál es el token del bot de Telegram a utilizar?")
numId = input("Por último, ¿cuál es el Id del grupo/usuario al que enviará los mensajes?")
print("Creando configuracion....")	
cfg = configparser.ConfigParser()
cfg.add_section("GENERAL")
cfg.set("GENERAL","Ruta",ruta)
cfg.set("GENERAL","PrimerEnvio","SI")
cfg.add_section("PARAMETROS")
cfg.set("PARAMETROS","Token",str(token))
cfg.set("PARAMETROS","Id",str(numId))
cfg.set("PARAMETROS","Fichero","")
with open("config.ini","w+") as archivo:
	cfg.write(archivo)	

print("Archivo de configuración creado correctamente.")
