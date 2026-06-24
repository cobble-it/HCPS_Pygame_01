# smiley_face.py
# Draws a smiling face using only simple Pygame geometric primitives.
# Great for learning how shapes combine to make something recognizable!
#
# Shapes used (6 total):
#   1. circle  – yellow head
#   2. circle  – left eye
#   3. circle  – right eye
#   4. arc     – smile
#   5. rect    – left eyebrow
#   6. rect    – right eyebrow

import pygame
import sys
import math   # needed for arc angles (math.pi)

# ── Constants ──────────────────────────────────────────────────────────────────

WINDOW_WIDTH  = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE  = "Smiley Face — Pygame Primitives Demo"

SKY_BLUE  = (135, 206, 235)
YELLOW    = (255, 220,   0)
BLACK     = (  0,   0,   0)
WHITE     = (255, 255, 255)
DARK_GRAY = ( 50,  50,  50)

# Face geometry — change these numbers to reshape the face!
FACE_CENTER_X = WINDOW_WIDTH  // 2   # 300
FACE_CENTER_Y = WINDOW_HEIGHT // 2   # 300
FACE_RADIUS   = 200

EYE_OFFSET_X  = 75    # how far each eye is from the center horizontally
EYE_OFFSET_Y  = 60    # how far each eye is above the center
EYE_RADIUS    = 28

EYEBROW_WIDTH  = 65
EYEBROW_HEIGHT = 12
EYEBROW_OFFSET_Y = 105   # how far above the center the eyebrows sit


# ── Drawing Functions ──────────────────────────────────────────────────────────

def draw_head(surface):
    """Shape 1: Big yellow filled circle for the head."""
    pygame.draw.circle(surface, YELLOW, (FACE_CENTER_X, FACE_CENTER_Y), FACE_RADIUS)
    # Outline — same circle, thickness=5, no fill (thickness > 0)
    pygame.draw.circle(surface, BLACK,  (FACE_CENTER_X, FACE_CENTER_Y), FACE_RADIUS, 5)


def draw_eyes(surface):
    """Shapes 2 & 3: Two black filled circles for the eyes."""
    left_eye_x  = FACE_CENTER_X - EYE_OFFSET_X
    right_eye_x = FACE_CENTER_X + EYE_OFFSET_X
    eye_y       = FACE_CENTER_Y - EYE_OFFSET_Y

    pygame.draw.circle(surface, BLACK, (left_eye_x,  eye_y), EYE_RADIUS)
    pygame.draw.circle(surface, BLACK, (right_eye_x, eye_y), EYE_RADIUS)

    # White glint on each eye — makes them look a little livelier
    glint_offset = EYE_RADIUS // 3
    pygame.draw.circle(surface, WHITE, (left_eye_x  - glint_offset, eye_y - glint_offset), 7)
    pygame.draw.circle(surface, WHITE, (right_eye_x - glint_offset, eye_y - glint_offset), 7)


def draw_eyebrows(surface):
    """
    Shapes 4 & 5: Two dark rectangles for eyebrows.
    A rect is defined as (x, y, width, height) where (x, y) is the TOP-LEFT corner.
    """
    eyebrow_y = FACE_CENTER_Y - EYEBROW_OFFSET_Y   # top edge of both eyebrows

    left_eyebrow_x  = FACE_CENTER_X - EYE_OFFSET_X - EYEBROW_WIDTH // 2
    right_eyebrow_x = FACE_CENTER_X + EYE_OFFSET_X - EYEBROW_WIDTH // 2

    pygame.draw.rect(surface, DARK_GRAY,
                     (left_eyebrow_x,  eyebrow_y, EYEBROW_WIDTH, EYEBROW_HEIGHT))
    pygame.draw.rect(surface, DARK_GRAY,
                     (right_eyebrow_x, eyebrow_y, EYEBROW_WIDTH, EYEBROW_HEIGHT))


def draw_smile(surface):
    """
    Shape 6: An arc drawn along the bottom of a bounding rectangle.

    pygame.draw.arc(surface, color, rect, start_angle, stop_angle, width)
      - Angles are in RADIANS, measured counter-clockwise from the right (3 o'clock)
      - math.pi      = 180°  (left / 9 o'clock)
      - math.pi * 2  = 360°  (full circle, back to 3 o'clock)
      - To get the BOTTOM half of an ellipse, sweep from math.pi to math.pi*2
        (but Pygame's y-axis is flipped, so this draws a smile, not a frown)
    """
    smile_width  = 240
    smile_height = 160
    smile_rect = (
        FACE_CENTER_X - smile_width  // 2,   # left edge
        FACE_CENTER_Y - smile_height // 4,   # top edge  (shifted up a little)
        smile_width,
        smile_height,
    )

    pygame.draw.arc(surface, BLACK, smile_rect,
                    math.pi,          # start: left side  (180°)
                    math.pi * 2,      # end:   right side (360°)
                    6)                # line thickness in pixels


def draw_label(surface, font):
    """Print a shape count at the bottom so students know what to look for."""
    msg = "6 shapes total: 3 circles  |  2 rects  |  1 arc"
    label = font.render(msg, True, DARK_GRAY)
    rect  = label.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 22))
    surface.blit(label, rect)


# ── Main Function ──────────────────────────────────────────────────────────────

def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()
    font  = pygame.font.SysFont("monospace", 18)

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
        screen.fill(SKY_BLUE)

        draw_head(screen)       # Shape 1      – circle (filled yellow)
        draw_eyes(screen)       # Shapes 2 & 3 – circles (filled black) + white glints
        draw_eyebrows(screen)   # Shapes 4 & 5 – rects
        draw_smile(screen)      # Shape 6      – arc

        draw_label(screen, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()