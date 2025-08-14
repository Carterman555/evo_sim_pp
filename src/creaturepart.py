import pygame
from enums import BoneSide
from helper import valid_part_pos

class CreaturePart(pygame.sprite.Sprite):
    def __init__(self, creature, bone_index, side, pos_on_bone, size, *groups):

        if not valid_part_pos(creature, bone_index, pos_on_bone, size):
            raise Exception(f"Error: Trying to create part {type(self)} which is not valid pos. Check if valid before creating.")

        super().__init__(*groups)

        self.creature = creature

        self.bone_index = bone_index
        self.side = side
        self.pos_on_bone = pos_on_bone
        self.size = size

        self.direction = creature.dna.get_bone_vector(self.bone_index).normalize()
        if self.side == BoneSide.BOTTOM:
            self.direction.rotate_ip(270)
        elif self.side == BoneSide.TOP:
            self.direction.rotate_ip(90)

        height = 5
        self.image = pygame.Surface((self.size, height), pygame.SRCALPHA)

        self.bone_positions = self.creature.dna.get_bone_pos(self.bone_index)
        self.bone_vector = self.creature.dna.get_bone_vector(self.bone_index).normalize()

        center = self.bone_positions[0] - (self.bone_vector * pos_on_bone)
        self.rect = self.image.get_rect(center=center + creature.offset)
    