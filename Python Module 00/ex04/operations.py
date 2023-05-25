import sys
def calcular_operaciones(A, B):
    try:
        # Convertir los argumentos a enteros
        A = int(A)
        B = int(B)
        # Realizar las operaciones
        # Imprimir los resultados
        print("Sum: ", A + B)
        print("Difference: ", A - B)
        print("Product: ", A * B)
        if B == 0:
            # Verificar si la división es por cero
            print("Quotient: ERROR DIVISION 0")
            print("Remainder: ERROR módulo 0")
            exit()
        print("Quotient: ", A / B)
        print("Remainder: ", A % B)
    except ValueError:
        print("Error: Se esperaban dos argumentos enteros.")
# Obtener los argumentos de línea de comandos
if len(sys.argv) != 3:
    print("Usage: python operations.py <number1> <number2>")
    print("Example:")
    print("python operations.py 10 3")
else:
    A = sys.argv[1]
    B = sys.argv[2]
    calcular_operaciones(A, B)























