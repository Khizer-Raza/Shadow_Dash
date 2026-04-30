import pygame
from pygame.locals import *

# Screen information
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

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
            self.rect.centery = 650 #random.randint(30, SCREEN_HEIGHT-30)