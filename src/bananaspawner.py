import pygame
from numpy.random import randint

from banana import Banana
from constants import *

class BananaSpawner:
    def __init__(self, updatable, drawable):

        self.updatable = updatable
        self.drawable = drawable

        # banana = Banana((650,450))
        # self.updatable.add(banana)
        # self.drawable.add(banana)

        self.spawn_timer = BANANA_SPAWN_COOLDOWN

    def update(self):

        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_timer = BANANA_SPAWN_COOLDOWN

            # self.spawn_banana()

    def spawn_banana(self):
        padding = 40

        pos = pygame.Vector2(randint(padding, SCREEN_WIDTH-padding), randint(padding, SCREEN_HEIGHT-padding))
        banana = Banana(pos)

        self.updatable.add(banana)
        self.drawable.add(banana)
