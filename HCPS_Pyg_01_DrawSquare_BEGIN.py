################################################################################
# BEGIN HERE... ANALYZE AND EXPERIMENT WITH THIS CODE
################################################################################
import pygame

def main():
    # Initialize Pygame
    pygame.init()

    # Set Up The Display
    screen_width = 400
    screen_height = 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Black Square Example")

    # Define Colors (R, G, B)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Main Game Loop
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

    # Clean Up
    pygame.quit()

# Kick-off Script
main()

###############################################################################
# EXERCISES
#
# 1. Change the Size and Position of the Square:
#    Modify the dimensions and coordinates in the pygame.draw.rect() function
#    to draw the square at different sizes and locations on the screen.
#
# 2. Change the Background Color:
#    Change the RGB values in the screen.fill() function to set a different
#    background color for the window.  Develop a set of color values to 
#    add support for BLUE, GREEN, RED, YELLOW, ORANGE, PURPLE, GREY, and PINK.
#
# 3. Add A Circle and Place it Next to the Square:
#    Use pygame.draw.circle() to draw a circle next to the square on the
#    screen.  Experiment with different sizes, colors, and positions for 
#    both the circle and square.
#
# 4. Draw a Line to Connect the Circle and Square:
#    Use pygame.draw.line() to draw a line between the center of the square
#    and the center of the circle.
###############################################################################
