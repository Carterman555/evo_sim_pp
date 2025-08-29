import pygame
import numpy as np

from graph import Graph
from helper import np_to_v2
from creaturepart import CreaturePartData
from enums import PartType

class DNA:
    def __init__(self, joints, bones, parts_data):
        self.structure : Graph = Graph(joints, bones)
        self.parts_data : list[CreaturePartData] = list(parts_data)

    def copy(self):
        copy = DNA(self.structure.vertices, self.structure.edges, self.parts_data.copy())
        return copy

    def get_booster_rects(self):
        return [part_data.rect for part_data in self.parts_data if part_data.type == PartType.BOOSTER]
    
    def get_bone_vector(self, bone_index) -> pygame.Vector2:
        pos1, pos2 = self.structure.get_edge_pos(bone_index)
        return np_to_v2(pos2 - pos1)