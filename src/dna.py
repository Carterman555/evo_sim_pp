import pygame
import numpy as np
from helper import np_to_v2

# I might just want to combine this with creature class, but idk
class DNA:
    def __init__(self, joints, bones, booster_data, mouth_data):
        self.joints = np.array(joints)
        self.bones = np.array([sorted(b) for b in bones]) # bones should always remain sorted
        self.booster_data = booster_data
        self.mouth_data = mouth_data

    def check_bones_sorted(self):
        if not np.all(self.bones[:, 0] <= self.bones[:, 1]):
            raise Exception(f"Error: Found unsorted bones in {self.bones}")

    # make the min joint positions 0, adjust all other joint positions to keep
    # same relative positions
    def normalize_joint_positions(self):
        xmin = self.joints[:, 0].min()
        self.joints[:, 0] = self.joints[:, 0] - xmin

        ymin = self.joints[:, 1].min()
        self.joints[:, 1] = self.joints[:, 1] - ymin

    def get_copy(self):
        copy = DNA(self.joints.copy(), self.bones.copy(), self.booster_data.copy(), self.mouth_data.copy())
        return copy

    def get_bone_positions(self):
        bone_positions = [(self.joints[pos1].copy(), self.joints[pos2].copy()) for (pos1, pos2) in self.bones]
        return bone_positions
    
    def get_bone_pos(self, bone_index) -> np.array:
        bone = self.bones[int(bone_index)]
        return np.array((self.joints[bone[0]].copy(), self.joints[bone[1]].copy()))
    
    def get_bone_center(self, bone_index):
        pos1, pos2 = self.get_bone_pos((bone_index))
        center = (np_to_v2(pos1) + np_to_v2(pos2)) / 2
        return center
    
    def get_bone_vector(self, bone_index) -> pygame.Vector2:
        pos1, pos2 = self.get_bone_pos(bone_index)
        return np_to_v2(pos1) - np_to_v2(pos2)

    def get_booster_rects(self):
        return map(lambda booster: booster.rect, self.booster_data)