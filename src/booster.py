import pygame
from creaturepart import CreaturePartData
from creaturepart import CreaturePart

from helper import *

class Booster(CreaturePart):
    def __init__(self, creature, data: CreaturePartData):
        super().__init__(creature, data)

    def draw(self, creature_surf):
        self.image.fill('cyan')

        angle = pygame.Vector2(1,0).angle_to(self.bone_vector)
        
        rotated_image, rotated_rect = rotate(self.image, angle, self.rect.center)
        creature_surf.blit(rotated_image, rotated_rect)

    def force_vector(self) -> pygame.Vector2:
        return self.direction.rotate(self.creature.angle) * self.data.size * 0.1