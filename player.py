import pygame
from pygame.locals import *

# Screen information
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.orginal_image = pygame.image.load("assets/Image/Player.png").convert_alpha()
        self.image = pygame.transform.scale(self.orginal_image, (100, 100))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:    
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -10)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 10)
         
        #if self.rect.left > 0:
            #if pressed_keys[K_LEFT]:
                #self.rect.move_ip(-10, 0)
        #if self.rect.right < SCREEN_WIDTH:        
            #if pressed_keys[K_RIGHT]:
                #self.rect.move_ip(10, 0)
 
    # def draw(self, surface):
    #     surface.blit(self.image, self.rect)     