# Ejercicio: Función girar() que reciba el ángulo a girar y use
# el giroscopio para calcular cuándo detenerse.
from controller import Robot
import math # Vamos a referirnos a algunas constantes matemáticas

TIME_STEP = 16
MAX_VEL = 6.28

robot = Robot()

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor") 
wheelR.setPosition(float("inf"))

# Inicializamos el giroscopio
gyro = robot.getDevice("gyro")
gyro.enable(TIME_STEP)

# Esta variable va a tener la orientación del robot (en radianes).
# Inicializamos la variable en 90 grados para que el ángulo 0 se 
# corresponda con la derecha y aumente en sentido antihorario.
rotation = 0.25*math.tau

# Necesitamos algunas variables más para llevar la cuenta del tiempo de la 
# simulación, y cuánto tiempo pasó desde el último ciclo
beginTime = robot.getTime()
currentTime = beginTime
deltaTime = 0

# La función updateVars() se encarga de actualizar las variables globales 
# de acuerdo a los valores de los sensores. 
# IMPORTANTE: Hay que llamarla después de cada robot.step()
def updateVars():
    global currentTime, deltaTime, rotation
    # Primero calculamos cuánto tiempo pasó desde el último ciclo
    lastTime = currentTime
    currentTime = robot.getTime()
    deltaTime = currentTime - lastTime
    
    # Luego calculamos la rotación del robot:
    # 1) Obtenemos primero la velocidad angular
    vel, _, _ = gyro.getValues()
    # 2) Calculamos luego la rotación en el último ciclo y la sumamos a la 
    # variable rotation
    rotation += (vel * deltaTime)
    # 3) Normalizamos el valor de rotation para que se mantenga siempre entre
    # 0 y 360 grados (o el equivalente en radianes: 0 y 2*PI)
    rotation %= math.tau # Normalizamos el valor del ángulo
    
    # OPCIONAL: Calcular el valor de rotación en grados y mostrarlo en consola
    degrees = rotation * 180/math.pi
    print(f"Velocidad: {vel:.3f} rad/s")
    print(f"Rotación: {rotation:.3f} rad ({degrees:.3f} deg)")
    print("================")

# Encapsulamos la llamada a robot.step() en una función step() propia que llama 
# automáticamente a updateVars(). De esta forma evitamos llamar a updateVars() 
# manualmente porque step() lo hace por nosotros.
def step():
    result = robot.step(TIME_STEP)
    updateVars()
    return result

# Tenemos que actualizar delay() para que llame a nuestra función step() en
# lugar de robot.step()
def delay(ms):
    initTime = robot.getTime()
    while step() != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

# Esta función calcula la distancia entre 2 ángulos y siempre devuelve un valor 
# positivo entre 0 y 2*PI
def angle_diff(a, b):
    clockwise = (a - b) % math.tau
    counterclockwise = (b - a) % math.tau
    return min(clockwise, counterclockwise)

# La función girar espera los radianes a girar (si el valor es positivo gira a 
# la derecha, sino gira a la izq)
def girar(rad):
    # Primero guardamos en lastRot el valor de rotación actual. Y deltaRot lo
    # vamos a usar para acumular el ángulo que ya giramos (por ahora nada)
    lastRot = rotation
    deltaRot = 0

    # Luego ejecutamos el step() en un loop
    while step() != -1:
        # Dentro del loop lo primero que hacemos es calcular cuánto giramos 
        # hasta ahora acumulando en deltaRot el ángulo girado en la última iteración
        deltaRot += angle_diff(rotation, lastRot)
        lastRot = rotation

        # Luego calculamos cuánto falta por girar
        diff = angle_diff(deltaRot, rad)

        # En función de lo que falta por girar calculamos la velocidad de cada rueda
        mul = (5/math.pi) * diff
        mul = min(max(mul, 0.1), 1)

        # El sentido de giro depende del signo del ángulo a girar (si es positivo 
        # giramos a la derecha, si es negativo a la izquierda=
        if rad > 0:
            wheelL.setVelocity(mul*MAX_VEL)
            wheelR.setVelocity(-mul*MAX_VEL)
        else:
            wheelL.setVelocity(-mul*MAX_VEL)
            wheelR.setVelocity(mul*MAX_VEL)

        # Cuando lo que falta por girar sea menor a 0.01 radianes, salimos del loop
        if diff <= 0.01:
            break

    # Finalmente, frenamos los motores
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

# Es importante llamar a nuestra función step() en lugar de robot.step()
while step() != -1:
    # Giramos 90 grados a la derecha y luego esperamos 1 segundo
    girar(0.25*math.tau)
    delay(1000)

    # Giramos 180 grados a la izquierda y luego esperamos 1 segundo
    girar(-0.5*math.tau)
    delay(1000)
    