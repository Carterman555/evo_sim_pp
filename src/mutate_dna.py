import pygame
import numpy as np
from numpy import random

from dna import DNA
from constants import *
from helper import *

def mutate_dna(dna: DNA) -> DNA:

    mutated_dna = dna.get_copy()

    # for i in range(len(mutated_dna.structure.vertices)):
    #     if MOVE_JOINT_PROB > random.rand():
    #         move_vector = pygame.Vector2(random.randn()*AVG_JOINT_MOVE_AMOUNT, random.randn()*AVG_JOINT_MOVE_AMOUNT)
    #         mutated_dna.structure.vertices[i] = np.array(mutated_dna.structure.vertices[i] + move_vector)


    # if ADD_JOINT_PROB > random.rand():
    #     # spawn near random joint
    #     og_joint_index = random.randint(len(mutated_dna.structure.vertices))
    #     og_joint = mutated_dna.structure.vertices[og_joint_index]

    #     random_dir = get_random_direction()
    #     new_joint = og_joint + (np.array(random_dir) * NEW_JOINT_DIST)

    #     mutated_dna.structure.add_vertex(og_joint_index, new_joint)


    # if ADD_BONE_PROB > random.rand():
    #     possible_bones = np.zeros((0, 2))

    #     mutated_dna.structure.check_edges_sorted()

    #     # possible speed up
    #     for i in range(len(mutated_dna.structure.vertices)):
    #         for j in range(i+1, len(mutated_dna.structure.vertices)):
    #             bone = np.array((i,j))

    #             if not np.any(np.all(mutated_dna.structure.edges == bone, axis=1)):
    #                 possible_bones = np.append(possible_bones, [bone], axis=0)

    #     if len(possible_bones) > 0:
    #         new_bone = possible_bones[random.randint(len(possible_bones))]
    #         new_bone = np.asarray(new_bone, dtype=int)
    #         mutated_dna.structure.add_edge(new_bone)


    # # if REMOVE_BONE_PROB > random.rand():
    for x in range(2):

        remaining_bone_indices = np.arange(len(mutated_dna.structure.edges))
        
        removed_bone = False
        while len(remaining_bone_indices) > 0:
            indices_index = random.randint(len(remaining_bone_indices))
            bone_index = remaining_bone_indices[indices_index]

            remaining_bone_indices = np.delete(remaining_bone_indices, [indices_index])

            removed_bone = mutated_dna.structure.try_remove_edge(bone_index)
            if removed_bone:
                break


    mutated_dna.structure.normalize_vertices()
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