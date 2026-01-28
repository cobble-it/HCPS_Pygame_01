#################################################################################
# EXERCISES - DrawSquare - E4 - ANSWER
# 4. Draw a Line to Connect the Circle and Square:
#    Use pygame.draw.line() to draw a line between the center of the square
#    and the center of the circle.
#################################################################################
import pygame

# 1. Initialize Pygame
pygame.init()

# 2. Set up the display
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Black Square Example")

# 3. Define colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 4. Main Game Loop
running = True
while running:
    # Check for events (like clicking the 'X')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Drawing Logic ---
    
    # Fill the background with white
    screen.fill(WHITE)
    
    # Draw a black square
    # pygame.draw.rect(surface, color, [x, y, width, height])
    pygame.draw.rect(screen, BLACK, [150, 150, 100, 100])
    
    # Update the display to show what we drew
    pygame.display.flip()

# 5. Clean up
pygame.quit()