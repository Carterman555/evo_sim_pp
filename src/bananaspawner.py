import pygame
from numpy.random import randint

from banana import Banana
from constants import *
from settings import Settings

class BananaSpawner:
    def __init__(self, world_bounds):

        self.world_bounds: pygame.Rect = world_bounds

        # banana = Banana((650,450))

        self.spawn_timer = BANANA_SPAWN_COOLDOWN

    def update(self):

        if not Settings.spawn_bananas:
            return

        self.spawn_timer -= 1
        if self.spawn_timer <= 0 and len(Banana._instances) < MAX_BANANAS:
            self.spawn_timer = BANANA_SPAWN_COOLDOWN

            self.spawn_banana()

    def spawn_banana(self):
        padding = 40

        x = randint(self.world_bounds.left + padding, self.world_bounds.right - padding)
        y = randint(self.world_bounds.top + padding, self.world_bounds.bottom - padding)

        Banana(pygame.Vector2(x,y))