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

def delay(ms):
    initTime = robot.getTime()
    while robot.step(timeStep) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

for i in range(4):
    sensoresDistancia.append(robot.getDevice("distance sensor" + str(i)))
    sensoresDistancia[i].enable(timeStep)

def girar90():
    speed[0] = -0.5 * max_velocity
    speed[1] = 0.5 * max_velocity
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])
    delay(700)


# esta función es para saber que sensores estan viendo un objeto y cuales no, en especial tratamos el sensor que está al frente
def hayPared(distancia, i):
    if distancia < 0.1 :
        print("Hay pared en sensor " + str(i))
        return True
    else:
        print("No hay pared en sensor " + str(i))
        return False

# el robot gira
def encarar(i):
    if i == 0:
        girar90()


while robot.step(timeStep) != -1:
    speed[0] = 0
    speed[1] = 0
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])

    for i in range(4):
        distancia = sensoresDistancia[i].getValue()
        if hayPared(distancia, i) == True:
            encarar(i) # si el sensor frontal ve una pared gira hasta que no vea mas una pared