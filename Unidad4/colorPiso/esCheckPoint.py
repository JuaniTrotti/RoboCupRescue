from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

# Obtener el sensor de color y habilitarlo
colorSensor = robot.getDevice("colour_sensor")
colorSensor.enable(TIME_STEP)

def esCheckPoint(r, g, b):
    # El color del checkpoint es (R:255, G:255, B:255), así que analizamos cada 
    # canal por separado y usamos un umbral para comparar.
    return abs(r - 255) < 1 \
        and abs(g - 255) < 1 \
        and abs(b - 255) < 1

while robot.step(TIME_STEP) != -1:
    # Acceder al color detectado por el sensor. El canal A lo ignoramos.
    b, g, r, a = colorSensor.getImage()

    print(f"R: {r}, G: {g}, B: {b}")

    # Si llegamos a un pantano, mostramos un mensaje
    if esCheckPoint(r, g, b):
        print(f"{robot.getTime():.2f}: Ojo! CheckPoint!")