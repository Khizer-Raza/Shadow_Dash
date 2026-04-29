import pygame
from pygame.locals import *
import random

# Screen information
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.orginal_image = pygame.image.load("assets/Image/Enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.orginal_image, (100, 100))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH, random.randint(40, SCREEN_HEIGHT-40))
 
    def move(self):
        self.rect.move_ip(-10, 0)
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
            self.rect.centery = random.randint(30, SCREEN_HEIGHT-30)