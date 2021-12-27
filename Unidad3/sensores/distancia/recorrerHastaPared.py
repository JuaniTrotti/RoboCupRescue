# ejercicio: recorrer por derecha hasta zona de parking
# el robot tiene que estacionar en la zona donde haya tres paredes
# para resolver este ejercicio hay que hacer uso de la configuración avanzada de la estructura del robot
from controller import Robot, DistanceSensor

# estas variables siempre tienen que estar
TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

wheelL = robot.getDevice("wheel1 motor")
wheelR = robot.getDevice("wheel2 motor")

speed = [MAX_VEL, MAX_VEL]

wheelL.setPosition(float("inf"))
wheelR.setPosition(float("inf"))

sensoresDistancia = []
valorDistancia = []  # creamos un array para los valores de los sensores, para tener todos los valores al mismo tiempo. la posicion 0 corresponde al sensor que está
                     # en la posición 0

for i in range(4):
    sensoresDistancia.append(robot.getDevice("distance sensor" + str(i)))
    sensoresDistancia[i].enable(TIME_STEP)
    valorDistancia.append(0)  # inicializamos el arreglo en 0


def delay(ms):
    initTime = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

def girar90():
    wheelL.setVelocity(-0.5 * MAX_VEL)
    wheelR.setVelocity(0.5 * MAX_VEL)
    delay(720)


# funciones para aplicar velocidades a las ruedas, para que doble a la izquiera y derecha.
# para usarlas hay que poner un delay después de llamarlas, para que gira una determinada cantidad de tiempo.
def giroIzq():
    wheelL.setVelocity(0.5 * MAX_VEL)
    wheelR.setVelocity(-0.5 * MAX_VEL)

def giroDer():
    wheelL.setVelocity(-0.5 * MAX_VEL)
    wheelR.setVelocity(0.5 * MAX_VEL)


# esta función la usamos para hacer pequeñas correcciones en el camino del robot, porque puede separarse de la pared y entrar en un bucle.
# con esta función evitamos eso.
def correcciones(valorDistancia):
    if valorDistancia[2] > 0.07:
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
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)   

# función para que el robot avance
def avanzar():
    wheelL.setVelocity(MAX_VEL)
    wheelR.setVelocity(MAX_VEL)

# modificamos la función "hay pared" para que frene y doble a la izquierda
def hayPared(valorDistancia):
    if valorDistancia[0] < 0.06:
        frenar()
        giroIzq()
        delay(720)

# con esta función logramos que el robot avance solo cuando de frente no haya paredes y a la derecha haya paredes
# el robot sigue la pared derecha
def irDerecha(valorDistancia):
    if valorDistancia[2] > 0.1: # gira hasta encontrar una pared a la derecha
        print("giro")
        girar90()
    elif valorDistancia[2] < 0.07 and valorDistancia[0] > 0.06: # si tiene una pared a la derecha y no tiene nada adelante, avanza
        print("avanzo")
        avanzar()
        delay(10)
    elif valorDistancia[0] < 0.06:
        if valorDistancia[3] < 0.2: # llego a la zona donde tiene que frenar
            frenar()
            print("estacione")
        else: # si no hay una pared a la izquierda todavía no llego a la zona de frenado
            hayPared(valorDistancia)

while robot.step(TIME_STEP) != -1:

    for i in range(4):
        valorDistancia[i] = sensoresDistancia[i].getValue() # llenamos el array con los valores de los sensores
        
    irDerecha(valorDistancia)
    correcciones(valorDistancia)