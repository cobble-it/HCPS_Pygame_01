#########################################################################
# 1.) Modify the code to alter the text displayed in the window to say something else   #
# adittionally try to change the color of the background                #
#########################################################################

import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()

    # Create window
    width, height = 480, 360
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hello World")

    # Set up font
    font = pygame.font.SysFont(None, 48)
    text = font.render("This is a different message!", True, (255, 255, 255)) # Altered the text displayed to be white

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill background
        screen.fill((255, 0, 0)) # make the background red instead of black

        # Draw text (centered)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)

        # Update display (page flip)
        pygame.display.flip()

    # Clean up
    pygame.quit()
    sys.exit()

main()