# en este ejercicio aprenderemos a utilizar más de un sensor de distancia e imprimirlo por consola
from controller import Robot, DistanceSensor

# estas variables siempre tienen que estar
TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

# podemos crear y activar uno por uno pero si los sensores tienen los nombres de la siguiente manera "nombredelsensor NRO"
# creamos un array que contenga todos los sensores
sensoresDistancia = []

# usamos un for para agregar todos los sensores en las posiciones del array y los activamos. 
# IMPORTANTE, LOS ARRAYS EN PYTHON COMIENZAN EN LA POSICIÓN 0, es decir que los sensores que tengas tienen que ser así: sensor0, sensor1 .... sensor N
for i in range(4):
    sensoresDistancia.append(robot.getDevice("ps" + str(i))) # con la funcion str() convertimos i (que es un entero) en un string y asi podemos concatenar. 
    sensoresDistancia[i].enable(TIME_STEP) # aca el elemento que está en la posición i del array lo activamos.

while robot.step(TIME_STEP) != -1:

    # usamos un for para consultar el valor de cada sensor.
    for i in range(4):
        distancia = sensoresDistancia[i].getValue() # obtenemos el valor del sensor
        print("distancia" + str(i) + ":" + str(distancia)) # imprimimos el sensor con su valor