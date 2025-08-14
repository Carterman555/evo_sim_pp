import pygame
import numpy as np
from helper import np_to_v2

# I might just want to combine this with creature class, but idk
class DNA:
    def __init__(self):
        joints = [[0, 0], [300, 0], [50, 50], [0, 50]]
        self.joints = np.asarray(joints)
        
        bones = [(0,1), (1,2), (2,3), (3,0)]
        self.bones = sorted({tuple(sorted(b)) for b in bones}) # normalize edges to sorted tuples and dedupe
        
        self.boosters = []
        self.mouths = []
    
    def get_joints(self):
        return self.structure.keys()
    
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
    
    def get_bone_vector(self, bone_index):
        pos1, pos2 = self.get_bone_pos(bone_index)
        return np_to_v2(pos1) - np_to_v2(pos2)

    def get_booster_rects(self):
        return map(lambda booster: booster.rect, self.boosters)