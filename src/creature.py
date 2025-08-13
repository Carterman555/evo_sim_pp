import pygame
from DNA import DNA
import numpy as np
from helpers import rotate_around

class Creature():
    def __init__(self, x, y):

        self.DNA = DNA()

        joint_x_positions = self.DNA.joints[:, 0]
        joint_y_positions = self.DNA.joints[:, 1]
        self.width = joint_x_positions.max() - joint_x_positions.min()
        self.height = joint_y_positions.max() - joint_y_positions.min()

        padding = 0
        self.offset = pygame.Vector2(padding/2, padding/2)

        self.surface = pygame.Surface((self.width + padding, self.height + padding),pygame.SRCALPHA)

        self.pos = pygame.Vector2(x,y)
        self.angle = 0

        self.vel = pygame.Vector2(0,0)
        self.angvel = 20

        sum_pos = pygame.Vector2(0,0)
        for joint in self.DNA.joints:
            sum_pos += joint
        self.center_of_mass = sum_pos / len(self.DNA.joints)
        self.center_of_mass += self.offset
        self.draw_shapes()

    def update(self, dt):
        self.pos += self.vel * dt
        self.angle += self.angvel * dt

    def draw(self, screen):

        # offset is center of mass relative to center instead of topleft
        offset = pygame.Vector2(self.width/2, self.height/2) - self.center_of_mass 
        rotated_surf, rect = rotate_around(self.surface, self.angle, self.pos, offset)
        screen.blit(rotated_surf, rect)

    def draw_shapes(self):
        self.surface.fill((0,0,0,20))

        # bones
        for bone in self.DNA.get_bone_positions():
            start_pos = bone[0]
            end_pos = bone[1]
            pygame.draw.line(self.surface, 'white', self.offset + start_pos, self.offset + end_pos, 3)
            
        # joints
        for joint in self.DNA.joints:
            joint_pos = tuple(joint)
            pygame.draw.circle(self.surface, 'red', self.offset + joint_pos, radius=5)

        # boosters
        for bone_index in self.DNA.boosters:
            pos1, pos2 = self.DNA.get_bone_pos(self.DNA.bones[int(bone_index)])
            v1, v2 = pygame.Vector2(tuple(pos1)), pygame.Vector2(tuple(pos2))

            center = (v1 + v2) / 2

            pygame.draw.circle(self.surface, 'blue', self.offset + center, radius=5)

        pygame.draw.circle(self.surface, 'black', self.center_of_mass, radius=3)
        pygame.draw.circle(self.surface, 'blue', pygame.Vector2(0,0), radius=3)
