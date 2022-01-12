# Ejercicio: Función avanzar() que reciba la distancia a recorrer 
# en línea recta y use el GPS para decidir cuándo detenerse.
from controller import Robot
import math

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot() 

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor") 
wheelR.setPosition(float("inf"))

gps = robot.getDevice("gps") # Paso 1: Obtener el sensor
gps.enable(TIME_STEP) # Paso 2: Habilitar el sensor

position = None
initialPosition = None

def updateVars():
    global position, initialPosition
    x, _, y = gps.getValues()
    position = {"x": x, "y": y}

    if initialPosition == None: initialPosition = position
    
    print(f"{robot.getTime():.2f}) Position: {position}, Distance: {dist(position, initialPosition)}")


def step():
    result = robot.step(TIME_STEP)
    updateVars()
    return result

def delay(ms):
    initTime = robot.getTime()
    while step() != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

def dist(pt1, pt2):
    return math.sqrt((pt2["x"]-pt1["x"])**2 + (pt2["y"]-pt1["y"])**2)

def avanzar(distance):
    initPos = position


    while step() != -1:
        delta = dist(position, initPos)

        vel = 0.25 if distance > 0 else -0.25
        wheelL.setVelocity(vel*MAX_VEL)
        wheelR.setVelocity(vel*MAX_VEL)

        if delta >= distance:
            break
    
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

while step() != -1:
    avanzar(0.12)
    delay(1000)

    