# apnuntar el robot donde no haya paredes
from controller import Robot, DistanceSensor

# estas variables siempre tienen que estar
TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

wheelL = robot.getDevice("wheel2 motor")
wheelR = robot.getDevice("wheel1 motor")

speed = [MAX_VEL, MAX_VEL]

wheelL.setPosition(float("inf"))
wheelR.setPosition(float("inf"))

sensoresDistancia = []
valorDistancia = []

def delay(ms):
    initTime = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

for i in range(4):
    sensoresDistancia.append(robot.getDevice("ps" + str(i)))
    sensoresDistancia[i].enable(TIME_STEP)
    valorDistancia.append(0)

def girar90():
    speed[0] = -0.5 * MAX_VEL
    speed[1] = 0.5 * MAX_VEL
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


while robot.step(TIME_STEP) != -1:
    speed[0] = 0
    speed[1] = 0
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])

    for i in range(4):
        valorDistancia[i] = sensoresDistancia[i].getValue()

    hayPared(valorDistancia)