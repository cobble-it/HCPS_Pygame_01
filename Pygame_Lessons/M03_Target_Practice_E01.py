# NEW CODE With For Loop
import pygame

#Screen setup
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650

# Colors
NAVY = (18, 22, 32)
DARK_PANEL = (28, 34, 48)
RING_RED = (220, 30, 30)
RING_WHITE = (240, 240, 240)
DARK_GRAY = (65, 65, 65)

# Target rings: (radius, color)
TARGET_RINGS = [
    (18, RING_RED),
    (36, RING_RED),
    (60, RING_WHITE),
    (90, RING_WHITE),
    (126, DARK_PANEL),
]

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

        draw_target(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pygame.display.flip()

    pygame.quit()

def draw_target(screen, center_x, center_y):
    # Draw rings from largest to smallest
    for radius, color in reversed(TARGET_RINGS):
        pygame.draw.circle(screen, color, (center_x, center_y), radius)
        pygame.draw.circle(screen, DARK_GRAY, (center_x, center_y), radius, 1)

main()