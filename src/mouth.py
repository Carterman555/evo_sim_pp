import pygame
from creaturepart import CreaturePart
from banana import Banana
from constants import BANANA_ENERGY_GAIN
from helper import *

class Mouth(CreaturePart):
    def __init__(self, creature, data, *groups):
        super().__init__(creature, data, *groups)


    def draw(self, creature_surf):
        self.image.fill('pink')

        angle = pygame.Vector2(1,0).angle_to(self.bone_vector)

        rotated_image, rotated_rect = rotate(self.image, angle, self.rect.center)
        creature_surf.blit(rotated_image, rotated_rect)

    def update(self):
        for banana in Banana._instances:
            part_lpos1 = self.rect.center - ((self.data.size/2) * self.bone_vector)
            part_lpos2 = self.rect.center + ((self.data.size/2) * self.bone_vector)

            part_gpos1 = self.creature.global_pos(part_lpos1)
            part_gpos2 = self.creature.global_pos(part_lpos2)

            if banana.rect.clipline((part_gpos1, part_gpos2)):
                self.eat(banana)

    def eat(self, banana):
        banana.kill()

        self.creature.energy += BANANA_ENERGY_GAIN
        self.creature.energy = min(self.creature.energy, self.creature.max_energy)

