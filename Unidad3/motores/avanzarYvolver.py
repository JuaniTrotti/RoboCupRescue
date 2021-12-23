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
wheelL = robot.getDevice("wheel2 motor")
wheelR = robot.getDevice("wheel1 motor")

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

def girar90():
    speed[0] = -0.5 * MAX_VEL
    speed[1] = 0.5 * MAX_VEL
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])
    delay(700)

def girar180():
    speed[0] = -0.5 * MAX_VEL
    speed[1] = 0.5 * MAX_VEL
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])
    delay(1400)


# funciones nuevas
# avanza en línea recta
def avanzar():
    speed[0] = MAX_VEL
    speed[1] = MAX_VEL
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[0])
    delay(2600)

# retroce en línea recta
def retroceder():
    speed[0] = MAX_VEL *-1
    speed[1] = MAX_VEL *-1
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[0])
    delay(2600)

while robot.step(TIME_STEP) != -1:
    speed[0] = 0
    speed[1] = 0
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])
    
    # solución uno. retrocede de espaldas
    if cont == 1:
        girar90() #esto es necesario en este caso, solo para que el robot apunte a la pista
        avanzar()
        retroceder()
        cont += 1
    # solución dos. cuando pasa el tiempo determinado se da vuelta y vuelve mirando 
    if cont == 2:
        avanzar() 
        girar180()
        avanzar()
        cont += 1