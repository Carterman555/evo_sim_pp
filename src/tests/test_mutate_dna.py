import unittest
from dna import DNA
from creaturepart import CreaturePartData
from mutate_dna import *
from enums import *

class TestMutateDNA(unittest.TestCase):

    def test_move_joint1(self):
        joints = [[0,0],[40,0]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=20, size=20)]

        dna = DNA(joints, bones, boosters, [])

        move_joint(dna, 0, pygame.Vector2(4,0))

        self.assertEqual(dna.booster_data[0].pos_on_bone, 16)
        self.assertEqual(dna.booster_data[0].size, 20)

    def test_move_joint2(self):
        joints = [[0,0],[40,0]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=20, size=20)]

        dna = DNA(joints, bones, boosters, [])

        move_joint(dna, 1, pygame.Vector2(-4,0))

        self.assertEqual(dna.booster_data[0].pos_on_bone, 20)
        self.assertEqual(dna.booster_data[0].size, 20)

    def test_move_joint3(self):
        joints = [[0,0],[40,0]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=20, size=20)]

        dna = DNA(joints, bones, boosters, [])

        move_joint(dna, 0, pygame.Vector2(15,0))

        self.assertEqual(dna.booster_data[0].pos_on_bone, 11)
        self.assertEqual(dna.booster_data[0].size, 9)

    def test_move_joint4(self):
        joints = [[0,0],[40,0]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=20, size=20)]

        dna = DNA(joints, bones, boosters, [])

        move_joint(dna, 1, pygame.Vector2(-15,0))

        self.assertEqual(dna.booster_data[0].pos_on_bone, 14)
        self.assertEqual(dna.booster_data[0].size, 9)

    def test_move_joint5(self):
        joints = [[0,0],[0,40]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=20, size=20)]

        dna = DNA(joints, bones, boosters, [])

        move_joint(dna, 0, pygame.Vector2(0,9))

        self.assertEqual(dna.booster_data[0].pos_on_bone, 14)
        self.assertEqual(dna.booster_data[0].size, 15)

    def test_move_joint6(self):
        joints = [[0,0],[40,0]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=20, size=20)]

        dna = DNA(joints, bones, boosters, [])

        move_joint(dna, 1, pygame.Vector2(-10,0))

        self.assertEqual(dna.booster_data[0].pos_on_bone, 17)
        self.assertEqual(dna.booster_data[0].size, 14)

    def test_move_joint7(self):
        joints = [[0,0],[40,0]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=20, size=20)]

        dna = DNA(joints, bones, boosters, [])

        move_joint(dna, 0, pygame.Vector2(20,0))

        self.assertEqual(len(dna.booster_data), 0)


    def test_move_part1(self):
        joints = [[0,0],[60,0]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=30, size=20)]

        dna = DNA(joints, bones, boosters, [])

        move_part(dna, dna.booster_data[0], 10)

        self.assertEqual(dna.booster_data[0].pos_on_bone, 40)
        self.assertEqual(dna.booster_data[0].size, 20)

    def test_move_part2(self):
        joints = [[0,0],[60,0]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=30, size=20)]

        dna = DNA(joints, bones, boosters, [])

        move_part(dna, dna.booster_data[0], 30)

        self.assertEqual(dna.booster_data[0].pos_on_bone, 44)
        self.assertEqual(dna.booster_data[0].size, 20)

    def test_move_part3(self):
        joints = [[0,0],[60,0]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=30, size=20)]

        dna = DNA(joints, bones, boosters, [])

        move_part(dna, dna.booster_data[0], -30)

        self.assertEqual(dna.booster_data[0].pos_on_bone, 16)
        self.assertEqual(dna.booster_data[0].size, 20)

    def test_move_part_overlap(self):
        joints = [[0,0],[60,0]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=20, size=10),
                    CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=40, size=10)]

        dna = DNA(joints, bones, boosters, [])

        move_part(dna, dna.booster_data[0], 5)

        self.assertEqual(dna.booster_data[0].pos_on_bone, 20)
        self.assertEqual(dna.booster_data[0].size, 10)


    def test_resize_part1(self):
        joints = [[0,0],[60,0]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=30, size=10)]

        dna = DNA(joints, bones, boosters, [])

        resize_part(dna, dna.booster_data[0], -8)

        self.assertEqual(len(dna.booster_data), 0)

    def test_resize_part2(self):
        joints = [[0,0],[60,0]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=30, size=10)]

        dna = DNA(joints, bones, boosters, [])

        resize_part(dna, dna.booster_data[0], 10)

        self.assertEqual(dna.booster_data[0].pos_on_bone, 30)
        self.assertEqual(dna.booster_data[0].size, 20)

    def test_resize_part3(self):
        joints = [[0,0],[40,0]]
        bones = [[0, 1]]
        boosters = [CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=20, size=10)]

        dna = DNA(joints, bones, boosters, [])

        resize_part(dna, dna.booster_data[0], 50)

        self.assertEqual(dna.booster_data[0].pos_on_bone, 20)
        self.assertEqual(dna.booster_data[0].size, 28)