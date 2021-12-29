from controller import Robot

TIME_STEP = 32
MAX_VEL = 6.28

robot = Robot()

wheelL = robot.getDevice("left motor")
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("right motor")
wheelR.setPosition(float("inf"))

t0 = robot.getTime()
wheelL.setVelocity(0.5*MAX_VEL)
wheelR.setVelocity(-0.5*MAX_VEL)

while robot.step(TIME_STEP) != -1:
    if robot.getTime() - t0 > 0.700:
        break

wheelL.setVelocity(0)
wheelR.setVelocity(0)