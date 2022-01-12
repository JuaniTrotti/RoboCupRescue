# Ejercicio 1: Mostrar en pantalla sólo la capa 1 de la imagen de profundidad 
# del LIDAR
# NOTA: Usar robot "robot_lidar.json"
from controller import Robot
import math
import numpy as np
import cv2

TIME_STEP = 32

robot = Robot()

lidar = robot.getDevice("lidar")
lidar.enable(TIME_STEP)

def hasObstacle(layer):
    d = math.tau/(8*4)
    a = (math.tau/4)+(math.tau/8)

    s0 = int((a + d*0) / math.tau * 512)
    s1 = int((a + d*3) / math.tau * 512)
    s2 = int((a + d*4) / math.tau * 512)
    s3 = int((a + d*5) / math.tau * 512)
    s4 = int((a + d*8) / math.tau * 512)

    t_near = 0.06
    t_far = 0.2
    return (layer[s1] < t_near or layer[s2] < t_near or layer[s3] < t_near) \
        and (layer[s0] > t_far and layer[s4] > t_far)

while robot.step(TIME_STEP) != -1:
    image = lidar.getRangeImage()
    layer_1 = image[512:1024]


    pixels = []
    for d in layer_1*32:
        color = d * 255
        color = int(max(min(color, 255), 0))
        pixels.append(color)

    # Convertimos el array de pixeles en una imagen
    img = np.frombuffer(bytes(pixels), np.uint8).reshape((32, len(layer_1)))

    # Mostramos la imagen en la pantalla
    cv2.imshow("lidar", img)
    cv2.waitKey(1)