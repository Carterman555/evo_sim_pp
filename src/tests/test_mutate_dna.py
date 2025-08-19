import unittest
from dna import DNA
from creaturepart import CreaturePartData
from mutate_dna import *
from enums import *

class TestMutateDNA(unittest.TestCase):

    def test_move_part1(self):
        joints = [[0, 0], [66, 63], [36, 53]]
        bones = [[1, 2], [0, 2]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=24, size=16)]

        dna = DNA(joints, bones, boosters, [])

        move_part(dna, boosters[0], 11.530225266398158)

    def test_move_part2(self):
        joints = [[0.0, 1.0], [11.0, 0.0]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.TOP, pos_on_bone=2, size=5)]

        dna = DNA(joints, bones, boosters, [])

        move_part(dna, boosters[0], 9.155176348803938)

    def test_move_joint1(self):
        joints = [[0.0, 0.0], [80.0, 6.0], [55.0, 43.0], [0.0, 52.0], [15.0, 49.0]]
        bones = [[0, 1], [1, 2], [2, 3], [0, 3], [3, 4]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=20, size=20)]

        dna = DNA(joints, bones, boosters, [])

        move_joint(dna, 0, pygame.Vector2(9,4))

    def test_move_joint2(self):
        joints = [[15.0, 2.0], [0.0, 0.0]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=3, size=5)]

        dna = DNA(joints, bones, boosters, [])

        move_joint(dna, 1, pygame.Vector2(7,-1))