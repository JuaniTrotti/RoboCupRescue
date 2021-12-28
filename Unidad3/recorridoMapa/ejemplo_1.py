from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

wheelL = robot.getDevice("wheel1 motor")
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor")
wheelR.setPosition(float("inf"))

ps7 = robot.getDevice("ps7")
ps7.enable(TIME_STEP)

ps5 = robot.getDevice("ps5")
ps5.enable(TIME_STEP)

def delay(ms):
    initTime = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        if (robot.getTime() - initTime) * 1000.0 >= ms:
            break

def turnRight():
    wheelL.setVelocity(MAX_VEL)
    wheelR.setVelocity(-MAX_VEL)
    delay(350)
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)
    delay(1)

def turnLeft():
    wheelL.setVelocity(0.30*MAX_VEL)
    wheelR.setVelocity(1.00*MAX_VEL)
    delay(350)
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)
    delay(1)

while robot.step(TIME_STEP) != -1:
    dist_left = ps5.getValue()
    dist_front = ps7.getValue()

    if dist_left < 0.035:
        wheelL.setVelocity(1.0 * MAX_VEL)
        wheelR.setVelocity(.95 * MAX_VEL)
    elif dist_left > 0.045:
        wheelL.setVelocity(.95 * MAX_VEL)
        wheelR.setVelocity(1.0 * MAX_VEL)
    else:
        wheelL.setVelocity(1.0 * MAX_VEL)
        wheelR.setVelocity(1.0 * MAX_VEL)

    if dist_left > 0.1:
        turnLeft()
    elif dist_front < 0.05:
        turnRight()
        