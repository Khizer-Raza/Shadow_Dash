import pygame
from pygame.locals import *
import sys
import time
from player import Player
from enemy import Enemy

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen information
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
SPEED = 1
SCORE = 0

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 40)
game_over = font.render("Game Over", True, BLACK)
score_card = font.render("Score: ", True, BLACK)
 
background_original = pygame.image.load("assets/Image/Background.png")
background = pygame.transform.rotate(pygame.transform.scale(background_original, (1080, 720)), 0)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Car Game") 
         
#Setting up Sprites        
P1 = Player()
E1 = Enemy()
 
#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
SCORE_BOARD = pygame.USEREVENT + 2
pygame.time.set_timer(SCORE_BOARD, 1000)
pygame.time.set_timer(INC_SPEED, 1000)

#Game Loop Begin
while True:
    
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5
        if event.type == SCORE_BOARD:
              SCORE += 1
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, WHITE)
    DISPLAYSURF.blit(scores, (30,10))
    
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    
    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        #pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
          
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))
        DISPLAYSURF.blit(score_card, (30,350))
        DISPLAYSURF.blit(scores, (250,365))
          
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()        
         
    pygame.display.update()
    FramePerSec.tick(FPS)