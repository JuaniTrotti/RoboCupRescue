# apnuntar el robot donde no haya paredes
from controller import Robot, DistanceSensor

# estas variables siempre tienen que estar
TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

wheelL = robot.getDevice("wheel1 motor")
wheelR = robot.getDevice("wheel2 motor")

wheelL.setPosition(float("inf"))
wheelR.setPosition(float("inf"))

sensoresDistancia = []
valorDistancia = []  # creamos un array para los valores de los sensores, para tener todos los valores al mismo tiempo. la posicion 0 corresponde al sensor que está
                     # en la posición 0

for i in range(4):
    sensoresDistancia.append(robot.getDevice("ps" + str(i)))
    sensoresDistancia[i].enable(TIME_STEP)
    valorDistancia.append(0)  # inicializamos el arreglo en 0

# función para frenar el robot
def frenar():
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

# función para que el robot avance
def avanzar():
    wheelL.setVelocity(MAX_VEL)
    wheelR.setVelocity(MAX_VEL)

# modificamos la función "hay pared" para que frene cuando vea una en frente.
def hayPared(valorDistancia):
    if valorDistancia[0] < 0.06:
        frenar()
        print("no puedo pasar, hay una pared")
    else:
        avanzar()

while robot.step(TIME_STEP) != -1:

    for i in range(4):
        valorDistancia[i] = sensoresDistancia[i].getValue() # llenamos el array con los valores de los sensores

    # una vez que tenemos los 4 valores de los sensores llamamos a la función para analizar si hay que frenar o seguir
    hayPared(valorDistancia)