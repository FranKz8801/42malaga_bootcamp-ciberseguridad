import argparse
import logging
import os
import pwd
import signal
import sys
import time
import math

import psutil

logging.basicConfig(filename='/var/log/irondome/irondome.log', level=logging.INFO)

def check_file_extensions(path, extensions):
    """
    Esta función se encarga de comprobar si una extensión de archivo está en la lista de extensiones permitidas.
    """
    _, ext = os.path.splitext(path)
    return ext in extensions

def check_disk_usage():
    """
    Esta función se encarga de comprobar si se está abusando de la lectura de disco.
    """
    usage = psutil.disk_usage('/')
    if usage.percent > 80:
        logging.warning('Abuso en la lectura de disco detectado. Porcentaje de uso: {}'.format(usage.percent))

def check_crypto_activity():
    """
    Esta función se encarga de comprobar si se está haciendo un uso intensivo de actividad criptográfica.
    """
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            if proc.info['username'] == 'root' and 'crypto' in proc.info['name']:
                usage = proc.memory_info().rss / 1024 / 1024
                if usage > 50:
                    logging.warning('Uso intensivo de actividad criptográfica detectado. Proceso: {}, Uso de memoria: {}MB'.format(proc.info['name'], usage))
        except:
           print("")

def check_entropy(path):
    """
    Esta función se encarga de comprobar si hay cambios en la entropía de un archivo.
    """
    with open(path, 'rb') as f:
        data = f.read()
    entropy = compute_entropy(data)
    if entropy < 6.5:
        logging.warning('Cambio en la entropía detectado en el archivo {}. Entropía: {}'.format(path, entropy))

def compute_entropy(data):
    """
    Esta función se encarga de calcular la entropía de los datos.
    """
    if not data:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(x))/len(data)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

def signal_handler(signal, frame):
    """
    Esta función se encarga de manejar la señal de interrupción y salir del programa de forma segura.
    """
    logging.info('Programa Irondome detenido por el usuario.')
    sys.exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Programade monitoreo de seguridad de zona crítica.')
    parser.add_argument('path', type=str, help='Ruta de la zona crítica a monitorear.')
    parser.add_argument('-e', '--extensions', type=str, nargs='+', help='Lista de extensiones de archivo a monitorear.')
    args = parser.parse_args()

    # Comprobar si el usuario es root
    if pwd.getpwuid(os.getuid()).pw_name != 'root':
        sys.stderr.write('El programa solo puede ser ejecutado por el usuario root.\n')
        sys.exit(1)

    # Comprobar si la ruta existe y es un directorio
    if not os.path.isdir(args.path):
        sys.stderr.write('La ruta indicada no existe o no es un directorio.\n')
        sys.exit(1)

    # Configurar la señal de interrupción
    signal.signal(signal.SIGINT, signal_handler)

    # Monitorizar la zona crítica
    while True:
        for root, dirs, files in os.walk(args.path):
            for name in files:
                if args.extensions:
                    if check_file_extensions(name, args.extensions):
                        path = os.path.join(root, name)
                        check_entropy(path)
                else:
                    path = os.path.join(root, name)
                    check_entropy(path)
                check_disk_usage()
                check_crypto_activity()
    time.sleep(60)