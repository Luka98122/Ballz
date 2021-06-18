import pygame as pg, sys
from pygame.locals import *
import pygamebg as pgbg
import random as rand
import keyboard


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


def generateLayer():
    newNum = 1
    numBlocks = rand.randint(3, 7)

    for i in range(numBlocks):
        for k in range(7):
            block1 = Block()
            listOfBlocks.append(block1)
        while True:
            Pos = rand.randint(1, 7)
            for j in range(len(listOfBlocks)):
                if Pos == listOfBlocks[j].x and listOfBlocks[j].y == 0:
                    newNum = 0
            if newNum == 1:
                listOfBlocks[i].x = Pos
                break
            newNum = 1


def update():
    if keyboard.is_pressed("n"):
        for i in range(len(listOfBlocks)):
            listOfBlocks[i].y += 1
        generateLayer()
    for i in range(len(listOfBlocks)):
        listOfBlocks[i].draw()


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
