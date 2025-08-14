import pygame
from helper import *
from creaturepart import CreaturePart

class Booster(CreaturePart):
    def __init__(self, creature, bone_index, side, pos_on_bone, size, *groups):
        super().__init__(creature, bone_index, side, pos_on_bone, size, *groups)


    def draw(self, creature_surf):
        self.image.fill('cyan')

        angle = pygame.Vector2(1,0).angle_to(self.bone_vector)
        
        rotated_image, rotated_rect = rotate(self.image, angle, self.rect.center)
        creature_surf.blit(rotated_image, rotated_rect)

    def force_vector(self) -> pygame.Vector2:
        return self.direction.rotate(self.creature.angle) * self.size * 0.01