#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import os

print("Es necesario crear el archivo de configuración...")

ruta = input("Introduce la ruta del directorio a monitorizar:")
tipoEnvio = input("Formato del envio de avisos (F = Ftp, T = Telegram):")

print("Creando configuracion....")	
cfg = configparser.ConfigParser()
cfg.add_section("GENERAL")
cfg.set("GENERAL","Ruta",ruta)
cfg.set("GENERAL","PrimerEnvio","SI")
cfg.set("GENERAL","TipoEnvio",tipoEnvio)
cfg.set("GENERAL","Fichero","")
with open("config.ini","w+") as archivo:
	cfg.write(archivo)	
if upper(tipoEnvio) == 'T':
	token = input("¿Cuál es el token del bot de Telegram a utilizar?")
	numId = input("Por último, ¿cuál es el Id del grupo/usuario al que enviará los mensajes?")
	cfg.add_section("TELEGRAM")
	cfg.set("TELEGRAM","Token",str(token))
	cfg.set("TELEGRAM","Id",str(numId))
	cfg.add_section("FTP")
	cfg.set("FTP","Url","")
	cfg.set("FTP","User","")
	cfg.set("FTP","Password","")
	with open("config.ini","w+") as archivo:
		cfg.write(archivo)	
elif upper(tipoEnvio) == 'F':
	url = input("Introduce la dirección ftp: ")
	user = input("Introduce el usuario: ")
	passw = input("Por último, introduce la contraseña: ")
	cfg.add_section("TELEGRAM")
	cfg.set("TELEGRAM","Token","")
	cfg.set("TELEGRAM","Id","")
	cfg.add_section("FTP")
	cfg.set("FTP","Url",url)
	cfg.set("FTP","User",user)
	cfg.set("FTP","Password",passw)
	with open("config.ini","w+") as archivo:
		cfg.write(archivo)



print("Archivo de configuración creado correctamente.")
