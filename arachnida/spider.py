import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
# Función para descargar imagen 
def descargar_imagen(url, ruta):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(ruta, 'wb') as file:
            for chunk in response.iter_content(8192):
                file.write(chunk)
        print(f'Imagen descargada: {ruta}')
    except Exception as e:
        print(f'Error al descargar imagen: {url} - {e}')
# Función para obtener todas las imágenes de una página
def obtener_imagenes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        imagenes = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                imagenes.append(src)
        return imagenes
    except Exception as e:
        print(f'Error al obtener imágenes de {url} - {e}')
        return []
# Función para descargar imágenes recursivamente
def descargar_imagenes_recursivamente(url, ruta, nivel_maximo, nivel_actual=0):
    imagenes = obtener_imagenes(url)
    for img in imagenes:
        img_url = urljoin(url, img)
        img_ruta = os.path.join(ruta, os.path.basename(img_url))
        descargar_imagen(img_url, img_ruta)
    if nivel_actual < nivel_maximo:
        enlaces = obtener_enlaces(url)
        for enlace in enlaces:
            descargar_imagenes_recursivamente(enlace, ruta, nivel_maximo, nivel_actual + 1)
# Función para obtener enlaces de una página
def obtener_enlaces(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        enlaces = []
        for a in soup.find_all('a', href=True):
            href = a.get('href')
            if href:
                enlaces.append(urljoin(url, href))
        return enlaces
    except Exception as e:
        print(f'Error al obtener enlaces de {url} - {e}')
        return []
# Función principal
def spider(url, recursivo, nivel, ruta):
    print(f'URL: {url}')
    print(f'Recursivo: {recursivo}')
    print(f'Nivel máximo: {nivel}')
    print(f'Ruta de descarga: {ruta}')
    print('Descargando imágenes...')
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    if recursivo:
        descargar_imagenes_recursivamente(url, ruta, nivel)
    else:
        imagenes = obtener_imagenes(url)
        for img in imagenes:
            img_url = urljoin(url, img)
            img_ruta = os.path.join(ruta, os.path.basename(img_url))
            descargar_imagen(img_url, img_ruta)
    print('Descarga completa')
# Configuración de argumentos de línea de comandos
parser = argparse.ArgumentParser(description='Spider para descargar imágenes de un sitio web')
parser.add_argument('url', metavar='URL', type=str, help='URL del sitio web')
parser.add_argument('-r', '--recursivo', action='store_true', help='Descarga recursiva')
parser.add_argument('-l', '--nivel', type=int, default=5, help='Nivel máximo de descarga recursiva (predeterminado: 5)')
parser.add_argument('-p', '--ruta', type=str, default='./data/', help='Ruta de descarga (predeterminado: ./data/)')
args = parser.parse_args()
# Llamada a la función spider con los argumentos proporcionados
spider(args.url, args.recursivo, args.nivel, args.ruta)



















