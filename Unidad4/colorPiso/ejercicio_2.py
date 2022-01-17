# Ejercicio: Hacer un robot que recorra el mapa easy1 y NO se caiga en agujeros
# IMPORTANTE: Usar el mapa "easy1.wbt"
from controller import Robot
import math
from random import random

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot() 

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor") 
wheelR.setPosition(float("inf"))

ps7 = robot.getDevice("ps7")
ps7.enable(TIME_STEP)

ps5 = robot.getDevice("ps5")
ps5.enable(TIME_STEP)

ps2 = robot.getDevice("ps2")
ps2.enable(TIME_STEP)

gyro = robot.getDevice("gyro")
gyro.enable(TIME_STEP)

gps = robot.getDevice("gps")
gps.enable(TIME_STEP)

colorSensor = robot.getDevice("colour_sensor")
colorSensor.enable(TIME_STEP)

position = None
initialPosition = None
rotation = 0.25*math.tau
beginTime = robot.getTime()
currentTime = beginTime
deltaTime = 0

x = 0
y = 0

# Declaramos una variable para indicar si estamos por caer al agujero
holeDetected = False

# Esta función recibe un color descompuesto en sus 3 canales RGB y devuelve
# True/False dependiendo de si el color corresponde al agujero o no
def esHole(r, g, b):
    # El color del hole es (R:61, G:61, B:61), así que analizamos cada 
    # canal por separado y usamos un umbral para comparar.
    return abs(r - 61) < 4 \
        and abs(g - 61) < 4 \
        and abs(b - 61) < 4

# Además de actualizar variables de posición/rotación vamos a actualizar
# también la variable "holeDetected" de acuerdo al valor del sensor de color
def updateHoleDetection():
    global holeDetected
    b, g, r, _ = colorSensor.getImage()
    holeDetected = esHole(r, g, b)    

def updatePosition():
    global position, initialPosition
    x, _, y = gps.getValues()
    position = {"x": x, "y": y}
    if initialPosition == None: initialPosition = position

def updateRotation():
    global currentTime, deltaTime, rotation
    lastTime = currentTime
    currentTime = robot.getTime()
    deltaTime = currentTime - lastTime
    
    vel, _, _ = gyro.getValues()
    rotation += (vel * deltaTime)
    rotation %= math.tau # Normalizamos el valor del ángulo

def updateVars():
    updatePosition()
    updateRotation()
    updateHoleDetection()

def step():
    result = robot.step(TIME_STEP)
    updateVars()
    return result

def delay(ms):
    initTime = robot.getTime()
    while step() != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

def angle_diff(a, b):
    clockwise = (a - b) % math.tau
    counterclockwise = (b - a) % math.tau
    return min(clockwise, counterclockwise)

def looking_up(rot):
    return angle_diff(rot, math.tau/4) < math.tau/8

def looking_right(rot):
    return angle_diff(rot, 0) < math.tau/8

def looking_down(rot):
    return angle_diff(rot, -math.tau/4) < math.tau/8

def looking_left(rot):
    return angle_diff(rot, math.tau/2) < math.tau/8

def girar(rad):
    lastRot = rotation
    deltaRot = 0

    while step() != -1:
        deltaRot += angle_diff(rotation, lastRot)
        lastRot = rotation

        diff = angle_diff(deltaRot, abs(rad))

        mul = (5/math.pi) * diff
        mul = min(max(mul, 0.1), 1)

        if rad > 0:
            wheelL.setVelocity(mul*MAX_VEL)
            wheelR.setVelocity(-mul*MAX_VEL)
        else:
            wheelL.setVelocity(-mul*MAX_VEL)
            wheelR.setVelocity(mul*MAX_VEL)

        if diff <= 0.01:
            break

    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

def dist(pt1, pt2):
    return math.sqrt((pt2["x"]-pt1["x"])**2 + (pt2["y"]-pt1["y"])**2)

def avanzar(distance):
    initPos = position

    while step() != -1:
        diff = abs(distance) - dist(position, initPos)

        vel = min(max(diff/0.01, 0.1), 1)
        if distance < 0: vel *= -1
        
        # Corregimos la velocidad ligeramente si nos acercamos a la
        # pared izquierda o derecha
        if ps5.getValue() < 0.035:
            wheelL.setVelocity(vel*MAX_VEL)
            wheelR.setVelocity(.95*vel*MAX_VEL)
        elif ps2.getValue() < 0.06:
            wheelL.setVelocity(.95*vel*MAX_VEL)
            wheelR.setVelocity(vel*MAX_VEL)
        else:
            wheelL.setVelocity(vel*MAX_VEL)
            wheelR.setVelocity(vel*MAX_VEL)

        # Si mientras avanzamos detectamos un agujero, 
        # damos media vuelta y regresamos
        if holeDetected:
            girar(math.pi)
            avanzar(dist(position, initPos))
            return

        if diff < 0.001:
            break
    
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

while step() != -1:
    if ps2.getValue() > 0.1 and random() < 0.5:
        girar(0.25*math.tau) # Girar derecha
        avanzar(0.12)        # Avanzar 1 baldosa
    elif ps5.getValue() > 0.1 and random() < 0.5:
        girar(-0.25*math.tau) # Girar izquierda
        avanzar(0.12)         # Avanzar 1 baldosa
    elif ps7.getValue() < 0.08:
        if random() < 0.5:
            girar(0.25*math.tau) # Girar derecha
        else:
            girar(-0.25*math.tau) # Girar izquierda
    else:
        avanzar(0.12) # Avanzar 1 baldosa