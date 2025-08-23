import pygame
from numpy.random import randint

from banana import Banana
from environment import Environment
from constants import *
from settings import Settings

class BananaSpawner:
    def __init__(self):

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

        spawned_banana = False
        attempts = 0
        max_attempts = 100
        while not spawned_banana:
            attempts += 1
            if attempts >= max_attempts:
                break

            padding = 40

            x = randint(WORLD_BOUNDS.left + padding, WORLD_BOUNDS.right - padding)
            y = randint(WORLD_BOUNDS.top + padding, WORLD_BOUNDS.bottom - padding)

            banana = Banana(pygame.Vector2(x,y))

            if Environment.rect_in_env(banana.rect):
                spawned_banana = True
            else:
                banana.kill()