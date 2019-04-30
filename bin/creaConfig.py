#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import os
from utils import mylogger

logger = mylogger.getLogger()

logger.info("Iniciada la creación del archivo de configuración.")
print("Es necesario crear el archivo de configuración...")

ruta = ""
while not os.path.exists(ruta):
    ruta = input("Introduce la ruta del directorio a monitorizar:")
    if not os.path.exists(ruta):
        print("Error: directorio incorrecto. Vuelve a intentarlo.")
        logger.error("El directorio a monitorizar no existe.")

tipoEnvio = input("Formato del envio de avisos (F = Ftp, T = Telegram):")

print("Creando configuracion....")
cfg = configparser.ConfigParser()
cfg.add_section("GENERAL")
cfg.set("GENERAL", "Ruta", ruta)
cfg.set("GENERAL", "TipoEnvio", tipoEnvio)
cfg.set("GENERAL", "PrimerEnvio", "SI")
cfg.set("GENERAL", "Fichero", "")
with open("config.ini", "w+") as archivo:
    cfg.write(archivo)

if tipoEnvio.upper() == 'T':
    token = input("¿Cuál es el token del bot de Telegram a utilizar?")
    numId = input("Por último, ¿cuál es el Id del grupo/usuario al que enviará los mensajes?")
    cfg.add_section("TELEGRAM")
    cfg.set("TELEGRAM", "Token", str(token))
    cfg.set("TELEGRAM", "Id", str(numId))
    cfg.add_section("FTP")
    cfg.set("FTP", "Url", "")
    cfg.set("FTP", "User", "")
    cfg.set("FTP", "Password", "")
    with open("config.ini", "w+") as archivo:
        cfg.write(archivo)
elif tipoEnvio.upper() == 'F':
    url = input("Introduce la dirección ftp: ")
    user = input("Introduce el usuario: ")
    passw = input("Por último, introduce la contraseña: ")
    cfg.add_section("TELEGRAM")
    cfg.set("TELEGRAM", "Token", "")
    cfg.set("TELEGRAM", "Id", "")
    cfg.add_section("FTP")
    cfg.set("FTP", "Url", url)
    cfg.set("FTP", "User", user)
    cfg.set("FTP", "Password", passw)
    with open("config.ini", "w+") as archivo:
        cfg.write(archivo)

print("Archivo de configuración creado correctamente.")
logger.info("Archivo de configuración creado correctamente.")
