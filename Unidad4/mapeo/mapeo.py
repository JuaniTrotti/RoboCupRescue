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

ps7 = robot.getDevice("ps7")
ps7.enable(TIME_STEP)

ps5 = robot.getDevice("ps5")
ps5.enable(TIME_STEP)

ps2 = robot.getDevice("ps2")
ps2.enable(TIME_STEP)

ps4 = robot.getDevice("ps4")
ps4.enable(TIME_STEP)

gyro = robot.getDevice("gyro")
gyro.enable(TIME_STEP)

gps = robot.getDevice("gps")
gps.enable(TIME_STEP)

position = None
initialPosition = None
rotation = 0.25*math.tau
beginTime = robot.getTime()
currentTime = beginTime
deltaTime = 0

x = 0
y = 0

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
        
        wheelL.setVelocity(vel*MAX_VEL)
        wheelR.setVelocity(vel*MAX_VEL)

        if diff < 0.001:
            break
    
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

while step() != -1:

    if ps7.getValue() < 0.08:        
        if random() < 0.5:
            girar(0.25*math.tau) # Girar derecha
        else:
            girar(-0.25*math.tau) # Girar izquierda
    else:
        avanzar(0.12) # Avanzar 1 baldosa
            
        if looking_up(rotation): y -= 1
        if looking_right(rotation): x += 1
        if looking_down(rotation): y += 1
        if looking_left(rotation): x -= 1


    l = ps5.getValue() < 0.1
    r = ps2.getValue() < 0.1
    f = ps7.getValue() < 0.1
    b = ps4.getValue() < 0.1
    print(f"F: {f}, R: {r}, B: {b}, L: {l}")

    if looking_up(rotation): print("UP")
    if looking_right(rotation): print("RIGHT")
    if looking_down(rotation): print("DOWN")
    if looking_left(rotation): print("LEFT")

    print([x, y])

    delay(1000)