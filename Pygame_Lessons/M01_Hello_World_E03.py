####################################################################################################
# DIRECTIONS:                                                                                      
# Modify the "Hello_World.py" script to make the text fade in and out on the display.              
#################################################################################################### 

# Libraries
import pygame
import sys

# Constants
DISPLAY_WIDTH       = 480               # optimal value for CodeHS
DISPLAY_HEIGHT      = 360               # optimal value for CodeHS
DISPLAY_FPS         = 10                # optimal value for CodeHS
COLOR_BLACK         = (0, 0, 0)
COLOR_WHITE         = (255, 255, 255)

ALPHA_MIN           = 0                 # minimum alpha value to bottom out on
ALPHA_MAX           = 255               # maximum alpha value to cap out on
ALPHA_SHIFT_RATE    = 10                # rate at which alpha changes
                                        #  (higher value = quicker change)

def main():
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Create window
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Hello World")

    # Set up font
    font = pygame.font.SysFont(None, 48)
    textSurface = font.render("Hello, World!", True, COLOR_WHITE)
    
    # Main loop
    alphaValue = 0          # alpha value used to display text
    alphaDirection = 1      # 1 = alpha rising | 0 = alpha falling
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill background
        screen.fill(COLOR_BLACK)

        # Move the alpha value up and down systematically.
        if alphaDirection == 1:
            alphaValue += ALPHA_SHIFT_RATE
            if alphaValue >= ALPHA_MAX:
                alphaDirection *= -1
        else:
            alphaValue -= ALPHA_SHIFT_RATE
            if alphaValue <= ALPHA_MIN:
                alphaDirection *= -1

        # Set the alpha value.
        textSurface.set_alpha(alphaValue)
        
        #
        text_rect = textSurface.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2))
        screen.blit(textSurface, text_rect)

        # Update display (page flip)
        pygame.display.flip()

        # Stabalize FPS
        clock.tick(DISPLAY_FPS)

    # Clean up
    pygame.quit()

main()