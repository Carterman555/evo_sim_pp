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

    for i in range(len(mutated_dna.structure.vertices)):
        if MOVE_JOINT_PROB * TEST_PROB_MULT > nr.rand():
            move_joint(mutated_dna, i)


    if ADD_JOINT_PROB * TEST_PROB_MULT > nr.rand():
        add_joint(mutated_dna)
        print('add joint')


    if ADD_BONE_PROB * TEST_PROB_MULT > nr.rand():
        add_bone(mutated_dna)


    if REMOVE_BONE_PROB * TEST_PROB_MULT > nr.rand():
        remove_bone(mutated_dna)

    
    parts_data = all_part_data(mutated_dna)
    for part_data in parts_data:
        if MOVE_PART_PROB * TEST_PROB_MULT > nr.rand():
            move_part(mutated_dna, part_data)
        if RESIZE_PART_PROB * TEST_PROB_MULT > nr.rand():
            resize_part(mutated_dna, part_data)


    if ADD_PART_PROB * TEST_PROB_MULT > nr.rand():
        add_part(mutated_dna)


    parts_amount = len(all_part_data(mutated_dna))
    if parts_amount > 0 and REMOVE_PART_PROB * TEST_PROB_MULT > nr.rand():
        remove_part(mutated_dna)


    mutated_dna.structure.normalize_vertices()
    return mutated_dna


def move_joint(dna: DNA, index: int):
    move_vector = pygame.Vector2(nr.randn()*AVG_JOINT_MOVE_AMOUNT, nr.randn()*AVG_JOINT_MOVE_AMOUNT)
    dna.structure.vertices[index] = np.array(dna.structure.vertices[index] + move_vector)


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

        
def remove_part(dna: DNA):

    booster_data = [(PartType.BOOSTER, i) for i in range(len(dna.booster_data))]
    mouth_data = [(PartType.MOUTH, i) for i in range(len(dna.mouth_data))]

    all_data = booster_data + mouth_data

    part_type, index = random.choice(all_data)

    if part_type == PartType.BOOSTER:
        dna.booster_data.pop(index)
    elif part_type == PartType.MOUTH:
        dna.mouth_data.pop(index)


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
    return np.append(dna.booster_data, [dna.mouth_data])

# def add_joint_on_bone(dna):
#     # choose a random bone
#     bone_index = random.randint(0, len(dna.bones))

#     # get a random point on that bone, and place a joint there
#     bone_vector = dna.get_bone_vector(bone_index)
#     rand = (random.rand() * 0.8) + 0.1 # random number between 0.1 and 0.9
#     pos_on_bone = rand * bone_vector.magnitude()

#     bone_positions = dna.get_bone_pos(bone_index)

#     new_joint_pos = bone_positions[0] - np.array(bone_vector.normalize()*pos_on_bone)
#     dna.joints = np.append(dna.joints, [new_joint_pos], axis=0)

#     # there are 2 joints connected by the choosen bone
#     # create new bones connecting each of these 2 joints to the new joint
#     new_bone1 = (dna.bones[bone_index][0], len(dna.joints)-1)
#     new_bone2 = (dna.bones[bone_index][1], len(dna.joints)-1)
#     dna.bones = np.append(dna.bones, [new_bone1, new_bone2], axis=0)

#     # delete the choosen bone
#     dna.bones = np.delete(dna.bones, [bone_index], axis=0)