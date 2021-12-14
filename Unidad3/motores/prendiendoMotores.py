#girar el robot en 45, 90, 180 grados y frenar
from controller import Robot

timeStep = 32
max_velocity = 6.28

#creamos la instancia del controlador del robot
robot = Robot()

#creamos los objetos para controlar las ruedas
wheelL = robot.getDevice("wheel2 motor")
wheelR = robot.getDevice("wheel1 motor")

#velocidad de las ruedas, cada posición del array corresponde a una rueda
speed = [max_velocity, max_velocity]

#definimos la rotación de las ruedas para que esa infinita
# wheelL.setPosition(float("inf"))
# wheelR.setPosition(float("inf"))

#podemos definir funciones para no tener que escribir todo adentro del while principal, de esta manera dentro del while solo llamaremos a la función
def girar45():
    speed[0] = -1 * max_velocity
    speed[1] = max_velocity

# def delay(ms):
#     initTime = robot.getTime()      # Store starting time (in seconds)
#     while robot.step(timeStep) != -1:
#         if (robot.getTime() - initTime) * 1000.0 > ms: # If time elapsed (converted into ms) is greater than value passed in
#             break

#esta es la parte principal del programa. Adentro del while se pone todo lo que va a pasar durante la ejecucion del robot
while robot.step(timeStep) != -1:
    speed[0] = 0
    speed[1] = 0

    if speed[0] == 0:
        girar45()

    
    wheelL.setVelocity(speed[0])
    wheelR.setVelocity(speed[1])