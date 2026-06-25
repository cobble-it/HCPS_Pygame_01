"""
Color Square Display
====================
Shows a single colored square with a label beneath it.
"""

import pygame
import sys

# ── Configuration ─────────────────────────────────────────────────────────────
WINDOW_W, WINDOW_H = 480, 360
FPS = 10                            # frames per second
BG_COLOR    = (255, 255, 255)
SQUARE_COLOR = (255, 100, 50)       # ← change this to any RGB value
SQUARE_SIZE = 200
LABEL_TEXT  = "RGB(255, 100, 50)"
COLOR_SIZE = 20
# ──────────────────────────────────────────────────────────────────────────────

def main():
    pygame.init()                                                   # initialize pygame
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))          # set display resolution
    pygame.display.set_caption("Color Square")                      # set window caption
    font = pygame.font.SysFont("monospace", 18)                     # set font
    clock = pygame.time.Clock()                                     # create a clock object to set FPS

    # Center the square
    #square_x = (WINDOW_W - SQUARE_SIZE) // 2
    #square_y = (WINDOW_H - SQUARE_SIZE) // 2 - 20  # shift up slightly to make room for label
    #square_rect = pygame.Rect(square_x, square_y, SQUARE_SIZE, SQUARE_SIZE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()

        screen.fill(BG_COLOR)

        # Draw the square
        #pygame.draw.rect(screen, SQUARE_COLOR, square_rect)

        # Custom Draw
        for row in range(4):
            for col in range(6):
                drawPaletteEntry(screen, 0, 0, 0, "Black", col * (COLOR_SIZE + 5), row * (COLOR_SIZE + 5))

        # Draw the label centered below the square
        #label = font.render(LABEL_TEXT, True, (220, 220, 220))
        #label_x = (WINDOW_W - label.get_width()) // 2
        #label_y = square_rect.bottom + 16
        #screen.blit(label, (label_x, label_y))

        pygame.display.flip()
        clock.tick(FPS)

def drawPaletteEntry(screen, redValue, greenValue, blueValue, colorName, coordinate_X, coordinate_Y):
    square_rect = pygame.Rect(coordinate_X, coordinate_Y, COLOR_SIZE, COLOR_SIZE)
    pygame.draw.rect(screen, (redValue, greenValue, blueValue), square_rect)


if __name__ == "__main__":
    main()