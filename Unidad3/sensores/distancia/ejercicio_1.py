# Ejercicio 1: Leer el valor de uno de los sensores de distancia e imprimirlo por consola
from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

# Para usar el sensor tenemos que primero crearlo y después activarlo
sensorDistancia = robot.getDevice("ps0")                                                       
sensorDistancia.enable(TIME_STEP)

while robot.step(TIME_STEP) != 1:
    distancia = sensorDistancia.getValue() # getValue() sirve para obtener el valor numérico que devuelve el sensor
    print("Distancia: " + str(distancia))  # Imprimimos el resultado por consola