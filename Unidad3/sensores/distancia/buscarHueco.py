# Ejercicio: Detectar el hueco alrededor del robot
# IMPORTANTE: Usar mapa_salida.wbt
from controller import Robot

# Estas variables siempre tienen que estar
TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

wheelL = robot.getDevice("wheel1 motor")
wheelR = robot.getDevice("wheel2 motor")

wheelL.setPosition(float("inf"))
wheelR.setPosition(float("inf"))

# Creamos un array para los valores de los sensores, para poder tener todos 
# los valores al mismo tiempo. la posición 0 corresponde al sensor ps0
sensoresDistancia = []

# En un loop inicializamos todos los sensores y los cargamos en el array
for i in range(8):
    sensoresDistancia.append(robot.getDevice("ps" + str(i)))
    sensoresDistancia[i].enable(TIME_STEP)

# La función "hayPared" recibe un sensor y devuelve 
# True si detecta una pared y False en el caso contrario
def hayPared(sensor):
    return sensor.getValue() < 0.06

def delay(ms):
    initTime = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

def girar90():
    wheelL.setVelocity(-0.25 * MAX_VEL)
    wheelR.setVelocity(0.25 * MAX_VEL)
    delay(1400)

def frenar():
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

while robot.step(TIME_STEP) != -1:
    # Nos interesa chequear los dos sensores frontales (ps0 y ps7)
    if hayPared(sensoresDistancia[0]) or hayPared(sensoresDistancia[7]):
        print("Tengo una pared enfrente, no puedo salir...")
        girar90()
    else:
        print("Camino despejado. Encontré la salida!")
        frenar()