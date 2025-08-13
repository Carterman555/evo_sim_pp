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

        padding = 20
        self.offset = pygame.Vector2(padding/2, padding/2)

        self.surface = pygame.Surface((self.width + padding, self.height + padding), pygame.SRCALPHA)

        self.pos = pygame.Vector2(x, y)
        self.angle = 0

        self.vel = pygame.Vector2(0, 0)
        self.angvel = 0  # Start with no angular velocity
        
        # Physics properties
        self.mass = len(self.DNA.joints)  # Mass proportional to number of joints
        self.moment_of_inertia = self.calculate_moment_of_inertia()
        self.damping = 0.98  # Air resistance
        self.angular_damping = 0.90  # Rotational air resistance

        # Calculate center of mass
        sum_pos = pygame.Vector2(0, 0)
        for joint in self.DNA.joints:
            sum_pos += joint
        self.center_of_mass = sum_pos / len(self.DNA.joints)
        self.center_of_mass += self.offset
        
        self.draw_shapes()

    def calculate_moment_of_inertia(self):
        """Calculate moment of inertia based on joint positions"""
        I = 0
        local_com = (self.DNA.joints.sum(axis=0) / len(self.DNA.joints))
        
        for joint in self.DNA.joints:
            # Distance from center of mass (before adding offset)
            r_squared = ((joint - local_com) ** 2).sum()
            I += r_squared  # Assuming unit mass per joint
        
        # Scale down the moment of inertia to make rotation more responsive
        # You can adjust this scaling factor to tune rotational responsiveness
        scaling_factor = 0.001  # Reduce moment of inertia by 90%
        return max(I * scaling_factor, 0.1)  # Ensure minimum value

    def update(self, dt):
        # Apply forces from boosters
        total_force = pygame.Vector2(0, 0)
        total_torque = 0
        
        # Increase booster strength for more dramatic effects
        booster_strength = 100  # Increased from 100
        
        # Process each booster
        for bone_index in self.DNA.boosters:
            booster_pos = self.DNA.get_bone_center(bone_index)

            # Get the bone vector and create force perpendicular to it
            bone_vector = self.DNA.get_bone_vector(bone_index)
            if bone_vector.length() > 0:
                bone_vector.normalize_ip()
                # Force perpendicular to bone (you can adjust the angle)
                force_vector = bone_vector.rotate(270) * booster_strength
                
                # Add to total linear force
                total_force += force_vector
                
                # Calculate torque: r × F (cross product in 2D)
                # Vector from center of mass to booster position
                r = (booster_pos + self.offset) - self.center_of_mass
                
                # 2D cross product: r × F = r.x * F.y - r.y * F.x
                torque = r.x * force_vector.y - r.y * force_vector.x
                total_torque += torque
        
        # Apply linear physics
        acceleration = total_force / self.mass
        self.vel += acceleration * dt
        self.vel *= self.damping  # Apply damping
        self.pos += self.vel * dt
        
        # Apply rotational physics
        angular_acceleration = total_torque / self.moment_of_inertia
        self.angvel += angular_acceleration * dt
        self.angvel *= self.angular_damping  # Apply rotational damping
        self.angle += self.angvel * dt
        
        # Keep angle in reasonable range
        self.angle = self.angle % 360

    def get_global_pos(self, local_pos):
        """Convert local position to global world position"""
        # Translate to origin (relative to center of mass)
        relative_pos = local_pos - self.center_of_mass
        
        # Rotate around origin
        cos_angle = np.cos(np.radians(self.angle))
        sin_angle = np.sin(np.radians(self.angle))
        
        rotated_x = relative_pos.x * cos_angle - relative_pos.y * sin_angle
        rotated_y = relative_pos.x * sin_angle + relative_pos.y * cos_angle
        
        # Translate back and add world position
        global_pos = pygame.Vector2(rotated_x, rotated_y) + self.pos
        
        return global_pos

    def get_booster_global_pos(self, booster_local_pos):
        """Get the global position of a booster for force visualization"""
        booster_with_offset = booster_local_pos + self.offset
        return self.get_global_pos(booster_with_offset)

    def draw(self, screen):
        # offset is center of mass relative to center instead of topleft
        offset = pygame.Vector2(self.width/2, self.height/2) - self.center_of_mass 
        rotated_surf, rect = rotate_around(self.surface, self.angle, self.pos, offset)
        screen.blit(rotated_surf, rect)

    def draw_shapes(self):
        #self.surface.fill((0,0,0,20)) # to visualize surface

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
        for pos in self.DNA.get_booster_positions():
            pygame.draw.circle(self.surface, 'blue', self.offset + pos, radius=5)

        # Center of mass
        pygame.draw.circle(self.surface, 'black', self.center_of_mass, radius=3)