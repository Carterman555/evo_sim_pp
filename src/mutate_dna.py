import pygame
import numpy as np
from numpy import random

from dna import DNA
from constants import *
from helper import *

def mutate_dna(dna: DNA) -> DNA:

    mutated_dna = dna.get_copy()

    for i in range(len(mutated_dna.joints)):
        if MOVE_JOINT_PROB > random.rand():
            move_vector = pygame.Vector2(random.randn()*AVG_JOINT_MOVE_AMOUNT, random.randn()*AVG_JOINT_MOVE_AMOUNT)
            if random.rand() > 0.5:
                move_vector.x = -move_vector.x
            if random.rand() > 0.5:
                move_vector.y = -move_vector.y

            mutated_dna.joints[i] = np.array(mutated_dna.joints[i] + move_vector)


    if ADD_JOINT_PROB > random.rand():
        # spawn near random joint
        og_joint_index = random.randint(0, len(mutated_dna.joints))
        og_joint = mutated_dna.joints[og_joint_index]

        random_dir = get_random_direction()
        new_joint = og_joint + (np.array(random_dir) * NEW_JOINT_DIST)

        mutated_dna.joints = np.append(mutated_dna.joints, [new_joint], axis=0)

        # add bone to connect joints
        new_bone = (og_joint_index, len(mutated_dna.joints)-1)
        mutated_dna.bones = np.append(mutated_dna.bones, [new_bone], axis=0)


    if ADD_BONE_PROB > random.rand():
        possible_bones = np.zeros((0, 2))

        mutated_dna.check_bones_sorted()

        # speed up
        for i in range(len(mutated_dna.joints)):
            for j in range(i+1, len(mutated_dna.joints)):
                bone = np.array((i,j))

                if not np.any(np.all(mutated_dna.bones == bone, axis=1)):
                    possible_bones = np.append(possible_bones, [bone], axis=0)

        if len(possible_bones) > 0:
            new_bone = possible_bones[random.randint(len(possible_bones))]
            new_bone = np.asarray(new_bone, dtype=int)
            mutated_dna.bones = np.append(mutated_dna.bones, [new_bone], axis=0)


    # if REMOVE_BONE_PROB > random.rand():
    for x in range(2):
        count = 0

        remaining_bone_indices = np.arange(len(mutated_dna.bones))

        # speed up: I'm having it remove bones then check if valid. There might be faster algorithm to check all valid
        # bones to remove.
        # while created disconnected structure
        while count == 0:
            count+=1

            bones = mutated_dna.bones.copy()
            joints = mutated_dna.joints.copy()

            bone_index = random.choice(remaining_bone_indices)
            remaining_bone_indices = np.delete(remaining_bone_indices, bone_index)

            bone_removing = bones[bone_index].copy()

            # remove bone
            bones = np.delete(bones, [bone_index], axis=0)

            # if either joint connected to choosen bone has no other connections, remove it
            if not np.any(bones == bone_removing[0]):
                joints = np.delete(joints, [bone_removing[0]], axis=0)

            if not np.any(bones == bone_removing[1]):
                joints = np.delete(joints, [bone_removing[1]], axis=0)

        mutated_dna.bones = bones
        mutated_dna.joints = joints

    print()


    mutated_dna.normalize_joint_positions()
    return mutated_dna




# ADD JOINT TO POS ON EXISTING BONE
# # choose a random bone
# bone_index = random.randint(0, len(mutated_dna.bones))

# # get a random point on that bone, and place a joint there
# bone_vector = mutated_dna.get_bone_vector(bone_index)
# rand = (random.rand() * 0.8) + 0.1 # random number between 0.1 and 0.9
# pos_on_bone = rand * bone_vector.magnitude()

# bone_positions = mutated_dna.get_bone_pos(bone_index)

# new_joint_pos = bone_positions[0] - np.array(bone_vector.normalize()*pos_on_bone)
# mutated_dna.joints = np.append(mutated_dna.joints, [new_joint_pos], axis=0)

# # there are 2 joints connected by the choosen bone
# # create new bones connecting each of these 2 joints to the new joint
# new_bone1 = (mutated_dna.bones[bone_index][0], len(mutated_dna.joints)-1)
# new_bone2 = (mutated_dna.bones[bone_index][1], len(mutated_dna.joints)-1)
# mutated_dna.bones = np.append(mutated_dna.bones, [new_bone1, new_bone2], axis=0)

# # delete the choosen bone
# mutated_dna.bones = np.delete(mutated_dna.bones, [bone_index], axis=0)