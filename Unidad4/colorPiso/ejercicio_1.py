# Ejercicio 1: Detectar los distintos tipos de baldosa e imprimir su nombre 
# en la consola (el nombre, no el color)
from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

# Obtener el sensor de color y habilitarlo
colorSensor = robot.getDevice("colour_sensor")
colorSensor.enable(TIME_STEP)

def esPantano(r, g, b):
    # El color del pantano es (R:244, G:221, B:141), así que analizamos cada 
    # canal por separado y usamos un umbral para comparar.
    return abs(r - 244) < 10 \
        and abs(g - 221) < 10 \
        and abs(b - 141) < 10

def esHole(r, g, b):
    # El color del hole es (R:61, G:61, B:61), así que analizamos cada 
    # canal por separado y usamos un umbral para comparar.
    return abs(r - 61) < 4 \
        and abs(g - 61) < 4 \
        and abs(b - 61) < 4

def esBlue(r, g, b):
    # El color del room1--room2 es (R:91, G:91, B:255), así que analizamos cada 
    # canal por separado y usamos un umbral para comparar.
    return abs(r - 91) < 2 \
        and abs(g - 91) < 2 \
        and abs(b - 255) < 2

def esRed(r, g, b):
    # El color del room2--room3 es (R:255, G:91, B:91), así que analizamos cada 
    # canal por separado y usamos un umbral para comparar.
    return abs(r - 255) < 2 \
        and abs(g - 91) < 2 \
        and abs(b - 91) < 2
        
def esPurple(r, g, b):
    # El color del room1--room3 es (R:193, G:91, B:251), así que analizamos cada 
    # canal por separado y usamos un umbral para comparar.
    return abs(r - 193) < 2 \
        and abs(g - 91) < 2 \
        and abs(b - 251) < 2

def esCheckPoint(r, g, b):
    # El color del checkpoint es (R:255, G:255, B:255), así que analizamos cada 
    # canal por separado y usamos un umbral para comparar.
    return abs(r - 255) < 1 \
        and abs(g - 255) < 1 \
        and abs(b - 255) < 1


while robot.step(TIME_STEP) != -1:
    # Acceder al color detectado por el sensor. El canal A lo ignoramos.
    b, g, r, _ = colorSensor.getImage()

    time = robot.getTime()

    # Si llegamos a un pantano, mostramos un mensaje 
    if esPantano(r, g, b): print(f"{time:.2f}: PANTANO")
    elif esHole(r, g, b): print(f"{time:.2f}: AGUJERO")
    elif esBlue(r, g, b): print(f"{time:.2f}: AZUL")
    elif esRed(r, g, b): print(f"{time:.2f}: ROJO")
    elif esPurple(r, g, b): print(f"{time:.2f}: VIOLETA")
    elif esCheckPoint(r, g, b): print(f"{time:.2f}: CHECKPOINT")
     
