# Ejemplo: Detección de obstáculos básica usando sensores de distancia
# NOTA: Usar robot "robot_obstacles.json"
from controller import Robot

TIME_STEP = 32

robot = Robot()

dist = []

for i in range(0, 5):
    sensor = robot.getDevice("i" + str(i))
    sensor.enable(TIME_STEP)
    dist.append(sensor)

# Función que busca obstáculos usando los sensores de distancia
def hasObstacle():
    # Cargamos los valores de los sensores de distancia en una lista
    layer = []
    for i in range(0, 5):
        layer.append(dist[i].getValue())

    # Umbrales para objetos cercanos y lejanos
    t_near = 0.06
    t_far = 0.2

    # Finalmente chequeamos que los sensores centrales (i1, i2, e i3) detecten
    # objeto cercano pero los extremos (i0 e i4) no detecten nada
    return (layer[1] < t_near or layer[2] < t_near or layer[3] < t_near) \
        and (layer[0] > t_far and layer[4] > t_far)

while robot.step(TIME_STEP) != -1:

    # Si detectamos un obstáculo mostramos un mensaje
    if hasObstacle():
        print("OBSTÁCULO!")