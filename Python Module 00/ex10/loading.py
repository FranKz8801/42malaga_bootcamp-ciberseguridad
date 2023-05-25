import time
def ft_progress(lst):
    total = len(lst) # Obtiene el total de elementos en la lista
    start_time = time.time() # Obtiene el tiempo de inicio del bucle
    elapsed_time = 0 # Inicializa el tiempo transcurrido en 0
    progress = 0 # Inicializa el progreso en 0
    eta = 0 # Inicializa el ETA (Estimated Time of Arrival) en 0
    for i, elem in enumerate(lst, 1): # Utiliza enumerate para obtener el índice y el elemento de la lista
        progress = i / total # Calcula el progreso como la fracción de elementos procesados sobre el total
        elapsed_time = time.time() - start_time # Calcula el tiempo transcurrido restando el tiempo de inicio actual al tiempo de inicio del bucle
        eta = (elapsed_time / progress) * (1 - progress) # Calcula el ETA como el tiempo transcurrido dividido por el progreso, multiplicado por el complemento del progreso
        # Formatea y muestra el progreso en la salida estándar
        print("ETA: {:.2f}s [{:3.0%}][{}{}] {}/{} | elapsed time {:.2f}s".format(eta, progress, '=' * int(progress * 20), '>' if progress < 1 else '', i, total, elapsed_time), end='\r')
        yield elem # Utiliza el operador yield para devolver el elemento actual del bucle y suspender temporalmente la ejecución de la función
    print() # Imprime una nueva línea después de finalizar el bucle
lst = range(0, -100, -1)
ret = 0
for elem in ft_progress(lst):
    ret += elem
    time.sleep(0.005)
print()
print(ret)