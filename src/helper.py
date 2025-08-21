import pygame
import numpy as np

def rotate(surface, angle, pivot, offset=pygame.Vector2(0,0)):
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)
    rotated_offset = offset.rotate(angle)
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect

def get_random_direction():
    angle = np.random.uniform(0, 2 * np.pi)
    return pygame.Vector2(np.cos(angle), np.sin(angle))

def np_to_v2(np_array: np.ndarray) -> pygame.Vector2:

    if not isinstance(np_array, np.ndarray):
        raise Exception(f"Error: Trying to convert numpy array to pygame vector2, but recieved {np_array} of type {type(np_array)}")

    if len(np_array) != 2:
        raise Exception(f"Error: Try to convert np array {np_array} to vector2 not length is not 2")

    return pygame.Vector2(np_array[0], np_array[1])


def valid_part_pos(dna, bone_index, pos_on_bone, width):
    bone_positions = dna.structure.get_edge_pos(bone_index)
    bone_vector = dna.get_bone_vector(bone_index).normalize()

    center = bone_positions[0] + (bone_vector * pos_on_bone)

    part_pos1 = center - ((width/2) * bone_vector)
    part_pos2 = center + ((width/2) * bone_vector)
    
    part_min_x = min(part_pos1[0], part_pos2[0])
    part_max_x = max(part_pos1[0], part_pos2[0])
    part_min_y = min(part_pos1[1], part_pos2[1])
    part_max_y = max(part_pos1[1], part_pos2[1])

    bone_min_x = min(bone_positions[0][0], bone_positions[1][0])
    bone_max_x = max(bone_positions[0][0], bone_positions[1][0])
    bone_min_y = min(bone_positions[0][1], bone_positions[1][1])
    bone_max_y = max(bone_positions[0][1], bone_positions[1][1])

    within_bone_bounds = (part_min_x >= bone_min_x and part_max_x <= bone_max_x and
        part_min_y >= bone_min_y and part_max_y <= bone_max_y)
    return within_bone_bounds