from numpy import random

from creature import Creature
from creaturepart import CreaturePartData
from dna import DNA
from graph import Graph
from mutate_dna import try_add_part

from enums import *
from constants import *

class CreatureSpawner:

    def __init__(self):
        while len(Creature._instances) < 1:
            dna = self.box_starting_dna()
            creature = Creature(dna, (WORLD_CENTER_X, WORLD_CENTER_Y))


    def update(self):
        # if len(Creature._instances) < MIN_CREATURE_AMOUNT:
        #     padding = 100

        #     x = random.randint(WORLD_BOUNDS.left + padding, WORLD_BOUNDS.right - padding)
        #     y = random.randint(WORLD_BOUNDS.top + padding, WORLD_BOUNDS.bottom - padding)

        #     dna = self.starting_dna()
        #     creature = Creature(dna, (x, y))

        pass



    def rand_starting_dna(self) -> DNA:
        dna: DNA = DNA([], [], [], [])
        
        njoints = random.randint(2,5)
        joints = [(random.randint(0,100), random.randint(0,100)) for i in range(njoints)]

        bones = [[i,i+1] for i in range(njoints)]
        bones[-1][1] = 0

        dna.structure = Graph(joints, bones)

        try_add_part(dna, PartType.BOOSTER)
        try_add_part(dna, PartType.MOUTH)

        for i in range(random.randint(0,3)):
            try_add_part(dna, random.choice(list(PartType)))
            
        dna.structure.normalize_vertices()
        return dna
    

    def box_starting_dna(self) -> DNA:
        joints = [(0,0),(80,0),(80,80),(0,80)]

        bones = [[i,i+1] for i in range(len(joints))]
        bones[-1][1] = 0

        parts_data = [
            CreaturePartData(PartType.BOOSTER, bone_index=0, side=BoneSide.TOP, pos_on_bone=40, size=40),
            CreaturePartData(PartType.BOOSTER, bone_index=1, side=BoneSide.TOP, pos_on_bone=40, size=40),
            CreaturePartData(PartType.BOOSTER, bone_index=2, side=BoneSide.TOP, pos_on_bone=40, size=40),
            CreaturePartData(PartType.BOOSTER, bone_index=3, side=BoneSide.BOTTOM, pos_on_bone=40, size=40),

            CreaturePartData(PartType.MOUTH, bone_index=0, side=BoneSide.BOTTOM, pos_on_bone=40, size=60),
            CreaturePartData(PartType.MOUTH, bone_index=1, side=BoneSide.BOTTOM, pos_on_bone=40, size=60),
            CreaturePartData(PartType.MOUTH, bone_index=2, side=BoneSide.BOTTOM, pos_on_bone=40, size=60),
            CreaturePartData(PartType.MOUTH, bone_index=3, side=BoneSide.TOP, pos_on_bone=40, size=60)
        ]

        return DNA(joints, bones, parts_data)





