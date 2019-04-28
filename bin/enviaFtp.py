#!/usr/bin/python

import time
from ftplib import FTP
from watchfile import configuracion
from watchfile import fileConfig

# DATOS DEL FICHERO DE CONFIGURACION
parametros = configuracion['FTP']
url = parametros['Url']
user = parametros['User']
passw = parametros['Password']
config = configuracion['GENERAL']
archivo = config['fichero']
primerEnvio = config['PrimerEnvio']
print("Inicio del envio del fichero: ", archivo)


# ENVIO DEL ARCHIVO
def env_archivo(f):
    try:
        ftp = FTP(url,user,passw)
        ftp.routeDestination = "/tmp"
        ftp.storbinary("STOR %s" % archivo,open("%s%s" % (url,archivo)))
        ftp.quit()
    except Exception as e:
        print(e)
   
# ANALIZAR SI HAY QUE REALIZAR EL ENVIO
if primerEnvio.upper() == 'SI':
    configuracion.set('PARAMETROS', 'PrimerEnvio', 'NO')
    with open(fileConfig, 'w+') as fc:
        configuracion.write(fc)
    horaEnvio = round(time.time())
    with open("reg.txt", "w") as registro:
        registro.write(str(horaEnvio))
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
    tiempo = actualEnvio - ultimoEnvio
    print("diferencia con el último envio: ", tiempo)
    if (tiempo > 25):
        with open("reg.txt", "w") as f:
            f.write(str(actualEnvio))
        env_archivo(archivo)
    else:
        print("no ha pasado tiempo suficiente")
