import os
import sys
import time
import datetime
import winreg
import sqlite3
import argparse
from urllib.parse import urlparse
from collections import defaultdict

# Función para convertir estampas de tiempo Unix a formato legible por humanos
def convert_unixtime(unixtime):
    return datetime.datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')

# Función para extraer la lista de programas instalados en el sistema
def get_installed_programs():
    installed_programs = []
    with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
        with winreg.OpenKey(hkey, r'Software\Microsoft\Windows\CurrentVersion\Uninstall') as subkey:
            for i in range(winreg.QueryInfoKey(subkey)[0]):
                try:
                    keyname = winreg.EnumKey(subkey, i)
                    with winreg.OpenKey(subkey, keyname) as subsubkey:
                        installed_programs.append(winreg.QueryValueEx(subsubkey, 'DisplayName')[0])
                except:
                    pass
    return installed_programs

# Función para extraer la lista de programas abiertos en el sistema
def get_running_processes():
    running_processes = []
    for process in os.popen('tasklist /fo csv').readlines()[1:]:
        running_processes.append(process.split(',')[0].strip('"'))
    return running_processes

# Función para extraer la lista de dispositivos USB conectados al sistema
def get_connected_usb_devices():
    usb_devices = []
    for drive in winreg.EnumKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Enum\USBSTOR'):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Enum\USBSTOR\\'+drive) as subkey:
                usb_devices.append(winreg.QueryValueEx(subkey, 'FriendlyName')[0])
        except:
            pass
    return usb_devices

# Función para extraer el historial de navegación de Google Chrome
def get_chrome_history(start_time, end_time):
    history_file = os.path.join(os.getenv('LOCALAPPDATA'), r'Google\Chrome\User Data\Default\History')
    if not os.path.exists(history_file):
        return {}
    conn = sqlite3.connect(history_file)
    cursor = conn.cursor()
    cursor.execute("SELECT url, title, last_visit_time FROM urls WHERE last_visit_time BETWEEN ? AND ?", (start_time, end_time))
    results = cursor.fetchall()
    history = defaultdict(list)
    for url, title, last_visit_time in results:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.strip('www.')
        history[domain].append((title, convert_unixtime(last_visit_time)))
    conn.close()
    return dict(history)

# Función para extraer eventos de log del sistema
def get_system_log_events(start_time, end_time):
    event_log = 'System'
    event_id = 4624
    event_data = '<Data Name="LogonType">2</Data>'
    event_time = 'TimeCreated SystemTime'
    query = f'*[System[EventID={event_id}] and System[EventData[@Name="LogonType"]={event_data}]]'
    command = f'wevtutil qe {event_log} /q:"{query}" /rd:true /f:text /c:1 /q:"*[System[TimeCreated[@SystemTime>=\'{start_time}\'] and TimeCreated[@SystemTime<=\'{end_time}\']]]"'
    events = os.popen(command).readlines()
    events = [event.strip() for event in events if event.strip()]
    return events

# Función principal del programa
def main(start_time=None, end_time=None):
    if start_time is None:
        end_time = int(time.time())
        start_time = end_time - 24*60*60 # Tiempo predeterminado: últimas 24 horas
    if end_time is None:
        end_time = int(time.time())
    print(f'Información para el rango de tiempo: {convert_unixtime(start_time)} - {convert_unixtime(end_time)}\n')
    print('Fechas de cambio de ramas de registro (CurrentVersionRun):')
    # Código para extraer las fechas de cambio de ramas de registro (CurrentVersionRun)
    print('\nArchivos recientes:')
    # Código para extraer la lista de archivos recientes
    print('\nProgramas instalados:')
    installed_programs = get_installed_programs()
    print('\n'.join(installed_programs))
    print('\nProgramas abiertos:')
    running_processes = get_running_processes()
    print('\n'.join(running_processes))
    print('\nHistorial de navegación de Google Chrome:')
    chrome_history = get_chrome_history(start_time, end_time)
    for domain, visits in chrome_history.items():
        print(f'\n{domain}:')
        for title, last_visit_time in visits:
            print(f'    {title} ({last_visit_time})')
    print('\nDispositivos USB conectados:')
    usb_devices = get_connected_usb_devices()
    print('\n'.join(usb_devices))
    print('\nEventos de log del sistema:')
    system_log_events = get_system_log_events(start_time, end_time)
    print('\n'.join(system_log_events))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Programa para extraer información de interés para el forense en un rango de tiempo especificado.')
    parser.add_argument('-s', '--start-time', type=int, help='Estampa de tiempo Unix en segundos para el inicio del rango de tiempo.')
    parser.add_argument('-e', '--end-time', type=int, help='Estampa de tiempo Unix en segundos para el final del rango de tiempo.')
    args = parser.parse_args()
    main(args.start_time, args.end_time)