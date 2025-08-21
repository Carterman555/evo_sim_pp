import pygame
from sys import exit
import numpy as np

from creature import Creature

from creaturespawner import CreatureSpawner
from bananaspawner import BananaSpawner

from constants import *
from enums import *

def main():

    max_frames = 1000
    frame = 0

    seed = 69

    np.random.seed(seed)

    pygame.init()

    pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()

    screen_centerx = SCREEN_WIDTH/2
    screen_centery = SCREEN_HEIGHT/2
    world_bounds = pygame.Rect((-WORLD_WIDTH/2 + screen_centerx,-WORLD_HEIGHT/2 + screen_centery), (WORLD_WIDTH, WORLD_HEIGHT))

    creaturespawner = CreatureSpawner(updatable, world_bounds)
    bananaspawner = BananaSpawner(updatable, world_bounds)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Updates
        updatable.update()

        creaturespawner.update()
        bananaspawner.update()

        # while loop so to handle when creature dies
        creature_index = 0
        while creature_index < len(Creature._instances):
            Creature._instances[creature_index].update()
            creature_index += 1

        clock.tick(10000)

        frame += 1
        if frame >= max_frames:

            seconds = pygame.time.get_ticks() / 1000
            print(f"Simulating {frame} frames took {seconds} seconds")

            pygame.quit()
            exit()
        

if __name__ == "__main__":
    main()