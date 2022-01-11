# Ejemplo 1: Visualización de la info del LIDAR
# NOTA: Usar robot "robot_lidar.json"
from controller import Robot

TIME_STEP = 32

robot = Robot()

# Obtenemos el objeto que representa al sensor y lo habilitamos
lidar = robot.getDevice("lidar") # Paso 1
lidar.enable(TIME_STEP) # Paso 1

while robot.step(TIME_STEP) != -1:
    # Obtenemos la información del sensor:
    # - horizontalResolution: 
    # - numberOfLayers: 
    # - rangeImage: 
    horizontalResolution = lidar.getHorizontalResolution()
    numberOfLayers = lidar.getNumberOfLayers()
    rangeImage = lidar.getRangeImage()

    # Finalmente mostramos estos datos en la consola
    print(rangeImage)
    print(f"Resolución horizontal (ancho): {horizontalResolution}")
    print(f"Cantidad de capas (alto): {numberOfLayers}")
    print("=====================")
    
    break