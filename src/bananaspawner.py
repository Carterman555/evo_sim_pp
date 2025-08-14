import pygame
from banana import Banana

class BananaSpawner:
    def __init__(self, updatable, drawable):
        
        test_pos = pygame.Vector2(650,450)
        banana = Banana(test_pos)

        updatable.add(banana)
        drawable.add(banana)
