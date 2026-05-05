import pygame
import sys

# --- Initialization ---
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Runner")

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)  # The Player
GREEN = (0, 255, 0)    # The Goal

# --- Game Settings ---
FPS = 60
clock = pygame.time.Clock()
SPEED = 5

# --- Player Setup ---
# The player is a rect for collision math, but we draw it as a circle
player_rect = pygame.Rect(50, 50, 20, 20) 

# --- Wall Setup ---
# Create a list of rectangles to act as walls
walls = [
    # Borders
    pygame.Rect(0, 0, WIDTH, 10),              # Top
    pygame.Rect(0, HEIGHT-10, WIDTH, 10),      # Bottom
    pygame.Rect(0, 0, 10, HEIGHT),             # Left
    pygame.Rect(WIDTH-10, 0, 10, HEIGHT),      # Right
    
    # Maze Walls (x, y, width, height)
    pygame.Rect(100, 0, 20, 400),
    pygame.Rect(200, 200, 20, 400),
    pygame.Rect(300, 100, 300, 20),
    pygame.Rect(450, 300, 20, 300),
    pygame.Rect(600, 0, 20, 400),
]

# The Goal (Reach this to win)
goal_rect = pygame.Rect(WIDTH - 60, HEIGHT - 60, 40, 40)

def main():
    running = True
    
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2. Movement & Collision Logic
        keys = pygame.key.get_pressed()
        
        # Move along X axis first
        if keys[pygame.K_LEFT]:
            player_rect.x -= SPEED
        if keys[pygame.K_RIGHT]:
            player_rect.x += SPEED
            
        # Check X collisions
        for wall in walls:
            if player_rect.colliderect(wall):
                if keys[pygame.K_LEFT]:
                    player_rect.x += SPEED # Undo move
                if keys[pygame.K_RIGHT]:
                    player_rect.x -= SPEED # Undo move

        # Move along Y axis second
        if keys[pygame.K_UP]:
            player_rect.y -= SPEED
        if keys[pygame.K_DOWN]:
            player_rect.y += SPEED
            
        # Check Y collisions
        for wall in walls:
            if player_rect.colliderect(wall):
                if keys[pygame.K_UP]:
                    player_rect.y += SPEED # Undo move
                if keys[pygame.K_DOWN]:
                    player_rect.y -= SPEED # Undo move

        # Check Win Condition
        if player_rect.colliderect(goal_rect):
            print("You Win!")
            # Reset player to start
            player_rect.x = 50
            player_rect.y = 50

        # 3. Drawing
        screen.fill(WHITE) # Clear screen
        
        # Draw Walls
        for wall in walls:
            pygame.draw.rect(screen, BLACK, wall)
            
        # Draw Goal
        pygame.draw.rect(screen, GREEN, goal_rect)
        
        # Draw Player (Draw a circle at the center of the player_rect)
        pygame.draw.circle(screen, BLUE, player_rect.center, 10)

        # Update Display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

'''
HCPS_PYG_02_SimpleMaze_E1_ANS.py
Nick Schoeb
2026-02-12 @ 0800
Gemini 3 Pro
"make a simple pygame game where you hit arrow keys to move a ball around a maze"
'''
