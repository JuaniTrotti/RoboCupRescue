# Ejercicio: Activar más de un sensor de distancia e imprimir sus valores por consola
from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

# Creamos un array que contenga todos los sensores
sensoresDistancia = []

# Usamos un for para agregar todos los sensores en las posiciones del array y los activamos. 
# IMPORTANTE: LOS ARRAYS EN PYTHON COMIENZAN EN LA POSICIÓN 0
for i in range(8):
    sensoresDistancia.append(robot.getDevice("ps" + str(i))) # Con la funcion str() convertimos i (que es un entero) en un string y asi podemos concatenar
    sensoresDistancia[i].enable(TIME_STEP) # Activamos el sensor recién creado, que está en la posición i del array

while robot.step(TIME_STEP) != -1:
    # Usamos un for para consultar el valor de cada sensor.
    for i in range(8):
        distancia = sensoresDistancia[i].getValue() # Obtenemos el valor del sensor
        print("Distancia " + str(i) + ": " + str(distancia)) # Imprimimos el sensor con su valor
    print("-------------------") # Imprimimos una línea para separar los ciclos de la simulación