import pygame
import numpy as np

class DNA:
    def __init__(self):
        joints = [[0, 0], [300, 0], [50, 50], [0, 50]]
        self.joints = np.asarray(joints)
        
        bones = [(0,1), (1,2), (2,3), (3,0)]
        self.bones = sorted({tuple(sorted(b)) for b in bones}) # normalize edges to sorted tuples and dedupe
        
        boosters = [3,2,0,1] # [bone index, position on bone]
        self.boosters = np.asarray(boosters)
    
    def get_joints(self):
        return self.structure.keys()
    
    def get_bone_positions(self):
        bone_positions = [(self.joints[pos1].copy(), self.joints[pos2].copy()) for (pos1, pos2) in self.bones]
        return bone_positions
    
    def get_bone_pos(self, bone):
        return (self.joints[bone[0]].copy(), self.joints[bone[1]].copy())
    
    def get_booster_positions(self):
        return map(self.get_bone_center, self.boosters)
    
    def get_bone_center(self, bone_index):
        pos1, pos2 = self.get_bone_pos(self.bones[int(bone_index)])
        v1, v2 = pygame.Vector2(tuple(pos1)), pygame.Vector2(tuple(pos2))

        center = (v1 + v2) / 2
        return center
    
    def get_bone_vector(self, bone_index):
        pos1, pos2 = self.get_bone_pos(self.bones[int(bone_index)])
        return pygame.Vector2(tuple(pos1)) - pygame.Vector2(tuple(pos2))