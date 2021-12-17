# apnuntar el robot donde no haya paredes
from controller import Robot, DistanceSensor

# estas variables siempre tienen que estar
timeStep = 32
max_velocity = 6.28

robot = Robot()

wheelL = robot.getDevice("wheel2 motor")
wheelR = robot.getDevice("wheel1 motor")

speed = [max_velocity, max_velocity]

wheelL.setPosition(float("inf"))
wheelR.setPosition(float("inf"))

sensoresDistancia = []
valorDistancia = []  # creamos un array para los valores de los sensores, para tener todos los valores al mismo tiempo. la posicion 0 corresponde al sensor que está
                     # en la posición 0

for i in range(4):
    sensoresDistancia.append(robot.getDevice("distance sensor" + str(i)))
    sensoresDistancia[i].enable(timeStep)
    valorDistancia.append(0)  # inicializamos el arreglo en 0

# función para frenar el robot
def frenar():
    speed[0] = 0
    speed[1] = 0
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])   

# función para que el robot avance
def avanzar():
    speed[0] = max_velocity
    speed[1] = max_velocity
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])

# modificamos la función "hay pared" para que frene cuando vea una en frente
def hayPared(valorDistancia):
    if valorDistancia[0] < 0.06:
        frenar()
        print("no puedo pasar, hay una pared")
    else:
        avanzar()

while robot.step(timeStep) != -1:
    speed[0] = 0
    speed[1] = 0
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])


    for i in range(4):
        valorDistancia[i] = sensoresDistancia[i].getValue() # llenamos el array con los valores de los sensores

    # una vez que tenemos los 4 valores de los sensores llamamos a la función para analizar si hay que frenar o seguir
    hayPared(valorDistancia)