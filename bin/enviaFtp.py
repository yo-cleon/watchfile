#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from ftplib import FTP
from watchfile import configuracion
from watchfile import fc
from utils import mylogger
from os.path import basename

logger = mylogger.getLogger()

# DATOS DEL FICHERO DE CONFIGURACION
parametros = configuracion['FTP']
url = parametros['Url']
user = parametros['User']
passw = parametros['Password']
dir = parametros['DirectorioDestino']
config = configuracion['GENERAL']
archivo = config['fichero']
primerEnvio = config['PrimerEnvio']


# ENVIO DEL ARCHIVO
def env_archivo(f):
    try:
        ftp = FTP(url, user, passw)
        ftp.cwd(dir)
        ftp.storbinary("STOR %s" % basename(archivo), open(archivo, "rb"))
        ftp.quit()
        logger.info("enviaFTP: Archivo subido correctamente.")
    except Exception as e:
        # print(e)
        logger.error(e)


# PROCESO DE SUBIDA DEL ARCHVIO
# print("Inicio del envio del fichero: ", archivo)
logger.info("enviaFtp: inicio del proceso de envío FTP del archivo: %s", archivo)
if primerEnvio.upper() == 'SI':
    configuracion.set('GENERAL', 'PrimerEnvio', 'NO')
    with open(fc, 'w+') as fc:
        configuracion.write(fc)
    horaEnvio = round(time.time())
    with open("reg.txt", "w") as registro:
        registro.write(str(horaEnvio))
    env_archivo(archivo)
else:
    with open("reg.txt") as file:
        linea = file.readline()
        if len(linea) > 0:
            ultimoEnvio = int(linea)
        else:
            ultimoEnvio = 0
    actualEnvio = round(time.time())
    difTiempo = actualEnvio - ultimoEnvio
    # print("diferencia con el último envio: ", difTiempo)
    logger.info("enviaFtp: Diferencia de tiempo con el último envío: %s", difTiempo)
    if difTiempo > 25:
        with open("reg.txt", "w") as f:
            f.write(str(actualEnvio))
        env_archivo(archivo)
    else:
        # print("no ha pasado tiempo suficiente")
        logger.warning("enviaFtp: no ha pasado tiempo suficiente entre envíos. Envío anulado.")
