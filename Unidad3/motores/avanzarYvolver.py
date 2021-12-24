# ejericio: avanzar un determinado tiempo y retroceder al inicio
from controller import Robot 

# estas variables siempre tienen que estar
TIME_STEP = 32
MAX_VEL = 6.28

# variable para romper condicional
cont = 1

#creamos la instancia del controlador del robot
robot = Robot()

#creamos los objetos para controlar las ruedas
wheelL = robot.getDevice("wheel1 motor")
wheelR = robot.getDevice("wheel2 motor")

#velocidad de las ruedas, cada posición del array corresponde a una rueda
speed = [MAX_VEL, MAX_VEL]

#definimos la rotación de las ruedas para que esa infinita
wheelL.setPosition(float("inf"))
wheelR.setPosition(float("inf"))

# esta función sirve para que el robot no haga caso a ninguna nueva instrucción durante un determinado tiempo
def delay(ms):
    initTime = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

# funciones nuevas
# avanza en línea recta
def avanzar():
    speed[0] = MAX_VEL
    speed[1] = MAX_VEL
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])
    delay(1600)

# retroce en línea recta
def retroceder():
    speed[0] = MAX_VEL *-1
    speed[1] = MAX_VEL *-1
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])
    delay(1600)

while robot.step(TIME_STEP) != -1: 

    if cont == 2:
        retroceder()
        cont -= 1
  
    if cont == 1:
        avanzar()
        cont += 1