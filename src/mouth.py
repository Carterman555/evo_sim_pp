import pygame
from creaturepart import CreaturePart
from banana import Banana
from constants import BANANA_ENERGY_GAIN
from helper import *

class Mouth(CreaturePart):
    def __init__(self, creature, data):
        super().__init__(creature, data)


    def draw(self, creature_surf):
        self.image.fill('pink')

        angle = pygame.Vector2(1,0).angle_to(self.bone_vector)

        rotated_image, rotated_rect = rotate(self.image, angle, self.rect.center)
        creature_surf.blit(rotated_image, rotated_rect)


    def update(self):

        # while loop because eating banana modifies list
        banana_index = 0
        while banana_index < len(Banana._instances):
            banana: Banana = Banana._instances[banana_index]

            if not self.creature.rect.colliderect(banana.rect):
                banana_index += 1
                continue

            part_lpos1 = self.rect.center - ((self.data.size/2) * self.bone_vector)
            part_lpos2 = self.rect.center + ((self.data.size/2) * self.bone_vector)

            part_gpos1 = self.creature.global_pos(part_lpos1)
            part_gpos2 = self.creature.global_pos(part_lpos2)

            if banana.rect.clipline((part_gpos1, part_gpos2)):
                self.creature.eat(banana)

            banana_index += 1

    

