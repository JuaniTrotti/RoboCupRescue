# ejercicio: recorrer una isla
from controller import Robot

# estas variables siempre tienen que estar
timeStep = 32
max_velocity = 6.28

cont = 1

robot = Robot()

wheelL = robot.getDevice("wheel2 motor")
wheelR = robot.getDevice("wheel1 motor")

speed = [max_velocity, max_velocity]

wheelL.setPosition(float("inf"))
wheelR.setPosition(float("inf"))

sensoresDistancia = []
valorDistancia = []  # creamos un array para los valores de los sensores, para tener todos los valores al mismo tiempo. la posicion 0 corresponde al sensor que está
                     # en la posición 0

for i in range(4):
    sensoresDistancia.append(robot.getDevice("distance sensor" + str(i)))
    sensoresDistancia[i].enable(timeStep)
    valorDistancia.append(0)  # inicializamos el arreglo en 0


def delay(ms):
    initTime = robot.getTime()
    while robot.step(timeStep) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

def girar90():
    speed[0] = 0.5 * max_velocity
    speed[1] = -0.5 * max_velocity
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])
    delay(720)


# funciones para aplicar velocidades a las ruedas, para que doble a la izquiera y derecha.
# para usarlas hay que poner un delay después de llamarlas, para que gira una determinada cantidad de tiempo.
def giroIzq():
    speed[0] = -0.5 * max_velocity
    speed[1] = 0.5 * max_velocity
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])

def giroDer():
    speed[0] = 0.5 * max_velocity
    speed[1] = -0.5 * max_velocity
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])


# esta función la usamos para hacer pequeñas correcciones en el camino del robot, porque puede separarse de la pared y entrar en un bucle.
# con esta función evitamos eso.
def correcciones(valorDistancia):
    if valorDistancia[2] > 0.06:
        giroDer()
        delay(5)
        avanzar()
        delay(10)
    elif valorDistancia[2] < 0.05:
        giroIzq()
        delay(5)
        avanzar()
        delay(10)

# función para frenar el robot
def frenar():
    speed[0] = 0
    speed[1] = 0
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])   

# función para que el robot avance
def avanzar():
    speed[0] = max_velocity
    speed[1] = max_velocity
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])

# modificamos la función "hay pared" para que frene y doble a la izquierda
def hayPared():
    frenar()
    giroIzq()
    delay(700)

# con esta función logramos que el robot avance solo cuando de frente no haya paredes y a la derecha haya paredes
# el robot sigue la pared derecha
def irDerecha(valorDistancia):
    if valorDistancia[0] < 0.07:
        hayPared()
    elif valorDistancia[0] > 0.07 and valorDistancia[2] < 0.1:
        avanzar()
        delay(10)
    elif valorDistancia[0] > 0.07 and valorDistancia[2] > 0.1:
        print(valorDistancia)
        avanzar()
        delay(450)
        giroDer()
        print("giro derecha")
        delay(700)
        avanzar()
        delay(450)

while robot.step(timeStep) != -1:
    speed[0] = 0
    speed[1] = 0
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])

    for i in range(4):
        valorDistancia[i] = sensoresDistancia[i].getValue() # llenamos el array con los valores de los sensores
      
    irDerecha(valorDistancia)
    print(valorDistancia)
    correcciones(valorDistancia)