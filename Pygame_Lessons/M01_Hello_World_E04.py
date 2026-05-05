#################################################################################
# EXERCISES - DrawColoredSquareDiagonal - E4 - ANSWER
# 1. Draw an arrangement of equally sized rectangles with a varied spectral
#    color display that moves from the upper-left corner to the lower-right
#    corner. Be sure to take pride in your work.
# 
#################################################################################

# LIBRARIES
import pygame

# CONSTANTS
DISPLAY_WIDTH = 480             # Optimized for CodeHS
DISPLAY_HEIGHT = 360

COLOR_WHITE   = (255, 255, 255)       # Custom Colors
COLOR_BLACK   = (0, 0, 0)
COLOR_RED     = (255, 0, 0)
COLOR_ORANGE  = (255, 165, 0)
COLOR_YELLOW  = (255, 255, 0)
COLOR_GREEN   = (0, 128, 0)
COLOR_BLUE    = (0, 0, 255)
COLOR_PURPLE  = (148, 0, 211)

def main():
    # 1
    pygame.init()

    # 2
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Rainbow Rectangles!")

    # 3
    running = True
    while running:
        # Check for events (like clicking the 'X')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        # Fill the background with white
        screen.fill(COLOR_WHITE)
    
        # Draw the Rectangles
        # pygame.draw.rect(surface, color, [x, y, width, height]
        pygame.draw.rect(screen, COLOR_RED,    [0 * (DISPLAY_WIDTH // 6), 0 * (DISPLAY_HEIGHT // 6), (DISPLAY_WIDTH // 6), DISPLAY_HEIGHT // 6])
        pygame.draw.rect(screen, COLOR_ORANGE, [1 * (DISPLAY_WIDTH // 6), 1 * (DISPLAY_HEIGHT // 6), (DISPLAY_WIDTH // 6), DISPLAY_HEIGHT // 6])           
        pygame.draw.rect(screen, COLOR_YELLOW, [2 * (DISPLAY_WIDTH // 6), 2 * (DISPLAY_HEIGHT // 6), (DISPLAY_WIDTH // 6), DISPLAY_HEIGHT // 6])           
        pygame.draw.rect(screen, COLOR_GREEN,  [3 * (DISPLAY_WIDTH // 6), 3 * (DISPLAY_HEIGHT // 6), (DISPLAY_WIDTH // 6), DISPLAY_HEIGHT // 6])           
        pygame.draw.rect(screen, COLOR_BLUE,   [4 * (DISPLAY_WIDTH // 6), 4 * (DISPLAY_HEIGHT // 6), (DISPLAY_WIDTH // 6), DISPLAY_HEIGHT // 6])           
        pygame.draw.rect(screen, COLOR_PURPLE, [5 * (DISPLAY_WIDTH // 6), 5 * (DISPLAY_HEIGHT // 6), (DISPLAY_WIDTH // 6), DISPLAY_HEIGHT // 6])           
    
        # Update the display to show what we drew
        pygame.display.flip()

    # 5. Clean up
    pygame.quit()

main()