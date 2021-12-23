#girar el robot en 45, 90, 180 grados y frenar
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

#podemos definir funciones para no tener que escribir todo adentro del while principal, de esta manera dentro del while solo llamaremos a la función

# esta función sirve para que el robot no haga caso a ninguna nueva instrucción durante un determinado tiempo
def delay(ms):
    initTime = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break


# TODOS LOS GIROS DEPENDEN DE LA VELOCIDAD Y EL TIEMPO

# función girar 45 grados
def girar45():
    speed[0] = -0.5 * MAX_VEL
    speed[1] = 0.5 * MAX_VEL
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])
    delay(350)

# función girar 90 grados
def girar90():
    speed[0] = -0.5 * MAX_VEL
    speed[1] = 0.5 * MAX_VEL
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])
    delay(700)

# función girar 180 grados
def girar180():
    speed[0] = -0.5 * MAX_VEL
    speed[1] = 0.5 * MAX_VEL
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])
    delay(1400)

#función que devuelve al robot a su posicion inicial
def reset(): 
    wheelL.setVelocity(speed[1])
    wheelR.setVelocity(speed[0])

# función para que el robot espere una cierta cantidad de tiempo quito
def esperar():
    speed[0] = 0
    speed[1] = 0
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])
    delay(1000)

#esta es la parte principal del programa. Adentro del while se pone todo lo que va a pasar durante la ejecucion del robot
while robot.step(TIME_STEP) != -1:
    speed[0] = 0
    speed[1] = 0
    # forzamos que el robot este quieto solo para esta prueba de giro
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])

    # esto es solo para que no inicie a girar a penas arranca el programa
    delay(1000)

    # como el robot no esta sensando nada, forzamos un cierre del condicional para que solo gire un determinado tiempo una única vez
    # normalmente esto no se hace
    if cont == 1:
        girar45()
        cont += 1 # para salir del condicional

        reset()
        delay(350)

    esperar()

    # como el robot no esta sensando nada, forzamos un cierre del condicional para que solo gire un determinado tiempo una única vez
    # normalmente esto no se hace
    if cont == 2:
        girar90()
        cont += 1

        reset()
        delay(700)

    esperar()

    # como el robot no esta sensando nada, forzamos un cierre del condicional para que solo gire un determinado tiempo una única vez
    # normalmente esto no se hace
    if cont == 3:
        girar180()
        cont += 1
        
        reset()
        delay(1400)

    esperar()