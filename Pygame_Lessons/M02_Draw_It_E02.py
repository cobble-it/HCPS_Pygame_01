# bob_ross.py
# A Bob Ross-inspired landscape scene drawn entirely with Pygame primitives.
# Layers painted back-to-front (sky → mountains → hills → ground → house → trees)
# so closer objects naturally sit on top of farther ones.
#
# Shapes used and where:
#   polygon  – sky gradient bands, mountains, hills, ground, roof, tree canopies
#   rect     – house body, door, windows, chimney, window panes
#   circle   – sun, clouds, round tree tops, chimney smoke
#   ellipse  – cloud puffs, distant tree blobs
#   line     – window cross-panes, fence rails
#   arc      – (not used here — saved for smiley demo!)

import pygame
import sys

# ── Constants ──────────────────────────────────────────────────────────────────

W, H = 900, 600
TITLE = "Happy Little House  —  Pygame Landscape Demo"
FPS   = 60

# ── Bob Ross Palette ───────────────────────────────────────────────────────────
# Warm, slightly desaturated — paint, not pixels.

SKY_TOP        = ( 95, 145, 210)   # deep cerulean high up
SKY_MID        = (160, 200, 235)   # lighter blue at horizon
SKY_HORIZON    = (220, 225, 200)   # warm haze where sky meets mountains

MOUNTAIN_FAR   = (130, 140, 165)   # cool blue-grey distant peaks
MOUNTAIN_SNOW  = (230, 235, 240)   # snow caps
MOUNTAIN_NEAR  = ( 90, 115,  90)   # darker green-grey nearer range
MOUNTAIN_SHAD  = ( 65,  85,  70)   # shadow sides of near mountains

HILL_BACK      = ( 85, 130,  75)   # rolling far hills
HILL_MID       = ( 70, 115,  60)   # slightly darker mid hills
GROUND_BASE    = ( 85, 110,  55)   # open meadow
GROUND_FORE    = ( 60,  90,  40)   # closest ground strip

TREE_DARK      = ( 30,  65,  35)   # deep evergreen shadow
TREE_MID       = ( 45,  90,  45)   # mid evergreen
TREE_LIGHT     = ( 70, 120,  55)   # lit side of evergreen

HOUSE_WALL     = (220, 195, 160)   # warm cream siding
HOUSE_SHADOW   = (185, 160, 125)   # shaded side of house
ROOF_COLOR     = (110,  65,  50)   # rusty barn red roof
CHIMNEY_COLOR  = (140, 100,  80)   # brick chimney
DOOR_COLOR     = ( 90,  60,  40)   # dark wood door
WINDOW_COLOR   = (200, 220, 240)   # glass — reflects sky
WINDOW_FRAME   = ( 70,  50,  35)   # dark wood frame
SMOKE_COLOR    = (210, 210, 205)   # soft white smoke

SUN_COLOR      = (255, 240, 160)   # warm golden sun
SUN_GLOW       = (255, 250, 210)   # inner glow

CLOUD_COLOR    = (245, 248, 252)   # bright white clouds
CLOUD_SHADOW   = (210, 220, 230)   # underside of clouds

FENCE_COLOR    = (200, 185, 155)   # weathered white fence

BLACK          = (  0,   0,   0)
WHITE          = (255, 255, 255)


# ── Sky ────────────────────────────────────────────────────────────────────────

def draw_sky(surf):
    """Sky as three horizontal polygon bands fading warm at the horizon."""
    # Band 1 – top deep blue
    pygame.draw.polygon(surf, SKY_TOP, [
        (0, 0), (W, 0), (W, H * 0.30), (0, H * 0.30)
    ])
    # Band 2 – lighter mid-sky
    pygame.draw.polygon(surf, SKY_MID, [
        (0, H * 0.28), (W, H * 0.28), (W, H * 0.45), (0, H * 0.45)
    ])
    # Band 3 – warm horizon haze
    pygame.draw.polygon(surf, SKY_HORIZON, [
        (0, H * 0.43), (W, H * 0.43), (W, H * 0.52), (0, H * 0.52)
    ])


def draw_sun(surf):
    """Soft golden sun in the upper-right sky."""
    cx, cy = int(W * 0.82), int(H * 0.14)
    pygame.draw.circle(surf, SUN_GLOW,  (cx, cy), 46)
    pygame.draw.circle(surf, SUN_COLOR, (cx, cy), 34)


