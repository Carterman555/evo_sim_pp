import pygame
from dna import DNA
import numpy as np
from helper import *
from enums import BoneSide
from constants import *

from booster import Booster
from mouth import Mouth

class Creature():
    def __init__(self, x, y, updatable):
        self.dna = DNA()

        joint_x_positions = self.dna.joints[:, 0]
        joint_y_positions = self.dna.joints[:, 1]
        self.width = joint_x_positions.max() - joint_x_positions.min()
        self.height = joint_y_positions.max() - joint_y_positions.min()

        padding = 20
        self.offset = pygame.Vector2(padding/2, padding/2)

        self.pos = pygame.Vector2(x, y)
        self.angle = 0

        self.vel = pygame.Vector2(0, 0)
        self.angvel = 0  # Start with no angular velocity
        
        # Physics properties
        self.center_of_mass = (self.dna.joints.sum(axis=0) / len(self.dna.joints))
        self.center_of_mass += self.offset

        self.mass = len(self.dna.joints)  # Mass proportional to number of joints
        self.moment_of_inertia = self.calculate_moment_of_inertia()
        self.damping = 0.98  # Air resistance
        self.angular_damping = 0.95  # Rotational air resistance

        # self.dna.boosters.append(Booster(self,bone_index=0,side=BoneSide.BOTTOM,pos_on_bone=100,size=30))
        self.dna.mouths.append(Mouth(self,bone_index=2,side=BoneSide.BOTTOM,pos_on_bone=120,size=200))
        
        self.max_energy = 100
        self.energy = self.max_energy

        self.dead = False

        self.surface = pygame.Surface((self.width + padding, self.height + padding), pygame.SRCALPHA)
        self.draw_shapes()

        for mouth in self.dna.mouths:
            updatable.add(mouth)

    def calculate_moment_of_inertia(self):
        """Calculate moment of inertia based on joint positions"""
        I = 0
        for joint in self.dna.joints:
            joint_pos = joint + self.offset
            distance = (joint_pos - self.center_of_mass) / 10 # divide by 10 because r squared gets really large without it
            r_squared = (distance ** 2).sum()
            I += r_squared

        # Scale down the moment of inertia to make rotation more responsive
        # You can adjust this scaling factor to tune rotational responsiveness
        scaling_factor = 0.5
        return max(I * scaling_factor, 0.1)  # Ensure minimum value

    def update(self):
        # Apply forces from boosters
        total_force = pygame.Vector2(0, 0)
        total_torque = 0
        
        booster_strength = 0.01
        
        for booster in self.dna.boosters:
            force_vector = booster.direction.rotate(self.angle) * booster.size * booster_strength
            total_force += force_vector
            
            r = self.global_pos(booster.rect.center) - self.global_pos(self.center_of_mass)
            torque = r.x * force_vector.y - r.y * force_vector.x
            total_torque += torque
        
        # Apply linear physics
        acceleration = total_force / self.mass
        self.vel += acceleration
        self.vel *= self.damping
        self.pos += self.vel

        # Apply rotational physics
        angular_acceleration = total_torque / self.moment_of_inertia
        self.angvel += angular_acceleration
        self.angvel *= self.angular_damping
        self.angle += self.angvel
        
        self.angle = self.angle % 360


        energy_drain = BASE_ENERGY_DRAIN
        for booster in self.dna.boosters:
            energy_drain += (booster.size / 10) * BOOSTER_ENERGY_USAGE

        self.energy -= energy_drain/100
        if self.energy <= 0 and not self.dead:
            self.dead = True


    def draw(self, screen):
        # offset is center of mass relative to center instead of topleft
        offset = pygame.Vector2(self.width/2, self.height/2) - self.center_of_mass 
        rotated_surf, rect = rotate(self.surface, self.angle, self.pos, offset)
        screen.blit(rotated_surf, rect)

        # energy bar
        energy_bar_back = pygame.Rect(rect.center, (50, 10))
        pygame.draw.rect(screen, 'black', energy_bar_back)

        max_width = 46
        width = max_width * (self.energy / self.max_energy)

        energy_bar = pygame.Rect(rect.center + pygame.Vector2((2,2)), (width, 6))
        pygame.draw.rect(screen, 'lightgreen', energy_bar)

    def draw_shapes(self):
        #self.surface.fill((0,0,0,20)) # to visualize surface

        # bones
        for bone in self.dna.get_bone_positions():
            start_pos = bone[0]
            end_pos = bone[1]
            pygame.draw.line(self.surface, 'white', self.offset + start_pos, self.offset + end_pos, 3)
            
        # joints
        for joint in self.dna.joints:
            joint_pos = tuple(joint)
            pygame.draw.circle(self.surface, 'red', self.offset + joint_pos, radius=5)

        # boosters
        for booster in self.dna.boosters:
            booster.draw(self.surface)

        # mouths
        for mouth in self.dna.mouths:
            mouth.draw(self.surface)


        # Center of mass
        pygame.draw.circle(self.surface, 'black', self.center_of_mass, radius=3)


    def global_pos(self, local_pos):
        """Convert local position to global world position"""
        # Translate to origin (relative to center of mass)
        relative_pos = local_pos - self.center_of_mass

        # Rotate around origin
        cos_angle = np.cos(np.radians(self.angle))
        sin_angle = np.sin(np.radians(self.angle))
        
        rotated_x = relative_pos[0] * cos_angle - relative_pos[1] * sin_angle
        rotated_y = relative_pos[0] * sin_angle + relative_pos[1] * cos_angle
        
        # Translate back and add world position
        global_pos = pygame.Vector2(rotated_x, rotated_y) + self.pos
        
        return global_pos
