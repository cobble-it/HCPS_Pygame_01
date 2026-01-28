################################################################################
# EXERCISES - DrawSquare - E2 - ANSWER
# 2. Change the Background Color:
#    Change the RGB values in the screen.fill() function to set a different
#    background color for the window.  Develop a set of color values to 
#    add support for BLUE, GREEN, RED, YELLOW, ORANGE, PURPLE, GREY, and PINK.
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
        
        # Draw the rectangle in the upper-left corner and double its size.
        pygame.draw.rect(screen, BLACK, [0, 0, 200, 200])
    
        # Update the display to show what we drew
        pygame.display.flip()

    # Clean Up
    pygame.quit()

# Kick-off Script
main()