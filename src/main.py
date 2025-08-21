import pygame
from sys import exit

from creature import Creature
from banana import Banana
from creaturepart import CreaturePartData
from dna import DNA
from mouth import Mouth

from creaturespawner import CreatureSpawner
from bananaspawner import BananaSpawner

from constants import *
from enums import *
from settings import Settings
from zoomer import Zoomer

def main():
    
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    Zoomer.screen = screen

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    print(f"FPS: {clock.get_fps():.2f}")
                if event.key == pygame.K_r:
                    list(Creature._instances)[0].reproduce()
                
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
        updatable.update()

        creaturespawner.update()
        bananaspawner.update()

        # possible speed up - copying might use up a lot of memory
        # copy so set doesn't change while looping when creature dies
        creatures = Creature._instances.copy()
        for creature in creatures:
            creature.update()

        # Draws
        if Settings.draw:
            screen.fill("#738B75")
            Zoomer.draw_rect(world_bounds, '#85B889')

            for creature in Creature._instances:
                creature.draw()

            for banana in Banana._instances:
                banana.draw()

        
        pygame.display.update()

        frame_rate = Settings.frame_rate if Settings.draw else 10000
        clock.tick(frame_rate)

        

if __name__ == "__main__":
    main()