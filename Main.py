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
mode = MODE_BOUNCING


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
        if keyboard.is_pressed("enter"):
            mode = MODE_BOUNCING
            return

    def draw(self):
        for i in range(16):
            pg.draw.circle(
                canvas,
                pg.Color("Green"),
                (
                    500 + ds[0] * i * self.spaceAimBalls,
                    1000 + ds[1] * i * self.spaceAimBalls,
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
        if mode == MODE_AIMING:
            aimer.update()

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
            # FIXME: Remove magic value
            blockTopX = listOfBlocks[j].x * BLOCK_SIZE + listOfBlocks[j].offset
            blockTopY = listOfBlocks[j].y * BLOCK_SIZE + listOfBlocks[j].offset
            blockBottomX = blockTopX + listOfBlocks[j].size
            blockBottomY = blockTopY + listOfBlocks[j].size
            returnie = ballBlockCollision(
                self.x,
                self.y,
                self.dx,
                self.dy,
                blockTopX,
                blockTopY,
                blockBottomX,
                blockBottomY,
            )
            if returnie[0] == 1:
                self.x = returnie[1]
                self.y = returnie[2]
                self.dx = returnie[3]
                self.dy = returnie[4]
                break

            # k = ballBlockCollision(self.x, self.y, self.dx, self.dy,)
            # self.x = k[0]
            # self.y = k[1]
            # self.dx = k[2]
            # self.dy = k[3]


class Block:
    hp = 5
    x = 0
    y = 1
    size = BLOCK_SIZE
    offset = 10

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

# Something is wrong here. Blocks are correctly positioned, it is not detecting collision. except for top left corner
def ballBlockCollision(x, y, dx, dy, rectTX, rectTY, rectBX, rectBY):
    collision = 0
    dx = dx * 0.1
    dy = dy * 0.1
    for i in range(10):
        # Will the ball end up inside the rect on this tick?
        x1 = x + dx
        y1 = y + dy

        if x1 > rectTX and x1 < rectBX and y1 > rectTY and y1 < rectBY:
            # In this tick, the ball went from outside to inside
            collision = 1
            if x < rectTX:
                # Ball is to the left of left wall
                dx = -dx
            if x > rectBX:
                # Ball is to the right of right wall
                dx = -dx
            if y < rectTY:
                # Ball is above the block
                dy = -dy
            if y > rectBY:
                # Ball is bellow the block
                dy = -dy
        # Update ball position for next tick
        x = x + dx
        y = y + dy
    return (collision, x, y, dx * 10, dy * 10)


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
        xPos = rand.randint(0, 7)
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


windowWidth = 1000
windowHeight = 1000
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
