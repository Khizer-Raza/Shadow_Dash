import pygame
from pygame.locals import *
import sys
import time
from player import Player
from enemy import ObstacleManager

# Game States
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

pygame.init()
#pygame.mixer.init()  # Initialize mixer for sound effects

FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Screen information
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
SPEED = 1
SCORE = 0

#Setting up Fonts
font_large = pygame.font.SysFont("Verdana", 80)
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 40)
font_tiny = pygame.font.SysFont("Verdana", 30)

# PHASE 4: Visual & Audio Polish
# Sound effects setup (create dummy sounds if files not available)
# sounds = {}
# def load_sound(name, filepath):
#     """Safely load sound with fallback"""
#     try:
#         sounds[name] = pygame.mixer.Sound(filepath)
#         return True
#     except:
#         sounds[name] = None
#         return False

# # Attempt to load sounds (they're optional)
# load_sound('jump', 'assets/Sound/jump.wav')
# load_sound('collision', 'assets/Sound/collision.wav')
# load_sound('score', 'assets/Sound/score.wav')
# load_sound('speed_up', 'assets/Sound/speed_up.wav')

# Visual effects variables
collision_flash_timer = 0  # For screen flash effect on collision
collision_flash_duration = 15  # frames

# Game Over and Score texts (will be updated dynamically)
game_over_text = font_large.render("GAME OVER", True, RED)
score_card = font_small.render("Score: ", True, BLACK)

background_original = pygame.image.load("assets/Image/Background.png")
background = pygame.transform.rotate(pygame.transform.scale(background_original, (1080, 720)), 0)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Shadow Dash")

# Game state
current_state = GameState.MENU
paused = False

def init_game():
    global P1, obstacle_manager, SPEED, SCORE, collision_flash_timer
    P1 = Player()
    obstacle_manager = ObstacleManager(spike_pool_size=1, machine_pool_size=1)
    SPEED = 1
    SCORE = 0
    collision_flash_timer = 0
    return GameState.PLAYING

# def play_sound(sound_name):
#     """Play a sound effect if available"""
#     if sound_name in sounds and sounds[sound_name] is not None:
#         try:
#             sounds[sound_name].play()
#         except:
#             pass

def apply_collision_flash(surface):
    """Apply screen flash effect on collision"""
    if collision_flash_timer > 0:
        flash_intensity = int((collision_flash_timer / collision_flash_duration) * 100)
        flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        flash_surface.set_alpha(flash_intensity)
        flash_surface.fill(WHITE)
        surface.blit(flash_surface, (0, 0))

def draw_menu():
    DISPLAYSURF.fill(BLACK)
    
    title = font_large.render("SHADOW DASH", True, YELLOW)
    subtitle = font.render("Endless Running Game", True, WHITE)
    
    play_text = font_small.render("Press SPACE to Play", True, GREEN)
    instructions = font_tiny.render("UP = Jump | DOWN = Slide", True, WHITE)
    controls = font_tiny.render("P = Pause | ESC = Quit", True, WHITE)
    
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
    subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 180))
    play_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
    instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 450))
    controls_rect = controls.get_rect(center=(SCREEN_WIDTH // 2, 500))
    
    # Draw rectangles for visual framing
    pygame.draw.rect(DISPLAYSURF, YELLOW, (50, 50, SCREEN_WIDTH - 100, 200), 3)
    
    DISPLAYSURF.blit(title, title_rect)
    DISPLAYSURF.blit(subtitle, subtitle_rect)
    DISPLAYSURF.blit(play_text, play_rect)
    DISPLAYSURF.blit(instructions, instructions_rect)
    DISPLAYSURF.blit(controls, controls_rect)

def draw_pause():
    """Draw pause screen overlay"""
    # Darken the screen
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    DISPLAYSURF.blit(overlay, (0, 0))
    
    pause_text = font_large.render("PAUSED", True, YELLOW)
    resume_text = font_small.render("Press P to Resume", True, WHITE)
    
    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    
    DISPLAYSURF.blit(pause_text, pause_rect)
    DISPLAYSURF.blit(resume_text, resume_rect)

def draw_game_over(final_score):
    """Draw game over screen"""
    DISPLAYSURF.fill(RED)
    
    game_over_render = font_large.render("GAME OVER", True, YELLOW)
    score_text = font.render(f"Score: {final_score}", True, WHITE)
    restart_text = font_small.render("Press SPACE to Restart", True, WHITE)
    quit_text = font_small.render("Press ESC to Quit", True, WHITE)
    
    game_over_rect = game_over_render.get_rect(center=(SCREEN_WIDTH // 2, 150))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 450))
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, 520))
    
    DISPLAYSURF.blit(game_over_render, game_over_rect)
    DISPLAYSURF.blit(score_text, score_rect)
    DISPLAYSURF.blit(restart_text, restart_rect)
    DISPLAYSURF.blit(quit_text, quit_rect)

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

# PHASE 4: Enhanced game loop with visual/audio effects
#Game Loop Begin
while True:
    
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == KEYDOWN:
            # Space to start game or restart
            if event.key == K_SPACE:
                if current_state == GameState.MENU:
                    current_state = init_game()
                elif current_state == GameState.GAME_OVER:
                    current_state = init_game()
            
            # P to pause/resume
            if event.key == K_p:
                if current_state == GameState.PLAYING:
                    current_state = GameState.PAUSED
                elif current_state == GameState.PAUSED:
                    current_state = GameState.PLAYING
            
            # ESC to quit
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        
        if current_state == GameState.PLAYING:
            if event.type == INC_SPEED:
                SPEED += 0.5
            if event.type == SCORE_BOARD:
                SCORE += 1
    
    # Draw based on current state
    if current_state == GameState.MENU:
        draw_menu()
    
    elif current_state == GameState.PLAYING:
        # Update obstacles
        obstacle_manager.update(SPEED)
        
        # Sync enemies group with active obstacles for collision detection
        enemies = obstacle_manager.get_all_obstacles()
        
        DISPLAYSURF.blit(background, (0,0))
        
        # Draw score
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
            # PHASE 4: Play collision sound and start flash effect
            #play_sound('collision')
            collision_flash_timer = collision_flash_duration
            current_state = GameState.GAME_OVER
            P1.kill()
            obstacle_manager.reset()
        
        # Apply collision flash effect if active
        if collision_flash_timer > 0:
            collision_flash_timer -= 1
    
    elif current_state == GameState.PAUSED:
        # Draw the paused game state on top
        draw_pause()
    
    elif current_state == GameState.GAME_OVER:
        draw_game_over(SCORE)
        # Apply collision flash effect during game over
        apply_collision_flash(DISPLAYSURF)
    
    pygame.display.update()
    FramePerSec.tick(FPS)