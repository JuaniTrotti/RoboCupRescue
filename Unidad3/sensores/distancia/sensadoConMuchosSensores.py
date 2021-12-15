# en este ejercicio aprenderemos a utilizar más de un sensor de distancia e imprimirlo por consola
from controller import Robot, DistanceSensor

# estas variables siempre tienen que estar
timeStep = 32
max_velocity = 6.28

robot = Robot()

# podemos crear y activar uno por uno pero si los sensores tienen los nombres de la siguiente manera "nombredelsensor NRO" podemos
# crear un array que contenga todos los sensores

sensoresDistancia = []

for i in range(4):
    sensoresDistancia.append(robot.getDevice("distance sensor" + str(i)))
    sensoresDistancia[i].enable(timeStep)

while robot.step(timeStep) != -1:
    
    for i in range(4):
        distancia = sensoresDistancia[i].getValue()
        print("distancia" + str(i) + ":" + str(distancia))