# Gemini Pro, 4/29/2026
# "using python and pygame make a game steal the brainrot"
# How to Play:
# Move: Use the Left and Right arrow keys.
# Goal: Catch the Purple Blocks (Brainrot) to increase your score.
# Danger: Avoid the Green Blocks (Grass). Touching grass makes you lose a life.
# Difficulty: As your score goes up, the blocks will start falling faster.
# Restart: If you lose, press R to restart your brainrot collecting journey.

import pygame
import random
import sys

# --- Initialization ---
pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
PURPLE = (153, 50, 204)  # The Brainrot (Good)
GREEN = (34, 139, 34)    # The Grass (Bad!)
BLUE = (0, 191, 255)     # The Player

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Steal the Brainrot: Avoid the Grass!")
clock = pygame.time.Clock()

# Fonts
try:
    font = pygame.font.SysFont("impact", 36)
    big_font = pygame.font.SysFont("impact", 60)
except:
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 60)

# --- Game Variables ---
# Player
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 20
player_speed = 8

# Falling Objects
brainrots = []
grasses = []
object_size = 40
fall_speed = 5

score = 0
lives = 3

def spawn_object(obj_list):
    """Spawns an object at a random x position at the top of the screen."""
    x = random.randint(0, WIDTH - object_size)
    y = -object_size
    obj_list.append(pygame.Rect(x, y, object_size, object_size))

# --- Main Game Loop ---
running = True
game_over = False

while running:
    screen.fill(BLACK)

    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # 2. Player Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

        # 3. Spawning Logic
        # Spawn brainrot slightly faster than grass
        if random.randint(1, 25) == 1:
            spawn_object(brainrots)
        if random.randint(1, 45) == 1:
            spawn_object(grasses)

        # 4. Update & Draw Brainrot (Score Points)
        for br in brainrots[:]:
            br.y += fall_speed
            pygame.draw.rect(screen, PURPLE, br)
            
            # Collision detection
            if br.colliderect(player_rect):
                brainrots.remove(br)
                score += 10
                # Slowly increase difficulty
                if score % 50 == 0:
                    fall_speed += 0.5 
            elif br.y > HEIGHT:
                brainrots.remove(br)

        # 5. Update & Draw Grass (Lose Lives)
        for grass in grasses[:]:
            grass.y += fall_speed
            pygame.draw.rect(screen, GREEN, grass)
            
            # Collision detection
            if grass.colliderect(player_rect):
                grasses.remove(grass)
                lives -= 1
            elif grass.y > HEIGHT:
                grasses.remove(grass)

        # 6. Draw Player
        pygame.draw.rect(screen, BLUE, player_rect)

        # 7. Draw UI (Score & Lives)
        score_text = font.render(f"Brainrot Stolen: {score}", True, PURPLE)
        lives_text = font.render(f"Lives: {lives}", True, GREEN)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 150, 10))

        # Check for Game Over condition
        if lives <= 0:
            game_over = True

    else:
        # --- Game Over Screen ---
        game_over_text = big_font.render("YOU TOUCHED GRASS", True, GREEN)
        sub_text = font.render(f"Final Brainrot Score: {score}", True, WHITE)
        restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, PURPLE)
        
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

        # Handle Restart/Quit inputs
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game variables
            score = 0
            lives = 3
            fall_speed = 5
            brainrots.clear()
            grasses.clear()
            player_x = WIDTH // 2 - player_size // 2
            game_over = False
        if keys[pygame.K_q]:
            running = False

    # Update Display and maintain FPS
    pygame.display.flip()
    clock.tick(FPS)

# --- Cleanup ---
pygame.quit()
sys.exit()
