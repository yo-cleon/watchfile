import logging.handlers
import os
import sys

LOGGER_NAME = "my-logger"
LOG_FOLDER = "../log/"
LOG_FILE = "registro.log"
LOG = LOG_FOLDER + LOG_FILE
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(levelname)s: %(asctime)s -  %(message)s"
ROTATE_TIME = "midnight"
LOG_COUNT = 15


#VERIFICAR SI EXISTE EL DIRECTORIO PARA ALMACENAR LOS LOGS Y CREARLO SI NO EXISTE
log_folder = os.path.dirname(LOG_FOLDER)
if not os.path.exists(log_folder):
    try:
        os.makedirs(log_folder)
    except Exception as error:
        print('Error creating the log folder: %s' % (str(error)))


# CREACIÓN Y CONFIGURACIÓN DEL LOG
try:
    logger = logging.getLogger(LOGGER_NAME)
    loggerHandler = logging.handlers.TimedRotatingFileHandler(filename=LOG, when=ROTATE_TIME, interval=1, backupCount=LOG_COUNT)
    formatter = logging.Formatter(LOG_FORMAT)
    loggerHandler.setFormatter(formatter)
    logger.addHandler(loggerHandler)
    logger.setLevel(LOG_LEVEL)
except Exception as error:
    print ("Error with logs: %s" % (str(error)))
    sys.exit()


def getLogger():
    return logger
