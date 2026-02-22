import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Game settings
GRAVITY = 0.5
JUMP_STRENGTH = -10

# Short Jump Addition - Colton
SHORT_JUMP_STRENTH = -5

FLOOR_HEIGHT = 100

# Obstacle settings
OBSTACLE_WIDTH = 60
OBSTACLE_GAP = 150  # Gap between top and bottom obstacles
OBSTACLE_SPEED = 3  # How fast obstacles move left
OBSTACLE_SPAWN_DISTANCE = 250  # Distance between obstacles

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Ball")

# Clock to control frame rate
clock = pygame.time.Clock()

# Font for text
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

# Game states
PLAYING = 0
GAME_OVER = 1
game_state = PLAYING

# Ball (player) properties
ball_radius = 20
ball_x = SCREEN_WIDTH // 4
ball_y = SCREEN_HEIGHT // 2
ball_velocity_y = 0
ball_alive = True

# Obstacles list - each obstacle is a dictionary with position and gap height
obstacles = []

# Score
score = 0

# Spawn the first obstacle
def spawn_obstacle():
    """Create a new obstacle with random gap position"""
    floor_y = SCREEN_HEIGHT - FLOOR_HEIGHT
    # Random height for the gap (must fit between ceiling and floor)
    gap_y = random.randint(100, floor_y - OBSTACLE_GAP - 100)
    
    obstacle = {
        'x': SCREEN_WIDTH,
        'gap_y': gap_y,
        'scored': False  # Track if player has passed this obstacle
    }
    obstacles.append(obstacle)

def reset_game():
    """Reset all game variables to start a new game"""
    global ball_y, ball_velocity_y, ball_alive, obstacles, game_state, score
    ball_y = SCREEN_HEIGHT // 2
    ball_velocity_y = 0
    ball_alive = True
    obstacles = []
    spawn_obstacle()
    game_state = PLAYING
    score = 0

# Start with one obstacle
spawn_obstacle()

# Game loop
running = True
while running:
    # Handle events (user input)
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # Check for spacebar press during gameplay
            if event.key == pygame.K_SPACE and game_state == PLAYING:
                ball_velocity_y = JUMP_STRENGTH
                
            # Short Jump Addition - Colton
            elif event.key == pygame.K_b and game_state == PLAYING:
                ball_velocity_y = SHORT_JUMP_STRENTH
        
        # Check for mouse click on retry button when game is over
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == GAME_OVER:
            mouse_x, mouse_y = event.pos
            # Retry button dimensions (centered on screen)
            button_width = 200
            button_height = 60
            button_x = SCREEN_WIDTH // 2 - button_width // 2
            button_y = SCREEN_HEIGHT // 2 + 50
            
            # Check if click is inside button
            if (button_x <= mouse_x <= button_x + button_width and
                button_y <= mouse_y <= button_y + button_height):
                reset_game()
       
    # Only update game if we're playing
    if game_state == PLAYING:
        # Apply gravity to the ball
        ball_velocity_y += GRAVITY
        ball_y += ball_velocity_y
        
        # Floor collision detection
        floor_y = SCREEN_HEIGHT - FLOOR_HEIGHT
        if ball_y + ball_radius > floor_y:
            ball_alive = False
            game_state = GAME_OVER
        
        # Prevent ball from going above the screen
        if ball_y - ball_radius < 0:
            ball_alive = False
            game_state = GAME_OVER
        
        # Move obstacles left
        for obstacle in obstacles:
            obstacle['x'] -= OBSTACLE_SPEED
        
        # Remove obstacles that have gone off screen
        obstacles = [obs for obs in obstacles if obs['x'] > -OBSTACLE_WIDTH]
        
        # Spawn new obstacle when the last one is far enough
        if len(obstacles) == 0 or obstacles[-1]['x'] < SCREEN_WIDTH - OBSTACLE_SPAWN_DISTANCE:
            spawn_obstacle()
        
        # Check collision with obstacles
        for obstacle in obstacles:
            # Check if ball is horizontally aligned with obstacle
            if (obstacle['x'] < ball_x + ball_radius and 
                obstacle['x'] + OBSTACLE_WIDTH > ball_x - ball_radius):
                
                # Check if ball hits top or bottom obstacle
                if (ball_y - ball_radius < obstacle['gap_y'] or 
                    ball_y + ball_radius > obstacle['gap_y'] + OBSTACLE_GAP):
                    # Collision detected - kill the ball and end game
                    ball_alive = False
                    game_state = GAME_OVER
            
            # Check if player passed the obstacle (for scoring)
            if not obstacle['scored'] and obstacle['x'] + OBSTACLE_WIDTH < ball_x - ball_radius:
                obstacle['scored'] = True
                score += 1
    
    # Draw everything
    # Fill background with sky blue
    screen.fill(SKY_BLUE)
    
    # Draw obstacles (pipes)
    for obstacle in obstacles:
        # Top obstacle
        pygame.draw.rect(screen, GREEN, 
                        (obstacle['x'], 0, OBSTACLE_WIDTH, obstacle['gap_y']))
        
        # Bottom obstacle
        pygame.draw.rect(screen, GREEN, 
                        (obstacle['x'], obstacle['gap_y'] + OBSTACLE_GAP, 
                         OBSTACLE_WIDTH, floor_y - (obstacle['gap_y'] + OBSTACLE_GAP)))
    
    # Draw the floor
    floor_y = SCREEN_HEIGHT - FLOOR_HEIGHT
    pygame.draw.rect(screen, BROWN, (0, floor_y, SCREEN_WIDTH, FLOOR_HEIGHT))
    
    # Draw the ball (player) - only if alive
    if ball_alive:
        pygame.draw.circle(screen, YELLOW, (int(ball_x), int(ball_y)), ball_radius)
    
    # Draw score during gameplay
    if game_state == PLAYING:
        score_text = font_small.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    
    # Draw game over screen
    if game_state == GAME_OVER:
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = font_large.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(game_over_text, text_rect)
        
        # Final score
        final_score_text = font_medium.render(f"Score: {score}", True, WHITE)
        score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(final_score_text, score_rect)
        
        # Retry button
        button_width = 200
        button_height = 60
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y = SCREEN_HEIGHT // 2 + 50
        
        # Check if mouse is hovering over button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_color = WHITE if (button_x <= mouse_x <= button_x + button_width and
                                 button_y <= mouse_y <= button_y + button_height) else GRAY
        
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        pygame.draw.rect(screen, BLACK, (button_x, button_y, button_width, button_height), 3)
        
        retry_text = font_medium.render("RETRY", True, BLACK)
        retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH // 2, button_y + button_height // 2))
        screen.blit(retry_text, retry_rect)
    
    # Update the display
    pygame.display.flip()
    
    # Control frame rate (60 FPS)
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()