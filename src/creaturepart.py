import pygame
from enums import BoneSide
from helper import valid_part_pos

class CreaturePartData:
    def __init__(self, bone_index, side, pos_on_bone, size):
        self.bone_index = bone_index
        self.side = side
        self.pos_on_bone = pos_on_bone
        self.size = size

class CreaturePart(pygame.sprite.Sprite):
    def __init__(self, creature, data, *groups):

        if not valid_part_pos(creature, data.bone_index, data.pos_on_bone, data.size):
            raise Exception(f"Error: Trying to create part {type(self)} which is not valid pos. Check if valid before creating.")

        super().__init__(*groups)

        self.creature = creature

        self.data = data

        self.direction = creature.dna.get_bone_vector(data.bone_index).normalize()
        if data.side == BoneSide.BOTTOM:
            self.direction.rotate_ip(270)
        elif data.side == BoneSide.TOP:
            self.direction.rotate_ip(90)

        height = 5
        self.image = pygame.Surface((data.size, height), pygame.SRCALPHA)

        self.bone_positions = self.creature.dna.get_bone_pos(data.bone_index)
        self.bone_vector = self.creature.dna.get_bone_vector(data.bone_index).normalize()

        center = self.bone_positions[0] - (self.bone_vector * data.pos_on_bone)
        self.rect = self.image.get_rect(center=center + creature.offset)
    