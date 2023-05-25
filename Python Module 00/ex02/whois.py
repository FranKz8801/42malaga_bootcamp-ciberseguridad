import sys
def check_number(number):
    """
    Esta función toma un número como argumento y realiza pruebas
    condicionales basadas en su paridad.
    """
    if number == 0:
        return "Soy Cero."
    elif number % 2 == 0:
        return "Soy Par."
    else:
        return "Soy Impar."
# Verificar si se proporcionaron más de dos argumentos
if len(sys.argv) > 2:
    print("AssertionError: Se proporcionaron más de un argumento")
    exit()
elif len(sys.argv) == 2:
    try:
        number = int(sys.argv[1])
        print(check_number(number))
    except:
        print("AssertionError: El argumento no es un entero")
        exit()
else:
    print("No se proporcionaron argumentos. Uso: python programa.py <número>")



