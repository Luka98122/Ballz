# from _typeshed import Self
from math import radians, trunc
import pygame as pg, sys
from pygame import key
import pygame
from pygame.locals import *
import pygamebg as pgbg
import random as rand
import keyboard
import math
import os

listOfBlocks = []
cooldown = 300
turns = 0
ghostBallz = []
ds = [5, 5]
BLOCK_SIZE = 100
MODE_BOUNCING = 0
MODE_AIMING = 1
mode = MODE_AIMING
windowWidth = 1000
windowHeight = 1000
SUBDIVIDE = 1


class Aimer:
    global ds
    angle = 270
    spaceAimBalls = 65
    global mode

    def update(self):
        global mode
        global ds
        ds = Ball.angleToDs(self, self.angle)
        minim = 181
        maxim = 350

        if keyboard.is_pressed("left arrow"):
            self.angle = max(self.angle - 0.1, minim)
        if keyboard.is_pressed("right arrow"):
            self.angle = min(self.angle + 0.1, maxim)
        if keyboard.is_pressed("enter") and mode == MODE_AIMING:
            mode = MODE_BOUNCING
            ds = Ball.angleToDs(self, self.angle)
            return

    def draw(self):
        global mode
        if mode == MODE_AIMING:
            for i in range(16):
                pg.draw.circle(
                    canvas,
                    pg.Color("Green"),
                    (
                        listOfBallz[0].x + ds[0] * i * self.spaceAimBalls,
                        windowHeight + ds[1] * i * self.spaceAimBalls,
                    ),
                    20,
                )


aimer = Aimer()


class Ball:
    x = 500
    y = 990
    dx = 0
    dy = 0
    width = 20

    def draw(self):
        pg.draw.circle(canvas, pg.Color("Red"), (self.x, self.y), self.width)

    def angleToDs(self, angle):
        radian = math.radians(angle)
        dx = math.cos(radian)
        dy = math.sin(radian)
        return (dx, dy)

    def update(self):
        global aimer
        global ds
        global listOfBlocks
        global mode

        if self.y == 1000:
            mode = MODE_AIMING

        if mode == MODE_AIMING:
            aimer.update()
            self.dx = ds[0]
            self.dy = ds[1]

        if mode == MODE_BOUNCING:
            self.x = self.x + self.dx
            self.y = self.y + self.dy
            if self.x > 990:
                self.dx = -self.dx
            if self.x < 10:
                self.dx = -self.dx
            if self.y < 10:
                self.dy = -self.dy

        for j in range(len(listOfBlocks)):
            blockTopX = listOfBlocks[j].x * BLOCK_SIZE  # + listOfBlocks[j].offset
            blockTopY = listOfBlocks[j].y * BLOCK_SIZE  # + listOfBlocks[j].offset
            blockBottomX = blockTopX + listOfBlocks[j].size
            blockBottomY = blockTopY + listOfBlocks[j].size

            # FIXME: Remove magic value
            returnie = ballBlockCollision(
                self.x,
                self.y,
                self.dx,
                self.dy,
                blockTopX,
                blockTopY,
                blockBottomX,
                blockBottomY,
                j,
            )
            if returnie[0] == 1:
                self.x = returnie[1]
                self.y = returnie[2]
                self.dx = returnie[3]
                self.dy = returnie[4]
                break


class Block:
    hp = 5
    x = 0
    y = 1
    size = BLOCK_SIZE
    offset = 10

    # def getCollisionBox()

    def draw(self):

        pg.draw.rect(
            canvas,
            pg.Color("Orange"),
            (
                self.x * (self.size + self.offset),
                self.y * (self.size + self.offset),
                self.size,
                self.size,
            ),
        )


Tester = Block()
Tester.x = 7
Tester.y = 7
listOfBlocks.append(Tester)

listOfBallz = []


def GridToPixels(x):
    return x * Block.size


