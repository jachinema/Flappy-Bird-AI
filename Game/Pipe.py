from CONSTANTS import PIPE_SPRITE
import pygame as pg


class Pipe:
    def __init__(self, top_bottom, size):
        self.surface = top_bottom
        self.size = size
        self.sprite = pg.transform.rotate(pg.image.load(PIPE_SPRITE), 180 * top_bottom)

        self.x = 500
        self.y = ((not top_bottom) * 500) + ((size * 50) * -1)


