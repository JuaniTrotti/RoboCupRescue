# Ejemplo: Imprimir el color RGB que ve el sensor de color
from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

# wheelL = robot.getDevice("wheel1 motor") 
# wheelL.setPosition(float("inf"))

# wheelR = robot.getDevice("wheel2 motor") 
# wheelR.setPosition(float("inf"))

# Obtener el sensor de color y habilitarlo
colorSensor = robot.getDevice("colour_sensor")
colorSensor.enable(TIME_STEP)

def esPantano(r, g, b):
    # El color del pantano es (R:244, G:221, B:141), así que analizamos cada 
    # canal por separado y usamos un umbral para comparar.
    return abs(r - 244) < 10 \
        and abs(g - 221) < 10 \
        and abs(b - 141) < 10

while robot.step(TIME_STEP) != -1:
    # Acceder al color detectado por el sensor. El canal A lo ignoramos.
    b, g, r, a = colorSensor.getImage()


    # Si llegamos a un pantano, mostramos un mensaje
    if esPantano(r, g, b):
        print(f"{robot.getTime():.2f}: Ojo! Pantano!")
