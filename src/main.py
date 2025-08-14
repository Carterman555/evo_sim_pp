import pygame
from sys import exit
from creature import Creature
from bananaspawner import BananaSpawner
from bananaspawner import Banana

from mouth import Mouth

def main():
    
    pygame.init()

    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH,HEIGHT))

    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    creatures = [Creature(WIDTH/2, HEIGHT/2, updatable)]
    bananaspawner = BananaSpawner(updatable, drawable)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Updates
        updatable.update()

        creatures = list(filter(lambda creature: not creature.dead, creatures))
        for creature in creatures:
            creature.update()
        # bananaspawner.update()

        # Draws
        screen.fill("#85B889")

        drawable.draw(screen)

        for creature in creatures:
            creature.draw(screen)
        
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()