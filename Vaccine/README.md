Vaccine.py
Un analizador de vulnerabilidades de SQL injection
Vaccine.py es una herramienta para analizar sitios web en busca de vulnerabilidades de inyección SQL. Realiza las siguientes acciones:

Analiza todas las formas HTML en una URL dada
Intenta inyectar cadenas SQL maliciosas en cada campo de formulario
Comprueba las respuestas en busca de errores indicativos de una vulnerabilidad de SQLi
Informa de cualquier vulnerabilidad detectada e incluye el tipo (booleano, errores, UNION, etc.) y la carga útil que lo activó.
Uso

python vaccine.py URL [-o LOGFILE] [-X REQUEST_METHOD] [-c COOKIE] [-u USER_AGENT]
URL: La URL a analizar
-o LOGFILE: Archivo de registro opcional para guardar los resultados
-X REQUEST_METHOD: Método de solicitud opcional (GET o POST)
-c COOKIE: Cookie de inicio de sesión opcional
-u USER_AGENT: Agente de usuario opcional para falsificar
Instalación
Vaccine.py requiere las siguientes dependencias de Python:

requests
bs4 (BeautifulSoup4)
argparse
pprint
colorama
Puedes instalarlas usando pip:

pip install -r requirements.txt
