import pygame
import numpy as np

from graph import Graph
from helper import np_to_v2
from creaturepart import CreaturePartData

class DNA:
    def __init__(self, joints, bones, booster_data, mouth_data):
        self.structure : Graph = Graph(joints, bones)
        self.booster_data : list[CreaturePartData] = list(booster_data)
        self.mouth_data : list[CreaturePartData] = list(mouth_data)

    def copy(self):
        copy = DNA(self.structure.vertices, self.structure.edges, self.booster_data.copy(), self.mouth_data.copy())
        return copy

    def get_booster_rects(self):
        return map(lambda booster: booster.rect, self.booster_data)
    
    def get_bone_vector(self, bone_index) -> pygame.Vector2:
        pos1, pos2 = self.structure.get_edge_pos(bone_index)
        return np_to_v2(pos1 - pos2)