import pygame
from pygame.locals import *
import sys
import time
from player import Player
from enemy import ObstacleManager

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
obstacle_manager = ObstacleManager(spike_pool_size=1, machine_pool_size=1)
 
#Creating Sprites Groups
enemies = pygame.sprite.Group()  # Will be updated each frame with active obstacles
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)

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
    
    # Update obstacles
    obstacle_manager.update(SPEED)
    
    # Sync enemies group with active obstacles for collision detection
    enemies = obstacle_manager.get_all_obstacles()
    
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, WHITE)
    DISPLAYSURF.blit(scores, (30,10))
    
    #Moves and Re-draws all Sprites (player only)
    DISPLAYSURF.blit(P1.image, P1.rect)
    P1.move()
    
    # Draw all active obstacles
    for obstacle in enemies:
        DISPLAYSURF.blit(obstacle.image, obstacle.rect)
    
    #To be run if collision occurs between Player and any Obstacle
    collision_occurs = False
    
    for obstacle in enemies:
        # Collision mechanics:
        # Running:  Collision with Spike AND Collision with Machine
        # Sliding:  Collision with Spike AND Pass under Machine
        # Jumping:  Collision with Spike AND Collision with Machine
        
        if P1.is_sliding:
            # Sliding: always collides with spikes, passes under machines
            if obstacle.obstacle_type == "spike":
                # Spike at ground level - sliding doesn't help, still collides
                if P1.rect.colliderect(obstacle.rect):
                    collision_occurs = True
                    break
            else:  # machine
                # Machine in air - sliding allows passing under it
                continue  # No collision with machine when sliding
        elif P1.is_jumping:
            # Jumping: collides with both spikes and machines
            if P1.rect.colliderect(obstacle.rect):
                collision_occurs = True
                break
        else:  # Running
            # Running: collides with both spikes and machines
            if P1.rect.colliderect(obstacle.rect):
                collision_occurs = True
                break
    
    if collision_occurs:
        #pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))
        DISPLAYSURF.blit(score_card, (30,350))
        DISPLAYSURF.blit(scores, (250,365))
          
        pygame.display.update()
        P1.kill()
        obstacle_manager.reset()
        time.sleep(2)
        pygame.quit()
        sys.exit()
         
    pygame.display.update()
    FramePerSec.tick(FPS)