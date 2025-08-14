import pygame, os, weakref
from constants import IMAGE_PATH

class Banana(pygame.sprite.Sprite):
    _instances = weakref.WeakSet()

    def __init__(self, pos):
        super().__init__()

        Banana._instances.add(self)

        self.image = pygame.image.load(os.path.join(IMAGE_PATH, 'banana.png')).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 0.15)

        self.rect = self.image.get_rect(center=pos)

    def update(self):
        pass
