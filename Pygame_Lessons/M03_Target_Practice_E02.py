#NEW CODE Target with For Loop and Crosshairs
"""
A for loop is useful here because the target is made of several circles that follow the same pattern:

Draw a circle.
Use a different radius.
Use a different color.

Instead of writing a separate pygame.draw.circle() statement for each ring, a for loop lets you repeat the same action for a list of radii and colors. This makes the code shorter, easier to read, and easier to change.
"""

import pygame

#Screen setup
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650

#Colors
NAVY = (18, 22, 32)
DARK_PANEL = (28, 34, 48)
RING_RED = (220, 30, 30)
RING_WHITE = (240, 240, 240)
DARK_GRAY = (65, 65, 65)

OUTER_RING_RADIUS = 126

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
    # Radius and color for each ring
    rings = [
        (126, DARK_PANEL),
        (90, RING_WHITE),
        (60, DARK_PANEL),
        (36, RING_RED),
        (18, RING_WHITE)
    ]

    # Draw each ring
    for radius, color in rings:
        pygame.draw.circle(screen, color, (center_x, center_y), radius)
        pygame.draw.circle(screen, DARK_GRAY, (center_x, center_y), radius, 1)

    # horizontal and vertical crosshair lines through the centre
    pygame.draw.line(screen, DARK_GRAY,
                    (center_x - OUTER_RING_RADIUS, center_y),
                    (center_x + OUTER_RING_RADIUS, center_y), 1)
    pygame.draw.line(screen, DARK_GRAY,
                    (center_x, center_y - OUTER_RING_RADIUS),
                    (center_x, center_y + OUTER_RING_RADIUS), 1)

main()