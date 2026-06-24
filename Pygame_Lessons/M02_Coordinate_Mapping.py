# coordinates_demo.py
# A beginner-friendly Pygame program that shows how the coordinate system works.
# Made for middle school students learning Python and game programming.
#
# KEY IDEA: In Pygame, (0, 0) is the TOP-LEFT corner of the window.
#   - X increases going RIGHT
#   - Y increases going DOWN  (opposite of math class!)

import pygame
import sys

# ── Constants ──────────────────────────────────────────────────────────────────
# Constants are values that never change while the program runs.
# Using ALL_CAPS is a common way to name them.

WINDOW_WIDTH  = 800   # How many pixels wide the window is
WINDOW_HEIGHT = 600   # How many pixels tall the window is
WINDOW_TITLE  = "Pygame Coordinate Explorer"

FRAMES_PER_SECOND = 60   # How fast the game loop runs

# Colors are stored as (Red, Green, Blue) tuples — each value is 0–255
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
DARK_GRAY  = ( 50,  50,  50)
LIGHT_GRAY = (200, 200, 200)
RED        = (220,  50,  50)
GREEN      = ( 50, 180,  80)
BLUE       = ( 60, 120, 220)
YELLOW     = (240, 200,   0)
ORANGE     = (230, 130,  30)
PURPLE     = (150,  60, 200)


# ── Helper Functions ────────────────────────────────────────────────────────────

def draw_grid(surface):
    """Draw a light grid so students can estimate coordinates by eye."""
    step = 50   # Draw a line every 50 pixels

    for x in range(0, WINDOW_WIDTH, step):
        pygame.draw.line(surface, LIGHT_GRAY, (x, 0), (x, WINDOW_HEIGHT), 1)

    for y in range(0, WINDOW_HEIGHT, step):
        pygame.draw.line(surface, LIGHT_GRAY, (0, y), (WINDOW_WIDTH, y), 1)


def draw_axes(surface):
    """Draw X and Y axis lines with arrows to show direction."""
    mid_x = WINDOW_WIDTH  // 2
    mid_y = WINDOW_HEIGHT // 2

    # Horizontal axis (X)
    pygame.draw.line(surface, DARK_GRAY, (0, mid_y), (WINDOW_WIDTH, mid_y), 2)
    # Vertical axis (Y)
    pygame.draw.line(surface, DARK_GRAY, (mid_x, 0), (mid_x, WINDOW_HEIGHT), 2)


def draw_labeled_point(surface, font, x, y, color, label):
    """
    Draw a filled circle at (x, y) and print the coordinates next to it.
    
    Parameters:
        surface  - the window we're drawing on
        font     - the font object used to render text
        x, y     - the pixel position of the point
        color    - the circle's color (R, G, B)
        label    - a short name shown above the coordinates
    """
    radius = 10
    pygame.draw.circle(surface, color, (x, y), radius)
    pygame.draw.circle(surface, BLACK, (x, y), radius, 2)   # thin black border

    # Build the text strings
    name_text   = font.render(label, True, color)
    coords_text = font.render(f"({x}, {y})", True, BLACK)

    # Place the label just above and to the right of the circle
    surface.blit(name_text,   (x + radius + 4, y - radius - 18))
    surface.blit(coords_text, (x + radius + 4, y - radius + 2))


def draw_mouse_tracker(surface, font, mouse_x, mouse_y):
    """Show a crosshair and live coordinates wherever the mouse is."""
    line_length = 12

    # Crosshair lines
    pygame.draw.line(surface, RED,
                     (mouse_x - line_length, mouse_y),
                     (mouse_x + line_length, mouse_y), 2)
    pygame.draw.line(surface, RED,
                     (mouse_x, mouse_y - line_length),
                     (mouse_x, mouse_y + line_length), 2)

    # Live coordinate readout near the mouse — offset so it doesn't cover the cursor
    offset_x = 15
    offset_y = -25

    # Keep the label inside the window
    label_x = mouse_x + offset_x
    label_y = mouse_y + offset_y
    label_x = max(0, min(label_x, WINDOW_WIDTH  - 120))
    label_y = max(0, min(label_y, WINDOW_HEIGHT -  30))

    coord_label = font.render(f"({mouse_x}, {mouse_y})", True, RED)
    surface.blit(coord_label, (label_x, label_y))


def draw_corner_labels(surface, font):
    """
    Label all four corners so students can see where (0,0) is
    and how coordinates grow across the screen.
    """
    margin = 6
    small = pygame.font.SysFont("monospace", 16)

    corners = [
        # (text,              x position,              y position)
        ("(0, 0)",            margin,                  margin),
        (f"({WINDOW_WIDTH}, 0)",      WINDOW_WIDTH  - 100,     margin),
        (f"(0, {WINDOW_HEIGHT})",     margin,                  WINDOW_HEIGHT - 22),
        (f"({WINDOW_WIDTH}, {WINDOW_HEIGHT})", WINDOW_WIDTH - 110, WINDOW_HEIGHT - 22),
    ]

    for text, cx, cy in corners:
        label = small.render(text, True, DARK_GRAY)
        surface.blit(label, (cx, cy))


