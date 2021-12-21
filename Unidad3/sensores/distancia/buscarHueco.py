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
valorDistancia = []

def delay(ms):
    initTime = robot.getTime()
    while robot.step(timeStep) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

for i in range(4):
    sensoresDistancia.append(robot.getDevice("ps" + str(i)))
    sensoresDistancia[i].enable(timeStep)
    valorDistancia.append(0)

def girar90():
    speed[0] = -0.5 * max_velocity
    speed[1] = 0.5 * max_velocity
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])
    delay(700)


# nos fijamos si un sensor esta viendo una pared
def hayPared(valorDistancia):
    if valorDistancia[0] < 0.1:
        print("Tengo una pared en frente")
        encarar()
    else:
        print("No tengo una pared en frente")

# el robot gira
def encarar():
    girar90()


while robot.step(timeStep) != -1:
    speed[0] = 0
    speed[1] = 0
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])

    for i in range(4):
        valorDistancia[i] = sensoresDistancia[i].getValue()

    hayPared(valorDistancia)