################################################################################
# EXERCISES - DrawSquare - E3 - ANSWER
# 3. Add A Circle and Place it Next to the Square:
#    Use pygame.draw.circle() to draw a circle next to the square on the
#    screen.  Experiment with different sizes, colors, and positions for 
#    both the circle and square.
################################################################################

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