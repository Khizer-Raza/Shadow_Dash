import pygame
from pygame.locals import *
import random

# Screen information
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
GROUND_LEVEL = 660

class Spike(pygame.sprite.Sprite):
    
    SPIKE_WIDTH = 200
    SPIKE_HEIGHT = 50
    SPIKE_Y_POSITION = GROUND_LEVEL - 25
    SPIKE_SPEED = 10
    
    def __init__(self, speed=SPIKE_SPEED):
        super().__init__()
        
        self.obstacle_type = "spike"
        self.speed = speed
        self.is_active = False
        
        # Load and scale spike image
        original_image = pygame.image.load("assets/Image/Spikes.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (self.SPIKE_WIDTH, self.SPIKE_HEIGHT))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        
        # Set initial position off-screen
        self.rect.left = SCREEN_WIDTH
        self.rect.centery = self.SPIKE_Y_POSITION
    
    def reset_position(self):
        self.rect.left = SCREEN_WIDTH
        self.rect.centery = self.SPIKE_Y_POSITION
        self.is_active = True
    
    def move(self):
        if self.is_active:
            self.rect.move_ip(-self.speed, 0)
            
            # Deactivate if completely off-screen
            if self.rect.right < 0:
                self.is_active = False


class Machine(pygame.sprite.Sprite):
    
    MACHINE_WIDTH = 400
    MACHINE_HEIGHT = 400
    MACHINE_Y_MIN = 400
    MACHINE_Y_MAX = 400
    MACHINE_SPEED = 5
    
    def __init__(self, speed=MACHINE_SPEED):
        super().__init__()
        
        self.obstacle_type = "machine"
        self.speed = speed
        self.is_active = False
        
        # Load and scale machine image
        original_image = pygame.image.load("assets/Image/Machine.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (self.MACHINE_WIDTH, self.MACHINE_HEIGHT))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        
        # Set initial position off-screen
        self.rect.left = SCREEN_WIDTH
        self.rect.centery = random.randint(self.MACHINE_Y_MIN, self.MACHINE_Y_MAX)
    
    def reset_position(self):
        self.rect.left = SCREEN_WIDTH
        self.rect.centery = random.randint(self.MACHINE_Y_MIN, self.MACHINE_Y_MAX)
        self.is_active = True
    
    def move(self):
        if self.is_active:
            self.rect.move_ip(-self.speed, 0)
            
            # Deactivate if completely off-screen
            if self.rect.right < 0:
                self.is_active = False


# ===================== OBSTACLE MANAGER =====================
class ObstacleManager:
    """Manages separate pools for spikes and machines"""
    
    def __init__(self, spike_pool_size=8, machine_pool_size=7):
        # Separate pools for spikes and machines
        self.spike_pool = [Spike() for _ in range(spike_pool_size)]
        self.machine_pool = [Machine() for _ in range(machine_pool_size)]
        
        # Active obstacles
        self.active_spikes = pygame.sprite.Group()
        self.active_machines = pygame.sprite.Group()
        
        # Spawning counters
        self.spike_spawn_counter = 0
        self.machine_spawn_counter = 0
        self.spike_spawn_interval = random.randint(80, 140)
        self.machine_spawn_interval = random.randint(100, 180)
    
    def spawn_spike(self, base_speed):
        """Spawn a spike from the pool"""
        for spike in self.spike_pool:
            if not spike.is_active:
                # Vary speed slightly
                spike.speed = Spike.SPIKE_SPEED + random.randint(-2, 2) + base_speed
                spike.reset_position()
                self.active_spikes.add(spike)
                break
    
    def spawn_machine(self, base_speed):
        """Spawn a machine from the pool"""
        for machine in self.machine_pool:
            if not machine.is_active:
                # Vary speed slightly
                machine.speed = Machine.MACHINE_SPEED + random.randint(-2, 2) + base_speed
                machine.reset_position()
                self.active_machines.add(machine)
                break
    
    def update(self, base_speed):
        """Update spawning and movement"""
        # Update spike spawning
        self.spike_spawn_counter += 1
        if self.spike_spawn_counter >= self.spike_spawn_interval:
            self.spawn_spike(base_speed)
            self.spike_spawn_counter = 0
            self.spike_spawn_interval = random.randint(80, 140)
        
        # Update machine spawning
        self.machine_spawn_counter += 1
        if self.machine_spawn_counter >= self.machine_spawn_interval:
            self.spawn_machine(base_speed)
            self.machine_spawn_counter = 0
            self.machine_spawn_interval = random.randint(100, 180)
        
        # Move spikes and remove inactive ones
        spikes_to_remove = []
        for spike in self.active_spikes:
            if spike.is_active:
                spike.move()
            else:
                spikes_to_remove.append(spike)
        for spike in spikes_to_remove:
            self.active_spikes.remove(spike)
        
        # Move machines and remove inactive ones
        machines_to_remove = []
        for machine in self.active_machines:
            if machine.is_active:
                machine.move()
            else:
                machines_to_remove.append(machine)
        for machine in machines_to_remove:
            self.active_machines.remove(machine)
    
    def get_all_obstacles(self):
        """Return all active obstacles (spikes + machines)"""
        # Combine both groups into a temporary group
        all_obs = pygame.sprite.Group()
        all_obs.add(self.active_spikes)
        all_obs.add(self.active_machines)
        return all_obs
    
    def reset(self):
        """Reset all obstacles"""
        self.active_spikes.empty()
        self.active_machines.empty()
        self.spike_spawn_counter = 0
        self.machine_spawn_counter = 0
        for spike in self.spike_pool:
            spike.is_active = False
        for machine in self.machine_pool:
            machine.is_active = False


# Legacy Enemy class for backward compatibility if needed
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.orginal_image = pygame.image.load("assets/Image/Spikes.png").convert_alpha()
        self.image = pygame.transform.scale(self.orginal_image, (200, 50))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH, 650)
 
    def move(self):
        self.rect.move_ip(-10, 0)
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
            self.rect.centery = 650