# Something is wrong here. Blocks are correctly positioned, it is not detecting collision. except for top left corner
def ballBlockCollision(x, y, dx, dy, rectTX, rectTY, rectBX, rectBY, brickNUM):
    collision = 0
    #    if x + dx <
    dx = dx / SUBDIVIDE
    dy = dy / SUBDIVIDE
    for i in range(SUBDIVIDE):
        # Will the ball end up inside the rect on this tick?
        x1 = x + dx
        y1 = y + dy
        leftOffset = Block.offset * brickNUM
        topOffset = Block.offset * brickNUM
        if keyboard.is_pressed("p"):
            a = 3
        if keyboard.is_pressed("h"):
            pygame.draw.rect(
                canvas,
                pygame.Color("Purple"),
                (
                    rectTX + leftOffset,
                    rectTY + leftOffset,
                    rectBX,
                    rectBY,
                ),
            )
        if (
            x1 > rectTX + leftOffset
            and x1 < rectBX
            and y1 > rectTY + topOffset
            and y1 < rectBY
        ):
            if keyboard.is_pressed("p"):
                a = 3
            # In this tick, the ball went from outside to inside
            collision = 1
            if x < rectTX:
                # Ball is to the left of left wall
                dx = -dx
                break
            if x > rectBX:
                # Ball is to the right of right wallnn
                dx = -dx
                break
            if y < rectTY:
                # Ball is above the block
                dy = -dy
                break
            if y > rectBY:
                # Ball is bellow the block
                dy = -dy
                break
        # Update ball position for next tick
        x = x + dx
        y = y + dy
    return (collision, x, y, dx * SUBDIVIDE, dy * SUBDIVIDE)


def CheckToStopBall():
    for i in range(len(listOfBallz)):
        if listOfBallz[i].y > windowHeight:
            listOfBallz[i].dx = 0
            listOfBallz[i].dy = 0
            listOfBallz[i].y = windowHeight
            listOfBallz[i].mode = MODE_AIMING


def generateLayer():
    newNum = 1
    numBlocks = rand.randint(3, 5)

    for i in range(numBlocks):
        tempBlock = Block()
        xPos = rand.randint(0, 8)
        NewBlock = Block()

        # Checking to see if taken
        if len(listOfBlocks) == 0:
            listOfBlocks.append(tempBlock)
            tempBlock.x = -1
        for j in range(len(listOfBlocks)):
            while True:
                if listOfBlocks[j].x == xPos and listOfBlocks[j].y == 1:
                    newNum = 0
                    xPos = rand.randint(0, 7)
                if newNum == 1:
                    listOfBlocks.append(NewBlock)
                    NewBlock.x = xPos
                    break
            break


ball1 = Ball()
listOfBallz.append(ball1)
if len(listOfBallz) == 1:
    ball1.mode = MODE_AIMING
    ball1.y = windowHeight - 1


def clearGoneBlocks():
    for i in range(len(listOfBlocks)):
        if listOfBlocks[i].y > 9:
            listOfBlocks.remove[i]


def update():
    canvas.fill(pg.Color("White"))
    CheckToStopBall()
    global cooldown
    global turns
    cooldown = cooldown - 1

    # for j in range(len(listOfBlocks)):
    # if listOfBlocks[j].y == 8:
    # exit()

    if keyboard.is_pressed("n") and cooldown < 0:
        for i in range(len(listOfBlocks)):
            listOfBlocks[i].y += 1
        generateLayer()
        turns = turns + 1
        cooldown = 300
        if len(listOfBallz) == 1:
            ball1.mode = MODE_AIMING

    if keyboard.is_pressed("esc"):
        exit()

    for i in range(len(listOfBallz)):
        listOfBallz[i].update()
    for i in range(len(listOfBlocks)):
        listOfBlocks[i].draw()
    for i in range(len(listOfBallz)):
        listOfBallz[i].draw()
        if listOfBallz[i].mode == MODE_AIMING:
            aimer.draw()


pg.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = "200,20"
DISPLAYSURF = pg.display.set_mode((400, 300))
canvas = pgbg.open_window(windowWidth, windowHeight, "window.")
canvas.fill(pg.Color("White"))
pg.display.set_caption("Hello World!")
# generateLayer()
while True:  # main game loop
    update()
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    pg.display.update()
