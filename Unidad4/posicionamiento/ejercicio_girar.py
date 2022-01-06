# Ejercicio: Función girar() que reciba el ángulo a girar y use
# el giroscopio para calcular cuándo detenerse
from controller import Robot
import math

TIME_STEP = 16
MAX_VEL = 6.28 # Velocidad máxima (1 vuelta por segundo)

robot = Robot()

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor") 
wheelR.setPosition(float("inf"))

gyro = robot.getDevice("gyro")
gyro.enable(TIME_STEP)

rotation = 0

beginTime = robot.getTime()
currentTime = beginTime
deltaTime = 0

def updateVars():
    global currentTime, deltaTime, rotation
    lastTime = currentTime
    currentTime = robot.getTime()
    deltaTime = currentTime - lastTime
    
    vel, _, _ = gyro.getValues()
    rotation += (vel * deltaTime)
    rotation %= math.tau
    degrees = rotation * 180/math.pi
    print(f"Velocidad: {vel:.3f} rad/s")
    print(f"Rotación: {rotation:.3f} rad ({degrees:.3f} deg)")
    print("================")

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

def girar(rad):
    lastRot = rotation
    deltaRot = 0
    if rad > 0:
        wheelL.setVelocity(0.25*MAX_VEL)
        wheelR.setVelocity(-0.25*MAX_VEL)
    elif rad < 0:
        wheelL.setVelocity(-0.25*MAX_VEL)
        wheelR.setVelocity(0.25*MAX_VEL)
    while step() != -1:
        deltaRot += angle_diff(rotation, lastRot)
        lastRot = rotation
        if deltaRot >= abs(rad):
            break
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

while step() != -1:
    girar(0.25*math.tau)
    delay(1000)

    girar(-0.5*math.tau)
    delay(1000)
    