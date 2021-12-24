from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

wheelL = robot.getDevice("wheel1 motor")
wheelL.setPosition(float("inf"))
wheelL.setVelocity(0)

encoderL = robot.getDevice("wheel1 sensor")
encoderL.enable(TIME_STEP)

wheelR = robot.getDevice("wheel2 motor")
wheelR.setPosition(float("inf"))
wheelR.setVelocity(0)

encoderR = robot.getDevice("wheel2 sensor")
encoderR.enable(TIME_STEP)

ps7 = robot.getDevice("ps7")
ps7.enable(TIME_STEP)

ps6 = robot.getDevice("ps6")
ps6.enable(TIME_STEP)

ps5 = robot.getDevice("ps5")
ps5.enable(TIME_STEP)

gyro = robot.getDevice("gyro")
gyro.enable(TIME_STEP)

def delay(ms):
    initTime = robot.getTime()
    while robot.step(TIME_STEP) != -1:
        if (robot.getTime() - initTime) * 1000.0 >= ms:
            break

def turnRight():
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)
    delay(1)
    l0 = encoderL.getValue()
    wheelL.setVelocity(MAX_VEL)
    wheelR.setVelocity(-MAX_VEL)
    while encoderL.getValue() - l0 < 2.15:
        delay(TIME_STEP)
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)
    delay(1)


def turnLeft():
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)
    delay(1)
    r0 = encoderR.getValue()
    wheelL.setVelocity(0.30*MAX_VEL)
    wheelR.setVelocity(1.00*MAX_VEL)
    while encoderR.getValue() - r0 < 2.15:
        delay(TIME_STEP)
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)
    delay(1)

while robot.step(TIME_STEP) != -1:
    print("================")
    print(f"ps7: {ps7.getValue()}")
    print(f"ps6: {ps6.getValue()}")
    print(f"ps5: {ps5.getValue()}")
    print("================")

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
        