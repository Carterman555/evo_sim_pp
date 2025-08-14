import pygame
import numpy as np

def rotate(surface, angle, pivot, offset=pygame.Vector2(0,0)):
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)
    rotated_offset = offset.rotate(angle)
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect

def np_to_v2(np_array: np.array) -> pygame.Vector2:

    if len(np_array) != 2:
        raise Exception(f"Error: Try to convert np array {np_array} to vector2 not length is not 2")

    return pygame.Vector2(np_array[0], np_array[1])

def v2_to_np(vector2: pygame.Vector2) -> np.array:
    return np.array(vector2.x, vector2.y)