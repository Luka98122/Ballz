from math import radians, trunc
import pygame as pg, sys
from pygame import key
from pygame.locals import *
import pygamebg as pgbg
import random as rand
import keyboard
import math


cooldown = 300
turns = 0
ghostBallz = []
mode = 0
ds = [5, 5]


class Aimer:
    global ds
    angle = 270
    spaceAimBalls = 65
    global mode

    def update(self):
        global mode
        global ds
        ds = Ball.angleToDs(self, self.angle)
        minim = 190
        maxim = 350

        if keyboard.is_pressed("left arrow"):
            self.angle = max(self.angle - 0.1, minim)
        if keyboard.is_pressed("right arrow"):
            self.angle = min(self.angle + 0.1, maxim)
        if keyboard.is_pressed("enter"):
            mode = 1

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
    needaiming = 0
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
        global mode
        global ds
        if mode == 0:
            aimer.update()

        if mode == 1:
            self.dx = ds[0]
            self.dy = ds[1]
            mode = 2

        if mode == 2:

            self.x = self.x + self.dx
            self.y = self.y + self.dy
            if self.x > 990:
                self.dx = -self.dx
            if self.x < 10:
                self.dx = -self.dx
            if self.y < 10:
                self.dy = -self.dy
            # k = ballBlockCollision(self.x, self.y, self.dx, self.dy,)
            # self.x = k[0]
            # self.y = k[1]
            # self.dx = k[2]
            # self.dy = k[3]


class Block:
    hp = 5
    x = 0
    y = 0
    size = 100

    def draw(self):
        pg.draw.rect(
            canvas,
            pg.Color("Orange"),
            (
                self.x * self.size + 10 * self.x,
                self.y * self.size + 10 * self.y,
                self.size,
                self.size,
            ),
        )


listOfBlocks = []
listOfBallz = []


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
                dx = -dx
            if y < rectTY:
                dy = -dy
            if y > rectBY:
                dy = -dy
        # Update ball position for next tick
        x = x + dx
        y = y + dy
    return (collision, x, y, dx * 10, dy * 10)


def generateLayer():
    newNum = 1
    numBlocks = rand.randint(3, 5)

    for i in range(numBlocks):
        block1 = Block()
        listOfBlocks.append(block1)
        while True:
            Pos = rand.randint(0, 7)
            for j in range(len(listOfBlocks)):
                if Pos == listOfBlocks[j].x and listOfBlocks[j].y == 0:
                    newNum = 0
            if newNum == 1:
                listOfBlocks[i].x = Pos
                break
            newNum = 1


def update():
    canvas.fill(pg.Color("White"))
    global cooldown
    global turns
    cooldown = cooldown - 1

    if keyboard.is_pressed("n") and cooldown < 0:
        for i in range(len(listOfBlocks)):
            listOfBlocks[i].y += 1
        generateLayer()
        turns = turns + 1
        cooldown = 300

        ball1 = Ball()
        listOfBallz.append(ball1)
        if len(listOfBallz) == 1:
            ball1.needaiming = 1
    for i in range(len(listOfBallz)):
        listOfBallz[i].update()
    for i in range(len(listOfBlocks)):
        listOfBlocks[i].draw()
    for i in range(len(listOfBallz)):
        listOfBallz[i].draw()
    if mode == 0:
        aimer.draw()


windowWidth = 1000
windowHeight = 1000
pg.init()
DISPLAYSURF = pg.display.set_mode((400, 300))
canvas = pgbg.open_window(windowWidth, windowHeight, "window.")
canvas.fill(pg.Color("White"))
pg.display.set_caption("Hello World!")
generateLayer()
while True:  # main game loop
    update()
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    pg.display.update()
