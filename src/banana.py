import pygame, os
from constants import IMAGE_PATH
from zoomer import Zoomer

class Banana(pygame.sprite.Sprite):
    _instances = list()

    def __init__(self, pos):
        super().__init__()

        Banana._instances.append(self)

        self.image = pygame.image.load(os.path.join(IMAGE_PATH, 'banana.png')).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 0.15)

        self.rect = self.image.get_rect(center=pos)

    def update(self):
        pass

    def draw(self):
        Zoomer.draw_surf(self.image, self.rect)

    def kill(self):
        Banana._instances.pop(Banana._instances.index(self))
