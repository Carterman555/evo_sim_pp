import pygame, random
import numpy as np
from numpy import random as nr

from dna import DNA
from creaturepart import CreaturePartData

from constants import *
from enums import *
from helper import *

def mutate_dna(dna: DNA) -> DNA:

    mutated_dna = dna.get_copy()

    remove_bone(mutated_dna)

    # for i in range(len(mutated_dna.structure.vertices)):
    #     if MOVE_JOINT_PROB * TEST_PROB_MULT > nr.rand():
    #         move_joint(mutated_dna, i)


    # if ADD_JOINT_PROB * TEST_PROB_MULT > nr.rand():
    #     add_joint(mutated_dna)


    # if ADD_BONE_PROB * TEST_PROB_MULT > nr.rand():
    #     add_bone(mutated_dna)


    # if REMOVE_BONE_PROB * TEST_PROB_MULT > nr.rand():
    #     remove_bone(mutated_dna)

    
    # parts_data = all_part_data(mutated_dna)
    # for part_data in parts_data:
    #     if MOVE_PART_PROB * TEST_PROB_MULT > nr.rand():
    #         move_part(mutated_dna, part_data)
    #     if RESIZE_PART_PROB * TEST_PROB_MULT > nr.rand():
    #         resize_part(mutated_dna, part_data)


    # if ADD_PART_PROB * TEST_PROB_MULT > nr.rand():
    #     add_part(mutated_dna)


    # parts_amount = len(all_part_data(mutated_dna))
    # if parts_amount > 0 and REMOVE_PART_PROB * TEST_PROB_MULT > nr.rand():
    #     remove_rand_part(mutated_dna)


    mutated_dna.structure.normalize_vertices()
    return mutated_dna


def move_joint(dna: DNA, joint_index: int):

    connected_bone_indices = np.where(dna.structure.edges == joint_index)[0].tolist()
    og_bone_lengths = [(i, dna.get_bone_vector(i).magnitude()) for i in connected_bone_indices]

    # move the joint
    move_vector = pygame.Vector2(nr.randn()*AVG_JOINT_MOVE_AMOUNT, nr.randn()*AVG_JOINT_MOVE_AMOUNT)
    dna.structure.vertices[joint_index] = np.array(dna.structure.vertices[joint_index] + move_vector)

    # move and resize parts if needed
    for part_data in all_part_data(dna):
        if part_data.bone_index in connected_bone_indices:

            og_length = next((length_tup[1] for length_tup in og_bone_lengths if length_tup[0] == part_data.bone_index), None)
            new_length = dna.get_bone_vector(part_data.bone_index).magnitude()
            bone_length_change = new_length - og_length

            # handle the logic different whether moving the first or second joint because parts are positioned
            # pos_on_bone distance away from the first joint and not from the second

            # If the first joint was moved, change pos_on_bone for all parts on that bone. 
            moved_first_joint = dna.structure.edges[part_data.bone_index][0] == joint_index
            if moved_first_joint:
                part_data.pos_on_bone += bone_length_change

                # If bone shrunk, and there is a part near the joint, shrink the part.
                distance_from_joint = part_data.pos_on_bone
                if distance_from_joint < part_data.size/2:

                    og_pos = part_data.pos_on_bone - bone_length_change
                    og_right_side = og_pos + part_data.size/2
                    new_right_side = og_right_side + bone_length_change

                    part_data.size = new_right_side
                    part_data.pos_on_bone = part_data.size/2

                    # if bone shrunk enough to leave no room for part, remove it
                    if part_data.size <= 0:
                        remove_part(dna, part_data)

            else:
                new_distance_from_joint = new_length - part_data.pos_on_bone
                if new_distance_from_joint < part_data.size/2:

                    og_distance_from_joint = og_length - part_data.pos_on_bone
                    og_left_side = og_distance_from_joint + part_data.size/2 # distance between left side of part and moved joint
                    new_left_side = og_left_side + bone_length_change

                    part_data.size = new_left_side

                    distance = new_length - new_left_side # distance between left side of part and first joint
                    part_data.pos_on_bone = distance + part_data.size/2

                    # if bone shrunk enough to leave no room for part, remove it
                    if part_data.size <= 0:
                        remove_part(dna, part_data)

                    




def add_joint(dna: DNA):
    # spawn near random joint
    og_joint_index = nr.randint(len(dna.structure.vertices))
    og_joint = dna.structure.vertices[og_joint_index]

    random_dir = get_random_direction()
    new_joint = og_joint + (np.array(random_dir) * NEW_JOINT_DIST)

    dna.structure.add_vertex(og_joint_index, new_joint)


def add_bone(dna: DNA):
    possible_bones = np.zeros((0, 2))

    dna.structure.check_edges_sorted()

    # possible speed up
    for i in range(len(dna.structure.vertices)):
        for j in range(i+1, len(dna.structure.vertices)):
            bone = np.array((i,j))

            if not np.any(np.all(dna.structure.edges == bone, axis=1)):
                possible_bones = np.append(possible_bones, [bone], axis=0)

    if len(possible_bones) > 0:
        new_bone = possible_bones[nr.randint(len(possible_bones))]
        new_bone = np.asarray(new_bone, dtype=int)
        dna.structure.add_edge(new_bone)


