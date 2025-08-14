import pygame, math
from enums import BoneSide
from helper import *

class Booster(pygame.sprite.Sprite):
    def __init__(self, creature, bone_index, side, pos_on_bone, size, *groups):

        if not Booster.is_valid(self.creature, self.bone_index, self.pos_on_bone, self.size):
            raise Exception("Error: Trying to creating booster which is not valid. Check if valid before creating.")

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

    def draw(self, surface):
        self.image.fill('cyan')

        angle = pygame.Vector2(1,0).angle_to(self.bone_vector)
        
        rotated_image, rotated_rect = rotate(self.image, angle, self.rect.center)
        surface.blit(rotated_image, rotated_rect)

    @staticmethod
    def is_valid(creature, bone_index, pos_on_bone, size):
        bone_positions = creature.dna.get_bone_pos(bone_index)
        bone_vector = creature.dna.get_bone_vector(bone_index).normalize()

        center = bone_positions[0] - (bone_vector * pos_on_bone)

        booster_pos1 = center - ((size/2) * bone_vector)
        booster_pos2 = center + ((size/2) * bone_vector)
        
        # Get min/max x and y for booster positions
        booster_min_x = min(booster_pos1[0], booster_pos2[0])
        booster_max_x = max(booster_pos1[0], booster_pos2[0])
        booster_min_y = min(booster_pos1[1], booster_pos2[1])
        booster_max_y = max(booster_pos1[1], booster_pos2[1])

        # Get min/max x and y for bone positions
        bone_min_x = min(bone_positions[0][0], bone_positions[1][0])
        bone_max_x = max(bone_positions[0][0], bone_positions[1][0])
        bone_min_y = min(bone_positions[0][1], bone_positions[1][1])
        bone_max_y = max(bone_positions[0][1], bone_positions[1][1])

        # Check if booster is within bone bounds
        return (booster_min_x >= bone_min_x and booster_max_x <= bone_max_x and
            booster_min_y >= bone_min_y and booster_max_y <= bone_max_y)



        