# Ejercicio: Imprimir un mensaje en la consola cada vez que el robot pase
# al lado de una víctima (no hace falta identificar el tipo de víctima)
# NOTA 1: Usar mundo "mapa_noholes_2.wbt"
# NOTA 2: Usar robot "robot_cameras.json"
from controller import Robot
from enum import Enum
from random import random

TIME_STEP = 32
MAX_VEL = 6.28

class State(Enum):
    FOLLOW_LEFT = 1
    FOLLOW_RIGHT = 2

state = State.FOLLOW_RIGHT
robot = Robot()

wheelL = robot.getDevice("wheel1 motor")
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor")
wheelR.setPosition(float("inf"))

# Sensor frontal
ps7 = robot.getDevice("ps7")
ps7.enable(TIME_STEP)

# Sensor izquierda
ps5 = robot.getDevice("ps5")
ps5.enable(TIME_STEP)

# Sensor derecha
ps2 = robot.getDevice("ps2")
ps2.enable(TIME_STEP)

# Cámara izquierda
cameraL = robot.getDevice("camera_left")
cameraL.enable(TIME_STEP)

# Cámara derecha
cameraR = robot.getDevice("camera_right")
cameraR.enable(TIME_STEP)

def delay(ms):
    initTime = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        if (robot.getTime() - initTime) * 1000.0 >= ms:
            break

def getColorAt(camera, x, y):
    image = camera.getImage()
    w = camera.getWidth()
    r = camera.imageGetRed(image, w, x, y)
    g = camera.imageGetGreen(image, w, x, y)
    b = camera.imageGetBlue(image, w, x, y)
    return r, g, b

def frenar():
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

def girarDerecha():
    wheelL.setVelocity(MAX_VEL)
    wheelR.setVelocity(-MAX_VEL)
    delay(350)
    frenar()
    delay(1)

def girarIzquierda():
    wheelL.setVelocity(-MAX_VEL)
    wheelR.setVelocity(MAX_VEL)
    delay(350)
    frenar()
    delay(1)

def avanzar():    
    wheelL.setVelocity(0.5 * MAX_VEL)
    wheelR.setVelocity(0.5 * MAX_VEL)

def avanzarIzquierda():    
    wheelL.setVelocity(.47 * MAX_VEL)
    wheelR.setVelocity(0.5 * MAX_VEL)

def avanzarDerecha():
    wheelL.setVelocity(0.5 * MAX_VEL)
    wheelR.setVelocity(.47 * MAX_VEL)

def detectarVictima(camera):
    r, g, b = getColorAt(camera, 64, 64)
    if r > 200 and g > 200 and b > 200:
        print(f"{robot.getTime():.2f}: Acá hay una víctima!")

while robot.step(TIME_STEP) != -1:
    # Primero chequeamos las cámaras
    detectarVictima(cameraL)
    detectarVictima(cameraR)

    # Leo los sensores de distancia y guardo los valores en variables
    dist_left = ps5.getValue()
    dist_right = ps2.getValue()
    dist_front = ps7.getValue()
    # print(f"{state}, L: {dist_left}, R: {dist_right}, F: {dist_front}")

    # Si estoy siguiendo la pared izquierda, trato de avanzar corrigiendo la
    # velocidad de forma que me mantenga a la misma distancia.
    # Si estoy siguiendo la pared derecha, hago lo mismo pero con la derecha.
    if state == State.FOLLOW_LEFT:
        if dist_left < 0.035:
            avanzarDerecha()
        elif dist_left > 0.045:
            avanzarIzquierda()
        else:
            avanzar()
    elif state == State.FOLLOW_RIGHT:
        if dist_right < 0.035:
            avanzarIzquierda()
        elif dist_right > 0.045:
            avanzarDerecha()
        else:
            avanzar()

    # Si el sensor frontal detecta una pared, tiramos una moneda para decidir si 
    # giro 90 grados hacia la izquierda o hacia la derecha.
    # Cuando giro a la derecha paso a seguir la pared izquierda, y viceversa.
    if dist_front < 0.05:
        if random() < 0.5:
            state = State.FOLLOW_LEFT
            girarDerecha()
        else:
            state = State.FOLLOW_RIGHT
            girarIzquierda()