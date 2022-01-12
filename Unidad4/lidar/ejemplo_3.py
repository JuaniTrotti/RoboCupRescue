# Ejemplo 1: Visualización de la info del LIDAR
# NOTA: Usar robot "robot_lidar.json"
from controller import Robot
import csv # Librería para escribir y leer archivos CSV

TIME_STEP = 32

# En esta carpeta vamos a grabar los datos
FOLDER = r"X:\RoboCupRescue\temp"

robot = Robot()

lidar = robot.getDevice("lidar")
lidar.enable(TIME_STEP)

# Para calcular la nube de puntos tenemos que habilitarla primero 
lidar.enablePointCloud()

while robot.step(TIME_STEP) != -1:
    # Obtenemos la nube de puntos
    points = lidar.getPointCloud()

    # Cada punto es un objeto con los siguientes atributos x/y/z/layer_id/time,
    # necesitamos transformarlos en una secuencia 
    points = [(p.x, p.y, p.z, p.layer_id, p.time) for p in points]

    # Finalmente, escribimos el archivo
    with open(FOLDER + "/point_cloud.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("x", "y", "z", "layer_id", "time"))
        writer.writerows(points)