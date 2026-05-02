import pygame
from pygame.locals import *
from time import sleep

# Screen information
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

# Ground level for the player
GROUND_LEVEL = 660

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        # Load and cache all images at initialization
        self.image_running = pygame.image.load("assets/Image/Character_running.png").convert()
        self.image_running = pygame.transform.scale(self.image_running, (98, 100))
        self.image_running.set_colorkey((0, 0, 0))
        
        self.image_jumping = pygame.image.load("assets/Image/Character_jumping.png").convert()
        self.image_jumping = pygame.transform.scale(self.image_jumping, (72, 100))
        self.image_jumping.set_colorkey((255, 255, 255))
        
        self.image_sliding = pygame.image.load("assets/Image/Character_sliding.png").convert()
        self.image_sliding = pygame.transform.scale(self.image_sliding, (100, 50))
        self.image_sliding.set_colorkey((255, 255, 255))
        
        # Set initial image and rect
        self.image = self.image_running
        self.rect = self.image.get_rect()
        self.rect.center = (160, GROUND_LEVEL)
        
        # Physics variables for gravity
        self.velocity_y = 0
        self.gravity = 0.6
        self.jump_power = -15
        
        # State tracking
        self.is_jumping = False
        self.is_sliding = False
        self.slide_timer = 0
        self.slide_duration = 90  # frames for how long sliding lasts
        
        # Store original y position for sliding
        self.slide_offset = 60  # how much lower the player goes when sliding

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        # Handle jumping
        if pressed_keys[K_UP] and not self.is_jumping: #and not self.is_sliding
            self.slide_timer = 0
            self.is_jumping = True
            self.velocity_y = self.jump_power
        
        # Handle sliding
        if pressed_keys[K_DOWN]: #and not self.is_jumping and not self.is_sliding
            self.is_sliding = True
            self.slide_timer = self.slide_duration
        
        # Apply gravity when jumping
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.move_ip(0, self.velocity_y)
            self.image = self.image_jumping
            
            # Check if landed on ground
            if self.rect.bottom >= GROUND_LEVEL:
                self.rect.bottom = GROUND_LEVEL
                self.is_jumping = False
                self.velocity_y = 0
        
        # Handle sliding
        if self.is_sliding:
            self.image = self.image_sliding
            self.rect.bottom = GROUND_LEVEL + self.slide_offset
            self.slide_timer -= 1
            
            if self.slide_timer <= 0:
                self.is_sliding = False
                self.rect.bottom = GROUND_LEVEL
        
        # Auto-return to running state
        if not self.is_jumping and not self.is_sliding:
            self.image = self.image_running
            self.rect.bottom = GROUND_LEVEL    