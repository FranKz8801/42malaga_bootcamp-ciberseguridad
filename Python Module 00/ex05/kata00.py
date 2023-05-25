kata = (19, 42, 21, 25,)
numeros = ", ".join(str(num) for num in kata[:-1])
ult_numero = str(kata[-1])
print(f"The {len(kata)} numbers are: {numeros}, and {ult_numero}")