def draw_clouds(surf):
    """A few fluffy clouds built from overlapping ellipses and circles."""
    clouds = [
        # (center_x, center_y, scale)
        (int(W * 0.18), int(H * 0.12), 1.0),
        (int(W * 0.45), int(H * 0.08), 0.75),
    ]
    for cx, cy, s in clouds:
        puffs = [
            ( 0,   0, 38), (-40,  12, 28), ( 40,  12, 28),
            (-20, -14, 24), ( 20, -14, 24),
        ]
        # Shadow underside first
        for dx, dy, r in puffs:
            rx, ry = int(r * s * 1.6), int(r * s * 0.7)
            pygame.draw.ellipse(surf, CLOUD_SHADOW,
                                (cx + int(dx*s) - rx,
                                 cy + int(dy*s) + int(6*s) - ry,
                                 rx*2, ry*2))
        # Bright tops
        for dx, dy, r in puffs:
            pygame.draw.circle(surf, CLOUD_COLOR,
                               (cx + int(dx*s), cy + int(dy*s)),
                               int(r * s))


# ── Mountains ─────────────────────────────────────────────────────────────────

def draw_far_mountains(surf):
    """Distant cool blue-grey peaks — simple triangular polygons."""
    peaks = [
        # lit face                                    shadow face
        [(  0, 310),(160, 160),(260, 310)],           [(160,160),(260,310),(320,310),(220,200)],
        [(180, 310),(340, 140),(460, 310)],           [(340,140),(460,310),(500,310),(390,170)],
        [(370, 310),(530, 170),(640, 310)],           [(530,170),(640,310),(680,310),(570,190)],
        [(580, 310),(730, 155),(840, 310)],           [(730,155),(840,310),(880,310),(760,175)],
        [(760, 310),(900,  175),(900, 310)],
    ]
    for i, pts in enumerate(peaks):
        color = MOUNTAIN_FAR if i % 2 == 0 else MOUNTAIN_SHAD
        pygame.draw.polygon(surf, color, pts)

    # Snow caps
    snow_caps = [
        [(140,185),(160,160),(180,185)],
        [(325,165),(340,140),(360,165)],
        [(515,195),(530,170),(550,195)],
        [(715,178),(730,155),(748,178)],
    ]
    for cap in snow_caps:
        pygame.draw.polygon(surf, MOUNTAIN_SNOW, cap)


def draw_near_mountains(surf):
    """Closer forested mountain range — greener, more detail on slopes."""
    # Main silhouette
    pygame.draw.polygon(surf, MOUNTAIN_NEAR, [
        (  0, 340),(  0, 600),
        (120, 270),(200, 300),(280, 245),(380, 290),
        (460, 240),(540, 280),(620, 235),(700, 265),
        (780, 230),(860, 260),(900, 240),(900, 600),
    ])
    # Shadow sides
    shadow_patches = [
        [(120,270),(180,310),(200,300)],
        [(280,245),(360,290),(380,290),(330,265)],
        [(460,240),(540,280),(510,255)],
        [(620,235),(700,265),(660,248)],
        [(780,230),(840,260),(860,260),(820,245)],
    ]
    for patch in shadow_patches:
        pygame.draw.polygon(surf, MOUNTAIN_SHAD, patch)


# ── Rolling Hills & Ground ────────────────────────────────────────────────────

def draw_hills(surf):
    """Gentle rolling hills between mountains and foreground."""
    # Back hill band
    pygame.draw.polygon(surf, HILL_BACK, [
        (  0, 380),(  0, 600),
        (100, 355),(200, 370),(320, 345),(440, 365),
        (560, 348),(680, 362),(800, 350),(900, 360),(900, 600),
    ])
    # Mid hill band
    pygame.draw.polygon(surf, HILL_MID, [
        (  0, 420),(  0, 600),
        ( 80, 400),(200, 415),(350, 395),(500, 410),
        (650, 398),(800, 408),(900, 400),(900, 600),
    ])


def draw_ground(surf):
    """Flat meadow foreground — two strips for depth."""
    pygame.draw.polygon(surf, GROUND_BASE, [
        (0, 440),(W, 440),(W, 600),(0, 600)
    ])
    pygame.draw.polygon(surf, GROUND_FORE, [
        (0, 530),(W, 530),(W, 600),(0, 600)
    ])


