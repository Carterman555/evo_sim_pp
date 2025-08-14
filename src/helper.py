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


def valid_part_pos(creature, bone_index, pos_on_bone, width):
    bone_positions = creature.dna.get_bone_pos(bone_index)
    bone_vector = creature.dna.get_bone_vector(bone_index).normalize()

    center = bone_positions[0] - (bone_vector * pos_on_bone)

    part_pos1 = center - ((width/2) * bone_vector)
    part_pos2 = center + ((width/2) * bone_vector)
    
    booster_min_x = min(part_pos1[0], part_pos2[0])
    booster_max_x = max(part_pos1[0], part_pos2[0])
    booster_min_y = min(part_pos1[1], part_pos2[1])
    booster_max_y = max(part_pos1[1], part_pos2[1])

    bone_min_x = min(bone_positions[0][0], bone_positions[1][0])
    bone_max_x = max(bone_positions[0][0], bone_positions[1][0])
    bone_min_y = min(bone_positions[0][1], bone_positions[1][1])
    bone_max_y = max(bone_positions[0][1], bone_positions[1][1])

    within_bone_bounds = (booster_min_x >= bone_min_x and booster_max_x <= bone_max_x and
        booster_min_y >= bone_min_y and booster_max_y <= bone_max_y)
    return within_bone_bounds