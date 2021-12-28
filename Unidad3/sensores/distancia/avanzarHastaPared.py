# Ejercicio: Avanzar hasta encontrar una pared
# IMPORTANTE: Usar mapa_pasillo.wbt
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

# Función para frenar el robot
def frenar():
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

# Función para que el robot avance
def avanzar():
    wheelL.setVelocity(MAX_VEL)
    wheelR.setVelocity(MAX_VEL)

# La función "hayPared" recibe un sensor y devuelve 
# True si detecta una pared y False en el caso contrario
def hayPared(sensor):
    return sensor.getValue() < 0.06

while robot.step(TIME_STEP) != -1:
    # Sólo nos interesa chequear el sensor ps0
    if hayPared(sensoresDistancia[0]):
        frenar()
        print("NO puedo pasar, hay una pared!")
    else:
        avanzar()