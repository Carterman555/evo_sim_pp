import pygame
from sys import exit
from creature import Creature

def main():
    
    pygame.init()

    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH,HEIGHT))

    clock = pygame.time.Clock()
    dt = 0

    creature = Creature(WIDTH/2, HEIGHT/2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Updates
        creature.update(dt)

        # Draws
        screen.fill("#85B889")

        creature.draw(screen)

        pygame.display.update()
        dt = clock.tick(30) / 1000

if __name__ == "__main__":
    main()