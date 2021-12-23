# ejericio: Prendiendo motores!
from controller import Robot 

# estas variables siempre tienen que estar
TIME_STEP = 32
MAX_VEL = 6.28


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


while robot.step(TIME_STEP) != -1:
    # acá definimos que velocidad va a tener cada posición del array
    speed[0] = MAX_VEL
    speed[1] = MAX_VEL

    # acá setiamos la velocidad a cada rueda. Es importante que cada rueda tenga una velocidad independiente. 
    # más adelante lo usaremos para hacer giros
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])

    # el robot no va a parar nunca.

