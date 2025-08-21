from numpy import random

from creature import Creature
from creaturepart import CreaturePartData
from dna import DNA
from graph import Graph
from mutate_dna import try_add_part

from enums import *
from constants import *

class CreatureSpawner:

    def __init__(self, world_bounds):
        self.world_bounds = world_bounds


    def update(self):
        if len(Creature._instances) < MIN_CREATURE_AMOUNT:
            padding = 100

            x = random.randint(self.world_bounds.left + padding, self.world_bounds.right - padding)
            y = random.randint(self.world_bounds.top + padding, self.world_bounds.bottom - padding)

            dna = self.starting_dna()
            creature = Creature(self.world_bounds, dna, (x, y))


    def starting_dna(self) -> DNA:
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




