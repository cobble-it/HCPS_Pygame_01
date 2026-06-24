# color_squares.py
# A beginner-friendly Pygame program that shows how to draw colored squares.
# Demonstrates: RGB colors, loops, coordinates, and how to lay out a grid.
#
# KEY IDEAS:
#   - Every color is a mix of Red, Green, and Blue (each 0–255)
#   - pygame.draw.rect draws a rectangle at (x, y) with a given width and height
#   - We use a loop to draw many squares without repeating ourselves

import pygame
import sys

# ── Constants ──────────────────────────────────────────────────────────────────

WINDOW_WIDTH  = 820
WINDOW_HEIGHT = 680
WINDOW_TITLE  = "Color Squares — RGB Explorer"
FPS           = 60

BACKGROUND    = (240, 240, 240)   # light grey background
BLACK         = (  0,   0,   0)
DARK_GRAY     = ( 60,  60,  60)

SQUARE_SIZE   = 110   # each square is 110 x 110 pixels
GAP           =  18   # space between squares
MARGIN_LEFT   =  30   # space from the left edge to the first column
MARGIN_TOP    =  80   # space from the top edge to the first row


# ── Color Data ─────────────────────────────────────────────────────────────────
# Each entry is:  (Red, Green, Blue),  "Color Name"
#
# Try changing the numbers and see what happens!
# Red, Green, Blue each go from 0 (none) to 255 (full).

COLOR_DATA = [
    # Row 1 – Primary colors + black & white
    ((255,   0,   0), "Red"),
    ((  0, 255,   0), "Green"),
    ((  0,   0, 255), "Blue"),
    ((255, 255, 255), "White"),
    ((  0,   0,   0), "Black"),

    # Row 2 – Secondary colors
    ((255, 255,   0), "Yellow"),
    ((  0, 255, 255), "Cyan"),
    ((255,   0, 255), "Magenta"),
    ((255, 165,   0), "Orange"),
    ((128,   0, 128), "Purple"),

    # Row 3 – Pastel / mixed colors
    ((255, 182, 193), "Pink"),
    ((135, 206, 235), "Sky Blue"),
    ((144, 238, 144), "Light Green"),
    ((255, 218, 185), "Peach"),
    ((221, 160, 221), "Plum"),

    # Row 4 – Earth tones
    ((139,  69,  19), "Brown"),
    ((210, 180, 140), "Tan"),
    ((128, 128, 128), "Gray"),
    (( 70, 130, 180), "Steel Blue"),
    (( 34, 139,  34), "Forest Green"),
]

COLUMNS = 5   # how many squares per row (rows are calculated automatically)


# ── Helper Functions ───────────────────────────────────────────────────────────

def draw_square(surface, color, x, y, size, label, font):
    """
    Draw one colored square with its name and RGB values underneath.

    Parameters:
        surface  – the window we draw on
        color    – (R, G, B) tuple
        x, y     – top-left corner of the square
        size     – width and height in pixels
        label    – the color's name (e.g. "Red")
        font     – the font used for labels
    """
    # The filled square
    pygame.draw.rect(surface, color, (x, y, size, size))

    # A thin dark border so white/light squares are still visible
    pygame.draw.rect(surface, DARK_GRAY, (x, y, size, size), 2)

    # Color name below the square
    name_surf = font.render(label, True, DARK_GRAY)
    name_rect = name_surf.get_rect(centerx=x + size // 2, top=y + size + 4)
    surface.blit(name_surf, name_rect)

    # RGB values in small text below the name
    r, g, b = color
    rgb_text  = f"({r}, {g}, {b})"
    rgb_surf  = font.render(rgb_text, True, DARK_GRAY)
    rgb_rect  = rgb_surf.get_rect(centerx=x + size // 2, top=name_rect.bottom + 1)
    surface.blit(rgb_surf, rgb_rect)


def draw_title(surface, font_large):
    """Print the title and a short instruction at the top."""
    title = font_large.render("RGB Color Explorer", True, DARK_GRAY)
    surface.blit(title, (MARGIN_LEFT, 14))

    hint_font = pygame.font.SysFont("monospace", 15)
    hint = hint_font.render(
        "Every color = Red (0–255)  +  Green (0–255)  +  Blue (0–255)",
        True, (100, 100, 100))
    surface.blit(hint, (MARGIN_LEFT, 48))


def draw_all_squares(surface, font):
    """
    Loop through every color in COLOR_DATA and draw it in a grid.

    We use the index (i) to calculate each square's row and column:
        column  =  i % COLUMNS        (remainder after dividing by number of columns)
        row     =  i // COLUMNS       (how many full rows have been completed)
    """
    for i, (color, name) in enumerate(COLOR_DATA):
        col = i % COLUMNS    # 0, 1, 2, 3, 4, 0, 1, 2, ...
        row = i // COLUMNS   # 0, 0, 0, 0, 0, 1, 1, 1, ...

        # Convert grid position to pixel position
        x = MARGIN_LEFT + col * (SQUARE_SIZE + GAP)
        y = MARGIN_TOP  + row * (SQUARE_SIZE + GAP + 30)  # +30 for label height

        draw_square(surface, color, x, y, SQUARE_SIZE, name, font)


# ── Main Function ──────────────────────────────────────────────────────────────

def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    clock      = pygame.time.Clock()
    font       = pygame.font.SysFont("monospace", 14)
    font_large = pygame.font.SysFont("monospace", 26, bold=True)

    running = True
    while running:

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Draw
        screen.fill(BACKGROUND)
        draw_title(screen, font_large)
        draw_all_squares(screen, font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()