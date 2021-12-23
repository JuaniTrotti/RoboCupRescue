# en este ejercicio aprenderemos a utilizar un sensor de distancia e imprimirlo por consola
from controller import Robot, DistanceSensor

# estas variables siempre tienen que estar
TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

# para usar el sensor tenemos que primero crearlo y después activarlo

sensorDistancia = robot.getDevice("ps0")  # creamos una variable que contiene al sensor, "distance sensor1" es el nombre del sensor que aparece
                                                       # cuando configuramos el robot (el nombre que le pongan al sensor tiene que coincidir con el que quieran activar)
                                                       # en este caso es el sensor que esta en el frente
                                                       
sensorDistancia.enable(TIME_STEP)                       # en esta linea activamos el sensor y le pasamos timeStep como velocidad de refresco del sensor.

while robot.step(TIME_STEP) != 1:

    distanceAdelante = sensorDistancia.getValue() # getValue() sirve para obtener el valor numerico que devuelve el sensor
    print("Distancia: " + str(distanceAdelante))  # Imprimimos el resultado por consola