def remove_bone(dna: DNA):
    remaining_bone_indices = np.arange(len(dna.structure.edges))
        
    removed_bone = False
    while len(remaining_bone_indices) > 0:
        indices_index = nr.randint(len(remaining_bone_indices))
        bone_index = remaining_bone_indices[indices_index]

        remaining_bone_indices = np.delete(remaining_bone_indices, [indices_index])

        removed_bone = dna.structure.try_remove_edge(bone_index)
        if removed_bone:
            break


    if removed_bone:
        # delete parts on removed bone and adjust bone indices
        for part_data in all_part_data(dna):
            if part_data.bone_index == bone_index:
                remove_part(dna, part_data)
            elif part_data.bone_index > bone_index:
                part_data.bone_index -= 1


def move_part(dna: DNA, part_data: CreaturePartData):

    min_pos_on_bone = part_data.size/2

    bone_length = dna.get_bone_vector(part_data.bone_index).magnitude()
    max_pos_on_bone = bone_length - part_data.size/2

    original_pos = part_data.pos_on_bone

    desired_move_amount = nr.randn() * AVG_PART_MOVE_AMOUNT
    part_data.pos_on_bone += desired_move_amount
    part_data.pos_on_bone = np.clip(part_data.pos_on_bone, min_pos_on_bone, max_pos_on_bone)

    if overlapping_parts(dna, part_data):
        part_data.pos_on_bone = original_pos

    if not valid_part_pos(dna, part_data.bone_index, part_data.pos_on_bone, part_data.size):
        raise Exception("Try to move part to invalid pos.")


def resize_part(dna: DNA, part_data: CreaturePartData):

    bone_length = dna.get_bone_vector(part_data.bone_index).magnitude()

    # distances between center of part and bone positions
    distance1 = bone_length - part_data.pos_on_bone
    distance2 = part_data.pos_on_bone

    shorter_distance = np.min((distance1, distance2))

    max_size = shorter_distance * 2

    original_size = part_data.size

    desired_resize_amount = nr.randn() * AVG_PART_RESIZE_AMOUNT
    part_data.size += desired_resize_amount
    part_data.size = np.clip(part_data.size, MIN_PART_SIZE, max_size)

    if overlapping_parts(dna, part_data):
        part_data.size = original_size


def add_part(dna: DNA):
    part_type = nr.choice(PartType)

    max_attempts = 10
    attempt = 0

    overlapping = True
    while overlapping:

        attempt += 1
        if attempt >= max_attempts:
            return

        bone_index = nr.randint(len(dna.structure.edges))
        bone_side = nr.choice(BoneSide)

        min_pos_on_bone = MIN_PART_SIZE/2

        bone_length = dna.get_bone_vector(bone_index).magnitude()
        max_pos_on_bone = bone_length - MIN_PART_SIZE/2

        pos_on_bone = nr.uniform(min_pos_on_bone, max_pos_on_bone)

        part_data = CreaturePartData(part_type, bone_index, bone_side, pos_on_bone, MIN_PART_SIZE)

        overlapping = overlapping_parts(dna, part_data)

    if part_type == PartType.BOOSTER:
        dna.booster_data.append(part_data)
    if part_type == PartType.MOUTH:
        dna.mouth_data.append(part_data)

        
def remove_rand_part(dna: DNA):

    booster_data = [(PartType.BOOSTER, i) for i in range(len(dna.booster_data))]
    mouth_data = [(PartType.MOUTH, i) for i in range(len(dna.mouth_data))]

    all_data = booster_data + mouth_data

    part_type, index = random.choice(all_data)

    if part_type == PartType.BOOSTER:
        dna.booster_data.pop(index)
    elif part_type == PartType.MOUTH:
        dna.mouth_data.pop(index)


def remove_part(dna: DNA, part_data: CreaturePartData):
    if part_data.type == PartType.BOOSTER:
        dna.booster_data.pop(dna.booster_data.index(part_data))
    elif part_data.type == PartType.MOUTH:
        dna.mouth_data.pop(dna.mouth_data.index(part_data))


def overlapping_parts(dna: DNA, part_data: CreaturePartData):
    for other_part_data in all_part_data(dna):
        if other_part_data == part_data:
            continue
        
        on_same_bone = part_data.bone_index == other_part_data.bone_index
        if on_same_bone:
            distance = np.abs(part_data.pos_on_bone - other_part_data.pos_on_bone)
            min_distance = (part_data.size/2) + (other_part_data.size/2) + PART_PADDING

            if distance < min_distance:
                return True
    return False


def all_part_data(dna: DNA) -> list[CreaturePartData]:
    return dna.booster_data + dna.mouth_data