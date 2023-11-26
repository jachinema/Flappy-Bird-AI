from CONSTANTS import UP_SPRITE
import pygame as pg
from Vector import Vector2D


class Bird:
    possible_sprites = [pg.image.load(UP_SPRITE)]

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.current_sprite = Bird.possible_sprites[0]
        self.death = False
        self.can_jump = True
        self.jumping = False
        self.jump_start_tick = -1

        self.momentum = Vector2D(0, 0)
