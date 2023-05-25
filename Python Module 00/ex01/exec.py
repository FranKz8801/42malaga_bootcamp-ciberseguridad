import sys
def invertir_cadena(cadena):
    """
    Esta función toma una cadena como argumento, la invierte y
    intercambia sus letras mayúsculas y minúsculas.
    """
    cadena_invertida = cadena[::-1]  # Invertir la cadena
    resultado = []
    for char in cadena_invertida:
        if char.islower():
            resultado.append(char.upper())  # Convertir minúscula a mayúscula
        elif char.isupper():
            resultado.append(char.lower())  # Convertir mayúscula a minúscula
        else:
            resultado.append(char)  # Mantener caracteres especiales sin cambios
    return ''.join(resultado)
# Obtener argumentos de la línea de comandos
argumentos = sys.argv[1:]
# Unir argumentos en una sola cadena separada por espacios
cadena = ' '.join(argumentos)
# Verificar si se proporcionó algún argumento
if len(argumentos) == 0:
    print("No se proporcionaron argumentos. Uso: python programa.py <cadena>")
else:
    # Llamar a la función invertir_cadena y mostrar el resultado
    resultado = invertir_cadena(cadena)
    print("Cadena original: ", cadena)
    print("Cadena invertida con letras intercambiadas: ", resultado)