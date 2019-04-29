#!/usr/bin/python
# Script original de http://brunorocha.org/python/watching-a-directory-for-file-changes-with-python.html

# import sys
import os
import time
import configparser
import subprocess
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler 
fileConfig = ".\\config.ini"

if not os.path.exists(fileConfig):
	try:
		subprocess.call('python creaConfig.py')
	except subprocess.CalledProcessError as e:
		print ("Ha habido un error al crear el archivo de configuración: \n",e.output)

#LEER ARCHIVO DE CONFIGURACIÓN PARA LOCALIZAR EL DIRECTORIO A MONITORIZAR
configuracion = configparser.ConfigParser()
configuracion.read("fileConfig")
confGeneral = configuracion['GENERAL']
path = confGeneral['Ruta']
tipoEnvio = confGeneral['TipoEnvio']

#VERIFICAR EXISTENCIA ARCHIVO AUXILIAR DE REGISTRO
if not os.path.isfile("reg.txt"):
	f = open("reg.txt","w")

class MyHandler(PatternMatchingEventHandler):
	patterns = ["*.pdf", "*.xls", "*.xlsx"]
	# def process(self, event):
		# """
		# event.event_type 
			# 'modified' | 'created' | 'moved' | 'deleted'
		# event.is_directory
			# True | False
		# event.src_path
			# path/to/observed/file
		#"""
		# the file will be processed there
		#print (event.src_path, event.event_type)  print now only for debug
	def on_modified(self, event):
		#self.process(event)
		archivo = event.src_path
		print("Se ha modificado el archivo: ",archivo)
		configuracion.set('PARAMETROS','Fichero',archivo)
		with open(fileConfig, 'w+') as archivoConfig:
			configuracion.write(archivoConfig)
		if tipoEnvio.upper == 'T':
			result=subprocess.call('python enviaTelegram.py')
			if result == 0:
				print("Script ejecutado")
			else:
				print("problemas con el script")
		elif tipoEnvio.upper == 'F':
			result = subprocess.call('python enviaFtp.py')
			if result == 0:
				print("Script ejecutado")
			else:
				print("problemas con el script")
		print ("archivo modificado: ",event)
	def on_created(self, event):
		#self.process(event)
		archivo = event.src_path
		print("Se ha creado el archivo: ",archivo)
		configuracion.set('PARAMETROS','Fichero',archivo)
		with open('.\config.ini', 'w+') as archivoConfig:
			configuracion.write(archivoConfig)
		result=subprocess.call('python enviaTelegram.py')
		if result == 0:
			print("Script ejecutado")
		else:
			print("problemas con el script")
		
if __name__ == '__main__':
	#args = sys.argv[1:]
	observer = Observer()
	#observer.schedule(MyHandler(), path=args[0] if args else '.')
	observer.schedule(MyHandler(), path)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
		
	print("Script finalizado.")

	observer.join()