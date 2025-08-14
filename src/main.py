import pygame
from sys import exit
from creature import Creature
from bananaspawner import BananaSpawner
from constants import *

def main():
    
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Creature((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), updatable)
    bananaspawner = BananaSpawner(updatable, drawable)

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

        # Updates
        updatable.update()

        # so set doesn't change while looping when creature dies 
        creatures = Creature._instances.copy()
        for creature in creatures:
            creature.update()

        bananaspawner.update()

        # Draws
        screen.fill("#85B889")

        drawable.draw(screen)

        for creature in Creature._instances:
            creature.draw(screen)
        
        pygame.display.update()
        clock.tick(30)

        

if __name__ == "__main__":
    main()