# Ejercicio: Función avanzar() que reciba la distancia a recorrer 
# en línea recta y use el GPS para decidir cuándo detenerse.
from controller import Robot
import math

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot() 

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor") 
wheelR.setPosition(float("inf"))

gps = robot.getDevice("gps")
gps.enable(TIME_STEP)

# Vamos a guardar la posición del robot en la variable "position".
# También interesa guardar la posición inicial del robot para poder
# calcular la distancia recorrida.
position = None
initialPosition = None

# La función "updateVars" sólo actualiza el valor de posición
def updateVars():
    global position, initialPosition

    # Representamos la posición del robot como un dictionary con
    # dos valores "x" e "y". De esta forma reducimos el problema
    # a 2 dimensiones (ignoramos el eje vertical)
    x, _, y = gps.getValues()
    position = {"x": x, "y": y}

    # Sólo si la variable no tiene valor, guardamos la posición inicial.
    # Esta variable sólo nos será útil para mostrar la distancia que
    # recorrió el robot. 
    if initialPosition == None: initialPosition = position
    
    # (OPCIONAL): Mostramos en la consola la posición del robot y la
    # distancia recorrida desde su posición inicial. 
    print(f"Posición: {position}")
    print(f"Distancia: {dist(position, initialPosition)}")
    print("===========")

def step():
    result = robot.step(TIME_STEP)
    updateVars()
    return result

def delay(ms):
    initTime = robot.getTime()
    while step() != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

# Función para calcular la distancia entre puntos 2D
def dist(pt1, pt2):
    return math.sqrt((pt2["x"]-pt1["x"])**2 + (pt2["y"]-pt1["y"])**2)

# Función avanzar(), recibe la distancia a recorrer en metros
def avanzar(distance):
    # Lo primero que hacemos es registrar la posición actual
    initPos = position

    while step() != -1:
        # Calculamos cuánto nos falta
        diff = abs(distance) - dist(position, initPos) 

        # La velocidad es función de la distancia
        vel = min(max(diff/0.01, 0.1), 1)
        # Si la distancia es negativa retrocedemos
        if distance < 0: vel *= -1
        
        wheelL.setVelocity(vel*MAX_VEL)
        wheelR.setVelocity(vel*MAX_VEL)

        # Cuando nos falte menos de 0.001 frenamos
        if diff < 0.001:
            break
    
    # Finalmente, frenamos los 2 motores
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

while step() != -1:
    avanzar(0.12) # Avanzar 1 baldosa
    delay(1000)
    
    avanzar(0.12) # Avanzar 1 baldosa
    delay(1000)

    avanzar(-0.12) # Retroceder 1 baldosa
    delay(1000)