def draw_legend(surface, font):
    """Draw a small legend box explaining what the colored dots mean."""
    box_x, box_y = 10, 200
    box_w, box_h = 220, 160
    padding = 10

    # Semi-transparent background (we draw a filled rect with a border)
    pygame.draw.rect(surface, (240, 240, 255), (box_x, box_y, box_w, box_h))
    pygame.draw.rect(surface, DARK_GRAY,       (box_x, box_y, box_w, box_h), 2)

    title = font.render("Example Points:", True, BLACK)
    surface.blit(title, (box_x + padding, box_y + padding))

    entries = [
        (RED,    "A – near top-left"),
        (GREEN,  "B – near top-right"),
        (BLUE,   "C – near center"),
        (ORANGE, "D – near bottom"),
        (PURPLE, "E – bottom-right"),
    ]

    small = pygame.font.SysFont("monospace", 15)
    for i, (color, desc) in enumerate(entries):
        row_y = box_y + padding + 26 + i * 24
        pygame.draw.circle(surface, color, (box_x + padding + 6, row_y + 8), 6)
        label = small.render(desc, True, BLACK)
        surface.blit(label, (box_x + padding + 18, row_y))


def draw_instructions(surface, font):
    """Print a short instruction line at the bottom of the screen."""
    msg = "Move your mouse — watch the red crosshair track your coordinates!"
    label = font.render(msg, True, DARK_GRAY)
    # Center it horizontally
    label_rect = label.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
    surface.blit(label, label_rect)


# ── Main Function ───────────────────────────────────────────────────────────────

def main():
    """
    Entry point for the program.
    Sets up Pygame, creates the window, and runs the game loop.
    """
    # 1. Initialize Pygame (always do this first!)
    pygame.init()

    # 2. Create the window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    # 3. Create a clock to control how fast the loop runs
    clock = pygame.time.Clock()

    # 4. Load fonts
    font       = pygame.font.SysFont("monospace", 18)
    font_large = pygame.font.SysFont("monospace", 22, bold=True)

    # 5. Define the example points we'll show on screen
    #    Each entry: (x, y, color, label)
    example_points = [
        (120,  80,  RED,    "A"),
        (660,  90,  GREEN,  "B"),
        (400,  300, BLUE,   "C"),
        (300,  480, ORANGE, "D"),
        (680,  510, PURPLE, "E"),
    ]

    # ── Game Loop ──────────────────────────────────────────────────────────────
    # This loop runs over and over — up to FRAMES_PER_SECOND times per second.
    # Each pass through the loop is called a "frame."

    running = True
    while running:

        # — Step A: Handle events (keyboard, mouse, window close, etc.) —
        for event in pygame.event.get():
            if event.type == pygame.QUIT:          # User clicked the X button
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:   # Press Escape to quit
                    running = False

        # — Step B: Get the current mouse position —
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # — Step C: Draw everything —

        # Clear the screen with a white background
        screen.fill(WHITE)

        # Grid and axes (drawn first so everything else appears on top)
        draw_grid(screen)
        draw_axes(screen)

        # Corner labels to show the coordinate extremes
        draw_corner_labels(screen, font)

        # The five example points
        for (px, py, color, label) in example_points:
            draw_labeled_point(screen, font, px, py, color, label)

        # Live mouse tracker
        draw_mouse_tracker(screen, font, mouse_x, mouse_y)

        # Legend and instructions
        draw_legend(screen, font)
        draw_instructions(screen, font)

        # Title at the top-center
        title_label = font_large.render(
            "Pygame Coordinate System  |  (0, 0) = TOP-LEFT", True, DARK_GRAY)
        title_rect = title_label.get_rect(center=(WINDOW_WIDTH // 2, 22))
        screen.fill(WHITE, (0, 0, WINDOW_WIDTH, 44))   # clear just the title area
        screen.blit(title_label, title_rect)

        # — Step D: Flip the display (show what we just drew) —
        pygame.display.flip()

        # — Step E: Wait just long enough to hit our target frame rate —
        clock.tick(FRAMES_PER_SECOND)

    # 6. Clean up and exit
    pygame.quit()
    sys.exit()


# ── Run the program ─────────────────────────────────────────────────────────────
# This block only runs when you execute THIS file directly.
# If another file imports this one, main() won't be called automatically.

if __name__ == "__main__":
    main()

# What's on screen

# A light gray grid with tick marks every 50 pixels so students can estimate positions by eye
# X and Y axis lines through the center
# Corner labels showing the four extreme coordinates — great for hammering home that (0, 0) is top-left, not bottom-left like in math class
# Five colored example points (A–E) with their coordinates labeled
# A live red crosshair that follows the mouse and shows real-time coordinates

# Code structure students can trace

# The file is organized into clear layers:

# Constants — colors, window size, frame rate (all in one place, easy to tweak)
# Helper functions — each does one job (draw_grid, draw_axes, draw_labeled_point, etc.)
# main() — the game loop with clearly labeled steps: handle events → read mouse → draw → flip → tick
# if __name__ == "__main__" — a gentle intro to that Python idiom

# Good "break it and learn" experiments for students

# Change WINDOW_WIDTH/WINDOW_HEIGHT and watch the corner labels update
# Move the coordinates in example_points to new locations and predict where the dot will appear before running it
# Change a color tuple and see what happens
# Change FRAMES_PER_SECOND to 5 and watch the mouse tracker feel sluggish