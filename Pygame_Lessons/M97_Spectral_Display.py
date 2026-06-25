"""
RGB Spectral Display
====================
Moves through all RGB color combinations in a spectral pattern.

Controls:
  SPACE       - Pause / Resume
  UP / DOWN   - Increase / Decrease animation speed
  S           - Toggle between display modes (full-screen vs. banded spectrum)
  R           - Reset to the beginning
  ESC / Q     - Quit
"""

import pygame
import colorsys
import sys

# ── Configuration ─────────────────────────────────────────────────────────────
WINDOW_W, WINDOW_H = 900, 600
FPS = 60
TITLE = "RGB Spectral Display"

# How fast hue advances per frame (0.0 – 1.0 range)
HUE_SPEED_DEFAULT = 0.0015
HUE_SPEED_STEP    = 0.0005
HUE_SPEED_MIN     = 0.0001
HUE_SPEED_MAX     = 0.02

# Number of vertical bands in BANDED mode
NUM_BANDS = 64
# ──────────────────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.RESIZABLE)
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 15)

    hue   = 0.0
    speed = HUE_SPEED_DEFAULT
    paused = False
    mode   = 0  # 0 = fullscreen, 1 = banded

    running = True
    while running:
        # ── Events ────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_UP:
                    speed = min(speed + HUE_SPEED_STEP, HUE_SPEED_MAX)
                elif event.key == pygame.K_DOWN:
                    speed = max(speed - HUE_SPEED_STEP, HUE_SPEED_MIN)
                elif event.key == pygame.K_s:
                    mode = 1 - mode          # toggle
                elif event.key == pygame.K_r:
                    hue = 0.0

        # ── Update ────────────────────────────────────────────────────────────
        if not paused:
            hue += speed
            if hue >= 1.0:
                hue -= 1.0          # wrap so we keep cycling forever

        # ── Draw ──────────────────────────────────────────────────────────────
        if mode == 0:
            draw_fullscreen_mode(screen, hue)
        else:
            draw_banded_mode(screen, hue)

        draw_hud(screen, font, hue, speed, paused, mode)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def hsv_to_rgb255(h, s, v):
    """Convert HSV (0-1 each) → (R, G, B) in 0-255."""
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


def draw_fullscreen_mode(surface, hue):
    """
    Full-screen mode: entire window filled with the current hue,
    plus a small live preview strip showing the upcoming hues.
    """
    w, h = surface.get_size()

    # Main color fill
    color = hsv_to_rgb255(hue % 1.0, 1.0, 1.0)
    surface.fill(color)

    # Preview strip at the bottom – shows the next 180° of the spectrum
    strip_h = 60
    strip_y = h - strip_h
    for x in range(w):
        preview_hue = (hue + x / w * 0.5) % 1.0
        pygame.draw.line(
            surface,
            hsv_to_rgb255(preview_hue, 1.0, 1.0),
            (x, strip_y),
            (x, h - 1),
        )

    # Thin white separator above the strip
    pygame.draw.line(surface, (255, 255, 255), (0, strip_y), (w, strip_y), 2)


def draw_banded_mode(surface, hue):
    """
    Banded mode: the screen is split into vertical columns, each showing a
    different saturation/value combination for the current hue family.
    The columns scroll rightward as hue advances.
    """
    w, h = surface.get_size()
    band_w = w // NUM_BANDS

    for i in range(NUM_BANDS):
        # Spread saturation across the top half, value across the bottom
        band_hue = (hue + i / NUM_BANDS) % 1.0

        # Top half: vary saturation (full value)
        for row in range(h // 2):
            sat = row / (h // 2)
            color = hsv_to_rgb255(band_hue, sat, 1.0)
            pygame.draw.rect(
                surface, color,
                (i * band_w, row, band_w, 1)
            )

        # Bottom half: vary value (full saturation)
        for row in range(h // 2):
            val = 1.0 - row / (h // 2)
            color = hsv_to_rgb255(band_hue, 1.0, val)
            pygame.draw.rect(
                surface, color,
                (i * band_w, h // 2 + row, band_w, 1)
            )

    # Horizontal divider
    pygame.draw.line(surface, (255, 255, 255), (0, h // 2), (w, h // 2), 2)


def draw_hud(surface, font, hue, speed, paused, mode):
    """Render a semi-transparent info overlay."""
    lines = [
        f"Hue: {hue % 1.0:.4f}  ({int((hue % 1.0) * 360)}°)",
        f"Speed: {speed:.4f}  (↑/↓ to adjust)",
        f"Mode: {'Full-screen' if mode == 0 else 'Banded spectrum'}  (S to switch)",
        "SPACE pause  |  R reset  |  ESC quit",
    ]
    if paused:
        lines.insert(0, "⏸  PAUSED")

    pad = 8
    line_h = font.get_linesize()
    box_h = len(lines) * line_h + pad * 2
    box_w = 380
    box_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    box_surf.fill((0, 0, 0, 140))
    surface.blit(box_surf, (10, 10))

    for i, line in enumerate(lines):
        text = font.render(line, True, (255, 255, 255))
        surface.blit(text, (10 + pad, 10 + pad + i * line_h))





# Run the driver logic is this script file is being directly called.
if __name__ == "__main__":
    main()