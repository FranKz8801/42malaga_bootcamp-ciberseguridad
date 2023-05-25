kata = "hello world"  # Reemplaza con cualquier cadena de longitud <= 42

if len(kata) == 0:
    formatted_string = " " * 42
else:
    formatted_string = f"{kata:<42}"

print(formatted_string, end="")
