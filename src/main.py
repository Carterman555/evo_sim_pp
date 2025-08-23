import pygame
from sys import exit
import numpy as np

from creature import Creature
from banana import Banana

from environment import Environment
from creaturespawner import CreatureSpawner
from bananaspawner import BananaSpawner

from constants import *
from enums import *
from settings import Settings
from zoomer import Zoomer

def main():

    # np.random.seed(69)

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    Zoomer.screen = screen

    clock = pygame.time.Clock()

    creaturespawner = CreatureSpawner()
    bananaspawner = BananaSpawner()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    print(f"FPS: {clock.get_fps():.2f}")
                if event.key == pygame.K_r:
                    Settings.show_creature_rects = not Settings.show_creature_rects
                
                if event.key == pygame.K_q:
                    Settings.draw = not Settings.draw
                    screen.fill("black")

                if Settings.draw:
                    if event.key == pygame.K_0:
                        Settings.frame_rate = 0
                    if event.key == pygame.K_1:
                        Settings.frame_rate = 10
                    if event.key == pygame.K_2:
                        Settings.frame_rate = 20
                    if event.key == pygame.K_3:
                        Settings.frame_rate = 30
                    if event.key == pygame.K_4:
                        Settings.frame_rate = 40
                    if event.key == pygame.K_5:
                        Settings.frame_rate = 50
                    if event.key == pygame.K_6:
                        Settings.frame_rate = 60
                    if event.key == pygame.K_7:
                        Settings.frame_rate = 70
                    if event.key == pygame.K_8:
                        Settings.frame_rate = 80
                    if event.key == pygame.K_9:
                        Settings.frame_rate = 10000
                    

                if event.key == pygame.K_e:
                    Settings.show_energy = not Settings.show_energy

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    Zoomer.zoom_in()
                elif event.y < 0:
                    Zoomer.zoom_out()

        Zoomer.handle_panning()

        # Updates
        creaturespawner.update()
        bananaspawner.update()

        # while loop so to handle when creature dies
        creature_index = 0
        while creature_index < len(Creature._instances):
            Creature._instances[creature_index].update()
            creature_index += 1


        # Draws
        if Settings.draw:
            screen.fill("#738B75")

            Environment.draw()

            for creature in Creature._instances:
                creature.draw()

            for banana in Banana._instances:
                banana.draw()

        
        pygame.display.update()

        frame_rate = Settings.frame_rate if Settings.draw else 10000
        clock.tick(frame_rate)

        

if __name__ == "__main__":
    main()