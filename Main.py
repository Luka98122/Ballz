import pygame as pg, sys
from pygame.locals import *
import pygamebg as pgbg
import random as rand


class Block:
    hp = 5
    x = 0
    y = 0


def generateLayer():
    newNum = 1
    numBlocks = rand.randint(3, 7)
    BlockPositions = [0, 0, 0, 0, 0, 0, 0]
    for i in range(numBlocks):
        while True:
            Pos = rand.randint(1, 7)
            for j in range(numBlocks):
                if Pos == BlockPositions[j]:
                    newNum = 0
            if newNum == 1:
                BlockPositions[i] = Pos
                break
            newNum = 1
    for i in range(numBlocks):
        pg.draw.rect(
            canvas,
            pg.Color("Orange"),
            (BlockPositions[i] * 100 + 10 * BlockPositions[i], 0, 100, 100),
        )


windowWidth = 1000
windowHeight = 1000
pg.init()
DISPLAYSURF = pg.display.set_mode((400, 300))
canvas = pgbg.open_window(windowWidth, windowHeight, "window.")
canvas.fill(pg.Color("White"))
pg.display.set_caption("Hello World!")
generateLayer()
while True:  # main game loop
    pg.draw.rect(
        canvas,
        pg.Color("Red"),
        (windowWidth / 2 - 100, windowHeight / 2 - 100, 200, 200),
    )
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    pg.display.update()