# ── House ─────────────────────────────────────────────────────────────────────

def draw_house(surf):
    """
    A cozy cottage: body, shaded side wall, roof (polygon), chimney, door, windows.
    The house sits centered in the lower-middle of the scene.
    """
    # ── Anchor point ──
    hx, hy = 380, 340    # top-left corner of the main front wall
    hw, hh = 200, 155    # width and height of the front wall

    # Front wall
    pygame.draw.rect(surf, HOUSE_WALL, (hx, hy, hw, hh))

    # Shaded right side wall (gives 3-D feel)
    side_w = 55
    pygame.draw.polygon(surf, HOUSE_SHADOW, [
        (hx + hw,      hy),
        (hx + hw + side_w, hy + 30),
        (hx + hw + side_w, hy + hh + 30),
        (hx + hw,      hy + hh),
    ])

    # Roof — a pentagon that spans both the front and side
    roof_peak_x = hx + hw // 2
    roof_peak_y = hy - 90
    pygame.draw.polygon(surf, ROOF_COLOR, [
        (hx - 12,              hy),               # front left eave
        (hx + hw + side_w + 8, hy + 30),          # side right eave
        (hx + hw + side_w//2,  roof_peak_y + 18), # side peak
        (roof_peak_x,          roof_peak_y),       # front peak
        (hx - 12,              hy),
    ])
    # Roof underside / fascia strip
    pygame.draw.polygon(surf, ROOF_COLOR, [
        (hx - 12, hy),
        (hx + hw + 8, hy),
        (roof_peak_x + side_w//2 + 4, roof_peak_y + 18),
        (roof_peak_x, roof_peak_y),
    ])

    # Chimney (drawn after roof so it pokes through)
    cx = hx + int(hw * 0.72)
    pygame.draw.rect(surf, CHIMNEY_COLOR, (cx, roof_peak_y - 20, 28, 70))
    pygame.draw.rect(surf, (100, 70, 55),  (cx - 3, roof_peak_y - 25, 34, 10))  # cap

    # Smoke puffs from chimney
    smoke_x = cx + 14
    for i, (sy, sr, alpha) in enumerate([(roof_peak_y - 40, 10, 180),
                                          (roof_peak_y - 62, 13, 130),
                                          (roof_peak_y - 84, 16,  80)]):
        pygame.draw.circle(surf, SMOKE_COLOR, (smoke_x + i*4, sy), sr)

    # Door (centered on front wall, sitting on ground)
    door_w, door_h = 38, 60
    door_x = hx + (hw - door_w) // 2
    door_y = hy + hh - door_h
    pygame.draw.rect(surf, DOOR_COLOR, (door_x, door_y, door_w, door_h))
    # Door arch top (small ellipse upper half)
    pygame.draw.ellipse(surf, DOOR_COLOR,
                        (door_x, door_y - 14, door_w, 28))
    # Door knob
    pygame.draw.circle(surf, (180, 150, 80), (door_x + door_w - 8, door_y + 32), 4)

    # Left window
    _draw_window(surf, hx + 22, hy + 30, 50, 44)
    # Right window
    _draw_window(surf, hx + hw - 72, hy + 30, 50, 44)


def _draw_window(surf, wx, wy, ww, wh):
    """Helper — draws a single framed window with cross panes."""
    # Frame
    pygame.draw.rect(surf, WINDOW_FRAME, (wx - 4, wy - 4, ww + 8, wh + 8))
    # Glass
    pygame.draw.rect(surf, WINDOW_COLOR, (wx, wy, ww, wh))
    # Cross panes
    mid_x = wx + ww // 2
    mid_y = wy + wh // 2
    pygame.draw.line(surf, WINDOW_FRAME, (mid_x, wy), (mid_x, wy + wh), 2)
    pygame.draw.line(surf, WINDOW_FRAME, (wx, mid_y), (wx + ww, mid_y), 2)
    # Subtle sky reflection
    pygame.draw.rect(surf, (215, 230, 248), (wx + 2, wy + 2, ww // 2 - 2, wh // 2 - 2))


# ── Trees ─────────────────────────────────────────────────────────────────────

def draw_evergreen(surf, tx, ty, height, width):
    """
    A classic Bob Ross happy little tree — three stacked triangles
    getting narrower toward the top, with a trunk.
    """
    trunk_h = int(height * 0.18)
    # Trunk
    pygame.draw.rect(surf, (80, 55, 35),
                     (tx - 5, ty - trunk_h, 10, trunk_h))

    # Three triangle tiers (bottom to top, getting narrower)
    tiers = [
        (int(width * 1.0), int(height * 0.45), ty - trunk_h),
        (int(width * 0.70), int(height * 0.38), ty - trunk_h - int(height * 0.30)),
        (int(width * 0.45), int(height * 0.30), ty - trunk_h - int(height * 0.55)),
    ]
    for i, (tw, th, base_y) in enumerate(tiers):
        # Shadow side (slightly darker)
        pygame.draw.polygon(surf, TREE_DARK, [
            (tx, base_y - th), (tx, base_y), (tx + tw // 2, base_y)
        ])
        # Lit side
        pygame.draw.polygon(surf, TREE_MID, [
            (tx, base_y - th), (tx - tw // 2, base_y), (tx, base_y)
        ])
        # Highlight edge
        pygame.draw.polygon(surf, TREE_LIGHT, [
            (tx, base_y - th), (tx - tw // 2, base_y), (tx - tw // 3, base_y - th // 3)
        ])


def draw_trees(surf):
    """Place evergreens framing the house on both sides."""
    # Left cluster
    draw_evergreen(surf, 270, 490, 130, 60)
    draw_evergreen(surf, 310, 500, 110, 50)
    draw_evergreen(surf, 235, 500, 100, 45)

    # Right cluster
    draw_evergreen(surf, 630, 485, 140, 65)
    draw_evergreen(surf, 670, 495, 115, 52)
    draw_evergreen(surf, 595, 498, 105, 48)

    # A lone smaller tree far left for depth
    draw_evergreen(surf, 130, 450, 80, 38)
    draw_evergreen(surf, 790, 455, 85, 40)


# ── Fence ─────────────────────────────────────────────────────────────────────

def draw_fence(surf):
    """A simple picket fence across the foreground."""
    fence_y  = 510    # top of fence
    post_h   = 45
    post_w   = 8
    spacing  = 28
    start_x  = 160
    end_x    = 740

    # Two horizontal rails
    pygame.draw.line(surf, FENCE_COLOR, (start_x, fence_y + 12),  (end_x, fence_y + 12),  4)
    pygame.draw.line(surf, FENCE_COLOR, (start_x, fence_y + 30),  (end_x, fence_y + 30),  4)

    # Vertical pickets with pointed tops
    for x in range(start_x, end_x, spacing):
        # Picket body
        pygame.draw.rect(surf, FENCE_COLOR, (x, fence_y, post_w, post_h))
        # Pointed cap (small triangle)
        pygame.draw.polygon(surf, FENCE_COLOR, [
            (x,              fence_y),
            (x + post_w,     fence_y),
            (x + post_w // 2, fence_y - 10),
        ])


# ── Foreground grass detail ────────────────────────────────────────────────────

def draw_grass_details(surf):
    """Thin dark lines suggesting blades of grass in the foreground."""
    import random
    random.seed(42)   # fixed seed so the grass looks the same every frame
    for _ in range(120):
        gx = random.randint(0, W)
        gy = random.randint(535, 595)
        gh = random.randint(5, 14)
        lean = random.randint(-4, 4)
        pygame.draw.line(surf, TREE_DARK, (gx, gy), (gx + lean, gy - gh), 1)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption(TITLE)
    clock  = pygame.time.Clock()
    font   = pygame.font.SysFont("serif", 20, italic=True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Paint back to front — just like Bob does!
        draw_sky(screen)             # 1. Sky bands
        draw_sun(screen)             # 2. Sun
        draw_clouds(screen)          # 3. Clouds
        draw_far_mountains(screen)   # 4. Distant peaks
        draw_near_mountains(screen)  # 5. Near forested range
        draw_hills(screen)           # 6. Rolling hills
        draw_ground(screen)          # 7. Meadow ground
        draw_house(screen)           # 8. The house
        draw_trees(screen)           # 9. Framing evergreens
        draw_fence(screen)           # 10. Picket fence
        draw_grass_details(screen)   # 11. Foreground grass

        # Signature
        sig = font.render("Happy little trees.  —  Bob Ross  (Pygame edition)", True, (80, 60, 40))
        screen.blit(sig, (W // 2 - sig.get_width() // 2, H - 26))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()