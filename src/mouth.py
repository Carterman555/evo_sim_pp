import pygame
from creaturepart import CreaturePart
from banana import Banana
from helper import *

class Mouth(CreaturePart):
    def __init__(self, creature, bone_index, side, pos_on_bone, size, *groups):
        super().__init__(creature, bone_index, side, pos_on_bone, size, *groups)


    def draw(self, creature_surf):
        self.image.fill('pink')

        angle = pygame.Vector2(1,0).angle_to(self.bone_vector)

        part_lpos1 = self.rect.center - ((self.size/2) * self.bone_vector)
        part_lpos2 = self.rect.center + ((self.size/2) * self.bone_vector)

        pygame.draw.circle(creature_surf, 'pink', part_lpos1, 6)
        pygame.draw.circle(creature_surf, 'pink', part_lpos2, 6)
        
        rotated_image, rotated_rect = rotate(self.image, angle, self.rect.center)
        creature_surf.blit(rotated_image, rotated_rect)

    def update(self):
        for banana in Banana._instances:
            part_lpos1 = self.rect.center - ((self.size/2) * self.bone_vector)
            part_lpos2 = self.rect.center + ((self.size/2) * self.bone_vector)

            part_gpos1 = self.creature.global_pos(part_lpos1 - self.creature.offset)
            part_gpos2 = self.creature.global_pos(part_lpos2 - self.creature.offset)

            if banana.rect.clipline((part_gpos1, part_gpos2)):
                banana.kill()
    
