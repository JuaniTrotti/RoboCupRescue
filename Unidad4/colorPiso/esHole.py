from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor") 
wheelR.setPosition(float("inf"))

# Obtener el sensor de color y habilitarlo
colorSensor = robot.getDevice("colour_sensor")
colorSensor.enable(TIME_STEP)

def esHole(r, g, b):
    # El color del hole es (R:61, G:61, B:61), así que analizamos cada 
    # canal por separado y usamos un umbral para comparar.
    return abs(r - 61) < 4 \
        and abs(g - 61) < 4 \
        and abs(b - 61) < 4
    
while robot.step(TIME_STEP) != -1:
    # Acceder al color detectado por el sensor. El canal A lo ignoramos.
    b, g, r, a = colorSensor.getImage()

    print(f"R: {r}, G: {g}, B: {b}")

    # Si llegamos a un pantano, mostramos un mensaje
    if esHole(r, g, b):
        print(f"{robot.getTime():.2f}: Ojo! hole!")
        wheelL.setVelocity(0)
        wheelR.setVelocity(0)