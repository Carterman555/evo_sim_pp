import pygame, weakref
from dna import DNA
import numpy as np
from helper import *
from enums import BoneSide
from constants import *

from booster import Booster
from mouth import Mouth

class Creature():
    _instances = set()

    def __init__(self, updatable, dna, pos):
        Creature._instances.add(self)

        self.updatable = updatable
        self.dna = dna

        self.joints = self.dna.structure.vertices
        self.bones = self.dna.structure.edges

        joint_x_positions = self.joints[:, 0]
        joint_y_positions = self.joints[:, 1]
        self.width = joint_x_positions.max() - joint_x_positions.min()
        self.height = joint_y_positions.max() - joint_y_positions.min()

        padding = 20
        self.offset = pygame.Vector2(padding/2, padding/2)

        self.pos = pygame.Vector2(pos)
        self.angle = 0

        self.vel = pygame.Vector2(0, 0)
        self.angvel = 0  # Start with no angular velocity
        
        # Physics properties
        self.center_of_mass = (self.joints.sum(axis=0) / len(self.joints))
        self.center_of_mass += self.offset

        self.mass = len(self.joints)  # Mass proportional to number of joints
        self.moment_of_inertia = self.calculate_moment_of_inertia()
        self.damping = 0.98  # Air resistance
        self.angular_damping = 0.95  # Rotational air resistance

        self.boosters = []
        for booster_data in self.dna.booster_data:
            self.boosters.append(Booster(self, booster_data))

        self.mouths = []
        for mouth_data in self.dna.mouth_data:
            self.mouths.append(Mouth(self, mouth_data, updatable))
        
        self.max_energy = 100
        self.energy = self.max_energy

        self.invincible = True # start invincible for a little
        self.invincibilty_timer = INVINCIBILITY_TIME

        self.surface = pygame.Surface((self.width + padding, self.height + padding), pygame.SRCALPHA)
        self.draw_shapes()


    def calculate_moment_of_inertia(self):
        """Calculate moment of inertia based on joint positions"""
        I = 0
        for joint in self.joints:
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
        
        for booster in self.boosters:
            force_vector = booster.force_vector()
            total_force += force_vector
            
            r = self.global_pos(booster.rect.center) - self.global_pos(self.center_of_mass)
            torque = r.x * force_vector.y - r.y * force_vector.x
            total_torque += torque
        
        # Apply linear physics
        acceleration = total_force / self.mass
        self.vel += acceleration
        self.vel *= self.damping
        # self.pos += self.vel

        # Apply rotational physics
        angular_acceleration = total_torque / self.moment_of_inertia
        self.angvel += angular_acceleration
        self.angvel *= self.angular_damping
        # self.angle += self.angvel
        
        self.angle = self.angle % 360

        energy_drain = BASE_ENERGY_DRAIN
        for booster in self.boosters:
            energy_drain += (booster.data.size / 10) * BOOSTER_ENERGY_USAGE

        self.energy -= energy_drain/100
        if self.energy <= 0:
            Creature._instances.remove(self)

        if self.invincible:
            self.invincibilty_timer -= 1
            if self.invincibilty_timer < 0:
                self.invincible = False


    def reproduce(self):
        offset = (0,100)
        Creature(self.pos + offset, self.updatable)


    def draw(self, screen):
        # offset is center of mass relative to center instead of topleft
        offset = pygame.Vector2(self.width/2, self.height/2) - self.center_of_mass 
        rotated_surf, rect = rotate(self.surface, self.angle, self.pos, offset)

        if self.invincible:
            rotated_surf.set_alpha(100)

        screen.blit(rotated_surf, rect)

        # energy bar
        energy_bar_back = pygame.Rect(rect.center, (50, 10))
        pygame.draw.rect(screen, 'black', energy_bar_back)

        max_width = 46
        width = max_width * (self.energy / self.max_energy)

        energy_bar = pygame.Rect(rect.center + pygame.Vector2((2,2)), (width, 6))
        pygame.draw.rect(screen, 'lightgreen', energy_bar)

    def draw_shapes(self):
        self.surface.fill((0,0,0,20)) # to visualize surface

        # bones
        bone_positions = self.dna.structure.get_edge_positions()
        for bone in bone_positions:
            start_pos = bone[0]
            end_pos = bone[1]
            pygame.draw.line(self.surface, 'white', self.offset + start_pos, self.offset + end_pos, 3)
            
        # joints
        for joint_pos in self.dna.structure.vertices:
            # joint_pos = tuple(joint_pos) # TODO - remove this line if useless
            pygame.draw.circle(self.surface, 'red', self.offset + joint_pos, radius=5)

        # boosters
        for booster in self.boosters:
            booster.draw(self.surface)

        # mouths
        for mouth in self.mouths:
            mouth.draw(self.surface)


        # Center of mass
        pygame.draw.circle(self.surface, 'black', self.center_of_mass, radius=3)


    def global_pos(self, local_pos):
        """Convert local position to global world position"""
        # Translate to origin (relative to center of mass)

        relative_pos = (local_pos-self.offset) - self.center_of_mass

        # Rotate around origin
        cos_angle = np.cos(np.radians(self.angle))
        sin_angle = np.sin(np.radians(self.angle))
        
        rotated_x = relative_pos[0] * cos_angle - relative_pos[1] * sin_angle
        rotated_y = relative_pos[0] * sin_angle + relative_pos[1] * cos_angle
        
        # Translate back and add world position
        global_pos = pygame.Vector2(rotated_x, rotated_y) + self.pos
        
        return global_pos
