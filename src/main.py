import pygame
from sys import exit

from creature import Creature
from creaturepart import CreaturePartData
from dna import DNA
from mouth import Mouth
from mutate_dna import mutate_dna

from bananaspawner import BananaSpawner

from constants import *
from enums import BoneSide


def main():
    
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    joints = [[0, 0], [75, 0], [50, 50], [0, 50]]
    bones = [(0,1), (1,2), (2,3), (3,0)]
    # booster_data = [CreaturePartData(bone_index=0,side=BoneSide.BOTTOM,pos_on_bone=100,size=30)]
    # mouth_data = [CreaturePartData(bone_index=2,side=BoneSide.BOTTOM,pos_on_bone=25,size=20)]
    booster_data = []
    mouth_data = []

    dna = DNA(joints, bones, booster_data, mouth_data)
    Creature(updatable, dna, (200, SCREEN_HEIGHT/2))

    for x in range(1):
        dna = mutate_dna(dna)
        Creature(updatable, dna, (310 + 200*x, SCREEN_HEIGHT/2))


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