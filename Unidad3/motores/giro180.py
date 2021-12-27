from controller import Robot

# estas variables siempre tienen que estar
TIME_STEP = 32
MAX_VEL = 6.28

#creamos la instancia del controlador del robot
robot = Robot()

#creamos los objetos para controlar las ruedas
wheelL = robot.getDevice("wheel1 motor")
wheelR = robot.getDevice("wheel2 motor")

#definimos la rotación de las ruedas para que esa infinita
wheelL.setPosition(float("inf"))
wheelR.setPosition(float("inf"))

# esta función sirve para que el robot no haga caso a ninguna nueva instrucción durante un determinado tiempo
def delay(ms):
    initTime = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

# TODOS LOS GIROS DEPENDEN DE LA VELOCIDAD Y EL TIEMPO
# función girar 45 grados
def girar45():
    wheelL.setVelocity(-0.5 * MAX_VEL)
    wheelR.setVelocity(0.5 * MAX_VEL)
    delay(350)

def frenar():
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)   

while robot.step(TIME_STEP) != -1:
    girar45()
    frenar()
    delay(1000)
