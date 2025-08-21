import pygame, math
from numpy.random import randint

from creature import Creature
from creaturepart import CreaturePartData
from dna import DNA
from graph import Graph
from mutate_dna import add_part

from enums import *
from constants import *

class CreatureSpawner:

    def __init__(self, updatable, world_bounds):
        self.updatable = updatable
        self.world_bounds = world_bounds

    def update(self):
        if len(Creature._instances) < MIN_CREATURE_AMOUNT:
            padding = 100

            x = randint(self.world_bounds.left + padding, self.world_bounds.right - padding)
            y = randint(self.world_bounds.top + padding, self.world_bounds.bottom - padding)

            dna = self.starting_dna()
            creature = Creature(self.updatable, self.world_bounds, dna, (x, y))


    def starting_dna(self) -> DNA:
        dna: DNA = DNA([], [], [], [])
        
        njoints = randint(2,5)
        joints = [(randint(0,100), randint(0,100)) for i in range(njoints)]

        bones = [[i,i+1] for i in range(njoints)]
        bones[-1][1] = 0

        dna.structure = Graph(joints, bones)

        nparts = randint(0,5)
        for i in range(nparts):
            add_part(dna)
            
        dna.structure.normalize_vertices()
        return dna




