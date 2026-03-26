####################################################################
# change the alignment of the text box as well as the size of them #
####################################################################
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
    text = font.render("Hello, World!", True, (255, 255, 255))

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill background
        screen.fill((0, 0, 0))

        # Draw text (centered)
        # change the text box to be left aligned and move it to the upper left corner of the screen
        text_rect = text.get_rect(left=(width // 3, height // 3))

        screen.blit(text, text_rect)

        # Update display (page flip)
        pygame.display.flip()
main()
# Clean up
pygame.quit()
sys.exit()