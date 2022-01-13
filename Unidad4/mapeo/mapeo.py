from controller import Robot
from enum import Enum
import math
from random import random

TIME_STEP = 32
MAX_VEL = 6.28

FOLDER = r"X:\RoboCupRescue\temp"

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

robot = Robot() 

wheelL = robot.getDevice("wheel1 motor") 
wheelL.setPosition(float("inf"))

wheelR = robot.getDevice("wheel2 motor") 
wheelR.setPosition(float("inf"))

ps7 = robot.getDevice("ps7")
ps7.enable(TIME_STEP)

ps7 = robot.getDevice("ps7")
ps7.enable(TIME_STEP)

ps5 = robot.getDevice("ps5")
ps5.enable(TIME_STEP)

ps2 = robot.getDevice("ps2")
ps2.enable(TIME_STEP)

ps4 = robot.getDevice("ps4")
ps4.enable(TIME_STEP)

gyro = robot.getDevice("gyro")
gyro.enable(TIME_STEP)

gps = robot.getDevice("gps")
gps.enable(TIME_STEP)

position = None
direction = None
rotation = 0.25*math.tau
beginTime = robot.getTime()
currentTime = beginTime
deltaTime = 0

x = 0
y = 0

grid = {}

def tile(x, y):
    if (x, y) in grid: return grid[(x, y)]
    t = {"x": x, "y": y,
         "up": None,
         "down": None,
         "left": None,
         "right": None}
    grid[(x, y)] = t
    return t

def connectTiles(prev, cur, direction):
    if direction == Direction.UP:
        prev["up"] = cur
        cur["down"] = prev
    elif direction == Direction.RIGHT: 
        prev["right"] = cur
        cur["left"] = prev
    elif direction == Direction.DOWN:
        prev["down"] = cur
        cur["up"] = prev
    elif direction == Direction.LEFT:
        prev["left"] = cur
        cur["right"] = prev

def updatePosition():
    global position, initialPosition
    x, _, y = gps.getValues()
    position = {"x": x, "y": y}

def updateRotation():
    global currentTime, deltaTime, rotation, direction
    lastTime = currentTime
    currentTime = robot.getTime()
    deltaTime = currentTime - lastTime
    
    vel, _, _ = gyro.getValues()
    rotation += (vel * deltaTime)
    rotation %= math.tau
    
    if looking_up(rotation): direction = Direction.UP
    elif looking_right(rotation): direction = Direction.RIGHT
    elif looking_down(rotation): direction = Direction.DOWN
    elif looking_left(rotation): direction = Direction.LEFT
    
def updateVars():
    updatePosition()
    updateRotation()

def step():
    result = robot.step(TIME_STEP)
    updateVars()
    return result

def delay(ms):
    initTime = robot.getTime()
    while step() != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:
            break

def angle_diff(a, b):
    clockwise = (a - b) % math.tau
    counterclockwise = (b - a) % math.tau
    return min(clockwise, counterclockwise)

def looking_up(rot):
    return angle_diff(rot, math.tau/4) < math.tau/8

def looking_right(rot):
    return angle_diff(rot, 0) < math.tau/8

def looking_down(rot):
    return angle_diff(rot, -math.tau/4) < math.tau/8

def looking_left(rot):
    return angle_diff(rot, math.tau/2) < math.tau/8

def girar(rad):
    lastRot = rotation
    deltaRot = 0

    while step() != -1:
        deltaRot += angle_diff(rotation, lastRot)
        lastRot = rotation

        diff = angle_diff(deltaRot, abs(rad))

        mul = (5/math.pi) * diff
        mul = min(max(mul, 0.1), 1)

        if rad > 0:
            wheelL.setVelocity(mul*MAX_VEL)
            wheelR.setVelocity(-mul*MAX_VEL)
        else:
            wheelL.setVelocity(-mul*MAX_VEL)
            wheelR.setVelocity(mul*MAX_VEL)

        if diff <= 0.01:
            break

    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

def dist(pt1, pt2):
    return math.sqrt((pt2["x"]-pt1["x"])**2 + (pt2["y"]-pt1["y"])**2)

def avanzar(distance):
    initPos = position

    while step() != -1:
        diff = abs(distance) - dist(position, initPos) 

        vel = min(max(diff/0.01, 0.1), 1)
        if distance < 0: vel *= -1
        
        wheelL.setVelocity(vel*MAX_VEL)
        wheelR.setVelocity(vel*MAX_VEL)

        if diff < 0.001:
            break
    
    wheelL.setVelocity(0)
    wheelR.setVelocity(0)

def writeGrid():
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    for x, y in grid:
        if x < min_x: min_x = x
        if y < min_y: min_y = y
        if x > max_x: max_x = x
        if y > max_y: max_y = y

    rows = []
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            t = grid.get((x, y))
            chars = [["+", "-", "+"],["|", "?", "|"],["+", "-", "+"]]
            if t != None:
                chars[1][1] = "@" if x == 0 and y == 0 else " "
                if t["up"] != None: chars[0][1] = " "
                if t["right"] != None: chars[1][2] = " "
                if t["down"] != None: chars[2][1] = " "
                if t["left"] != None: chars[1][0] = " "
            row.append(chars)
        rows.append(row)
    
    with open(FOLDER + "/map.txt", "w") as f:
        for row in rows:
            for i in range(0, 3):
                for chars in row:
                    f.write("".join(chars[i]))
                f.write("\n")

while step() != -1:

    if ps7.getValue() < 0.08:        
        if random() < 0.5:
            girar(0.25*math.tau) # Girar derecha
        else:
            girar(-0.25*math.tau) # Girar izquierda
    else:
        prev = tile(x, y)
        avanzar(0.12) # Avanzar 1 baldosa
            
        if direction == Direction.UP: y -= 1
        elif direction == Direction.RIGHT: x += 1
        elif direction == Direction.DOWN: y += 1
        elif direction == Direction.LEFT: x -= 1
        
        cur = tile(x, y)
        connectTiles(prev, cur, direction)
        writeGrid()

    l = ps5.getValue() < 0.1
    r = ps2.getValue() < 0.1
    f = ps7.getValue() < 0.1
    b = ps4.getValue() < 0.1
    print(f"F: {f}, R: {r}, B: {b}, L: {l}")
    print(direction)

    print([x, y])

    delay(1000)