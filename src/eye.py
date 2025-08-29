import pygame

from creaturepart import CreaturePart
from helper import rotate

class Eye(CreaturePart):
    def __init__(self, creature, data):
        super().__init__(creature, data)

    def draw(self, creature_surf):
        self.image.fill('white')

        angle = pygame.Vector2(1,0).angle_to(self.bone_vector)

        rotated_image, rotated_rect = rotate(self.image, angle, self.rect.center)
        creature_surf.blit(rotated_image, rotated_rect)