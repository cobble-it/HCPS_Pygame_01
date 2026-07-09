# NEW CODE Target and Showing Mouse Click
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
YELLOW = (255, 255, 0)

OUTER_RING_RADIUS = 126

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Target")

    running = True

    # Stores the most recent click location
    click_position = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Save mouse click position
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_position = event.pos

        screen.fill(NAVY)

        # Draw target in center of screen
        draw_target(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Draw a marker where the user clicked
        if click_position:
            pygame.draw.circle(screen, YELLOW, click_position, 8)

            pygame.draw.line(
                screen, YELLOW,
                (click_position[0] - 12, click_position[1]),
                (click_position[0] + 12, click_position[1]), 2
            )
            pygame.draw.line(
                screen, YELLOW,
                (click_position[0], click_position[1] - 12),
                (click_position[0], click_position[1] + 12), 2
            )

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

    # Horizontal and vertical crosshair lines through the center
    pygame.draw.line(
        screen, DARK_GRAY,
        (center_x - OUTER_RING_RADIUS, center_y),
        (center_x + OUTER_RING_RADIUS, center_y), 1
    )
    pygame.draw.line(
        screen, DARK_GRAY,
        (center_x, center_y - OUTER_RING_RADIUS),
        (center_x, center_y + OUTER_RING_RADIUS), 1
    )

main()