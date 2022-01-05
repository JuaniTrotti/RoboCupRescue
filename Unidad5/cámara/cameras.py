from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28


robot = Robot()

wheelL = robot.getDevice("wheel1 motor")
wheelL.setPosition(float("inf"))
wheelL.setVelocity(0)

wheelR = robot.getDevice("wheel2 motor")
wheelR.setPosition(float("inf"))
wheelR.setVelocity(0)

cameraL = robot.getDevice("camera_left")
cameraL.enable(TIME_STEP)

cameraC = robot.getDevice("camera_centre")
cameraC.enable(TIME_STEP)

cameraR = robot.getDevice("camera_right")
cameraR.enable(TIME_STEP)

colorSensor = robot.getDevice("colour_sensor")
colorSensor.enable(TIME_STEP)

def getColorAt(camera, x, y):
    image = camera.getImage()
    w = camera.getWidth()
    r = camera.imageGetRed(image, w, x, y)
    g = camera.imageGetGreen(image, w, x, y)
    b = camera.imageGetBlue(image, w, x, y)
    return r, g, b

while robot.step(TIME_STEP) != -1:
    r, g, b = getColorAt(cameraC, 64, 64)
    if r > 200 and g > 200 and b > 200:
        print(f"{robot.getTime()}: Acá hay una víctima!")