# NEW CODE No For Loop
import pygame

# Screen setup
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650

# Colors
NAVY = (18, 22, 32)
DARK_PANEL = (28, 34, 48)
RING_RED = (220, 30, 30)
RING_WHITE = (240, 240, 240)
DARK_GRAY = (65, 65, 65)

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Target")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(NAVY)

        # Draw target in the center of the screen
        draw_target(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pygame.display.flip()

    pygame.quit()

def draw_target(screen, center_x, center_y):
    # Outer black ring
    pygame.draw.circle(screen, DARK_PANEL, (center_x, center_y), 126)
    pygame.draw.circle(screen, DARK_GRAY, (center_x, center_y), 126, 1)

    # White ring
    pygame.draw.circle(screen, RING_WHITE, (center_x, center_y), 90)
    pygame.draw.circle(screen, DARK_GRAY, (center_x, center_y), 90, 1)

    # White ring
    pygame.draw.circle(screen, RING_WHITE, (center_x, center_y), 60)
    pygame.draw.circle(screen, DARK_GRAY, (center_x, center_y), 60, 1)

    # Inner red ring
    pygame.draw.circle(screen, RING_RED, (center_x, center_y), 36)
    pygame.draw.circle(screen, DARK_GRAY, (center_x, center_y), 36, 1)

    # Bullseye
    pygame.draw.circle(screen, RING_RED, (center_x, center_y), 18)
    pygame.draw.circle(screen, DARK_GRAY, (center_x, center_y), 18, 1)




main()