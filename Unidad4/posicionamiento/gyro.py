# Ejemplo: Calculando la rotación del robot
from controller import Robot
import math

TIME_STEP = 32
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
    rotation += vel * deltaTime
    rotation %= 2*math.pi
    degrees = rotation * 180/math.pi
    print(f"Velocidad: {vel:.3f} rad/s")
    print(f"Rotación: {rotation:.3f} rad ({degrees:.3f} deg)")
    print("================")

def delay(ms):
    initTime = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        updateVars()
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

while robot.step(TIME_STEP) != -1:
    updateVars()

    wheelL.setVelocity(-0.25*MAX_VEL)
    wheelR.setVelocity(0.25*MAX_VEL)
    delay(500)
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)
    delay(500)

    

