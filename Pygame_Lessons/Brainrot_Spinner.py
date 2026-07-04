"""
Brainrot Case Opener — CS:GO-style case spinner.

Sound files (optional, place next to this script):
  tick.wav — click sound as items scroll past
  win.wav  — fanfare when the reel stops

Image files (optional, place next to this script):
  Match the "image" key in ITEM_POOL. Missing images show a colored placeholder.
"""

import math, os, random, sys, time
import pygame

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WIN_W, WIN_H = 900, 600
FPS          = 60

CARD_W, CARD_H = 160, 120
CARD_GAP       = 4
STRIP_Y        = WIN_H // 2 - CARD_H // 2 - 20
STRIP_START_X  = WIN_W // 2 - 4 * CARD_W   # keeps 7 cards visible
CENTER_X       = WIN_W // 2

IMG_SIZE = (80, 80)

# Spin feel
PRE_WINNER_CARDS  = (30, 40)   # random range of filler cards before winner
POST_WINNER_CARDS = 3
SPIN_DURATION     = (5.5, 7.5) # seconds
LAND_JITTER       = CARD_W // 3

# Colors
C_BG_DARK  = (13,  17,  23)
C_BG_MID   = (22,  28,  38)
C_GOLD     = (201, 164, 95)
C_GOLD_HI  = (255, 215, 120)
C_WHITE    = (230, 235, 245)
C_GRAY     = (150, 160, 175)
C_SUBTLE   = (70,  80,  100)
C_LINE     = (255, 215, 0)

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

RARITIES = [
    {"name": "Common",    "color": (100, 150, 255), "chance": 0.7992},
    {"name": "Uncommon",  "color": (160,  50, 255), "chance": 0.1598},
    {"name": "Rare",      "color": (220,  50, 180), "chance": 0.0320},
    {"name": "Epic",      "color": (220,  50,  47), "chance": 0.0064},
    {"name": "LEGENDARY", "color": (255, 185,   0), "chance": 0.0026},
]

ITEM_POOL = [
    # Common
    {"name": "Bombardiro",      "rarity": 0, "image": "bombardiro.png"},
    {"name": "Tralalero",       "rarity": 0, "image": "tralalero.png"},
    {"name": "Cappuccino",      "rarity": 0, "image": "cappuccino.png"},
    {"name": "Bombombini",      "rarity": 0, "image": "bombombini.png"},
    {"name": "Lirilì Larilà",  "rarity": 0, "image": "lirili.png"},
    # Uncommon
    {"name": "Tung Tung Sahur", "rarity": 1, "image": "tungtung.png"},
    {"name": "Frigo Camelo",    "rarity": 1, "image": "frigocamelo.png"},
    {"name": "Burbaloni",       "rarity": 1, "image": "burbaloni.png"},
    # Rare
    {"name": "Glorbo Fruttolli","rarity": 2, "image": "glorbo.png"},
    {"name": "Trippi Troppi",   "rarity": 2, "image": "trippi.png"},
    # Epic
    {"name": "Brrr Brrr Patapim","rarity": 3, "image": "patapim.png"},
    {"name": "La Vaca Saturno", "rarity": 3, "image": "lavaca.png"},
    # Legendary
    {"name": "* Bombardiro Crocodilo", "rarity": 4, "image": "bombardiro_croc.png"},
    {"name": "* Tung Tung Sahur",     "rarity": 4, "image": "tungtung_gold.png"},
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_sounds():
    sounds = {"tick": None, "win": None}
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        here = os.path.dirname(os.path.abspath(__file__))
        for key, fname in (("tick", "img/tick.wav"), ("win", "img/win.wav")):
            path = os.path.join(here, fname)
            if os.path.isfile(path):
                sounds[key] = pygame.mixer.Sound(path)
            else:
                print(f"[Audio] '{fname}' not found — place it next to the script to enable.")
    except pygame.error as e:
        print(f"[Audio] Could not init mixer: {e}")
    return sounds


def load_images():
    here = os.path.dirname(os.path.abspath(__file__))
    cache = {}
    for item in ITEM_POOL:
        fname =  item.get("image")
        if not fname or fname in cache:
            continue
        path = os.path.join(here, "img", fname)
        if os.path.isfile(path):
            try:
                print(f"[Images] Loading '{fname}'...")
                cache[fname] = pygame.transform.smoothscale(
                    pygame.image.load(path).convert_alpha(), IMG_SIZE
                )
            except pygame.error as e:
                print(f"[Images] Could not load '{fname}': {e}")
                cache[fname] = None
        else:
            print(f"[Images] '{fname}' not found — placeholder will be used.")
            cache[fname] = None
    return cache


def pick_winner():
    roll, cumulative = random.random(), 0.0
    chosen_rarity = 0
    for i, r in enumerate(RARITIES):
        cumulative += r["chance"]
        if roll < cumulative:
            chosen_rarity = i
            break
    return random.choice([x for x in ITEM_POOL if x["rarity"] == chosen_rarity])


def build_strip(winner):
    n = random.randint(*PRE_WINNER_CARDS)
    pre  = [random.choice(ITEM_POOL) for _ in range(n)]
    post = [random.choice(ITEM_POOL) for _ in range(POST_WINNER_CARDS)]
    return pre + [winner] + post


def ease_out(t):
    return 1.0 - (1.0 - t) ** 4


def rrect(surf, color, rect, r=8, bw=0, bc=None):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if bw and bc:
        pygame.draw.rect(surf, bc, rect, bw, border_radius=r)


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

def draw_card(surf, item, images, fonts, x, y, highlighted=False):
    rarity  = RARITIES[item["rarity"]]
    color   = rarity["color"]
    bg      = tuple(max(0, c - 160) for c in color)
    border  = color if highlighted else tuple(max(0, c - 80) for c in color)
    rect    = pygame.Rect(x, y, CARD_W - CARD_GAP, CARD_H)

    rrect(surf, bg, rect, bw=3 if highlighted else 2, bc=border)
    rrect(surf, color, pygame.Rect(x + 3, y + 3, CARD_W - CARD_GAP - 6, 5), r=3)

    # Image or placeholder
    img = images.get(item.get("image"))
    if img:
        surf.blit(img, (x + (CARD_W - CARD_GAP) // 2 - IMG_SIZE[0] // 2, y + 14))
    else:
        ph = pygame.Rect(x + (CARD_W - CARD_GAP) // 2 - 30, y + 14, 60, 60)
        rrect(surf, color, ph, r=6)
        q = fonts["sm"].render("?", True, C_WHITE)
        surf.blit(q, (ph.centerx - q.get_width() // 2, ph.centery - q.get_height() // 2))

    # Name (two lines)
    parts = item["name"].split(" ", 1)
    l1 = fonts["sm"].render(parts[0][:14], True, C_WHITE)
    surf.blit(l1, (x + (CARD_W - CARD_GAP) // 2 - l1.get_width() // 2, y + CARD_H - 38))
    if len(parts) > 1:
        tint = tuple(min(255, c + 80) for c in color)
        l2 = fonts["sm"].render(parts[1][:14], True, tint)
        surf.blit(l2, (x + (CARD_W - CARD_GAP) // 2 - l2.get_width() // 2, y + CARD_H - 22))

    if highlighted:
        glow = pygame.Surface((CARD_W + 16, CARD_H + 16), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*color, 40), glow.get_rect(), border_radius=12)
        surf.blit(glow, (x - 8, y - 8))


def draw_strip(surf, strip, scroll_x, images, fonts, phase):
    bg_rect = pygame.Rect(0, STRIP_Y - 12, WIN_W, CARD_H + 24)
    pygame.draw.rect(surf, C_BG_MID, bg_rect)
    pygame.draw.rect(surf, (40, 50, 70), bg_rect, 2)

    surf.set_clip(bg_rect)
    first = max(0, int(scroll_x // CARD_W) - 1)
    for i in range(first, min(len(strip), first + 11)):
        cx = STRIP_START_X + i * CARD_W - int(scroll_x)
        if cx + CARD_W < 0 or cx > WIN_W:
            continue
        dist = abs((cx + CARD_W // 2) - CENTER_X)
        draw_card(surf, strip[i], images, fonts, cx, STRIP_Y,
                  highlighted=(phase == "result" and dist < CARD_W // 3))
    surf.set_clip(None)

    # Edge fades
    for right in (False, True):
        fade = pygame.Surface((130, CARD_H + 24), pygame.SRCALPHA)
        for fx in range(130):
            a = int(220 * (fx / 130 if right else 1 - fx / 130))
            pygame.draw.line(fade, (*C_BG_DARK, a), (fx, 0), (fx, CARD_H + 24))
        surf.blit(fade, (WIN_W - 130 if right else 0, STRIP_Y - 12))


def draw_idle_strip(surf, fonts):
    """Draw the strip filled with mystery question-mark cards before any spin."""
    bg_rect = pygame.Rect(0, STRIP_Y - 12, WIN_W, CARD_H + 24)
    pygame.draw.rect(surf, C_BG_MID, bg_rect)
    pygame.draw.rect(surf, (40, 50, 70), bg_rect, 2)

    surf.set_clip(bg_rect)
    num_cards = WIN_W // CARD_W + 2
    for i in range(num_cards):
        x = STRIP_START_X + i * CARD_W
        rect = pygame.Rect(x, STRIP_Y, CARD_W - CARD_GAP, CARD_H)
        rrect(surf, (25, 32, 48), rect, bw=2, bc=(50, 65, 95))
        # Rarity stripe — neutral gray
        rrect(surf, (55, 65, 85), pygame.Rect(x + 3, STRIP_Y + 3, CARD_W - CARD_GAP - 6, 5), r=3)
        # Big question mark
        q = fonts["lg"].render("?", True, (60, 75, 110))
        surf.blit(q, (x + (CARD_W - CARD_GAP) // 2 - q.get_width() // 2,
                      STRIP_Y + CARD_H // 2 - q.get_height() // 2 - 4))
    surf.set_clip(None)

    # Edge fades
    for right in (False, True):
        fade = pygame.Surface((130, CARD_H + 24), pygame.SRCALPHA)
        for fx in range(130):
            a = int(220 * (fx / 130 if right else 1 - fx / 130))
            pygame.draw.line(fade, (*C_BG_DARK, a), (fx, 0), (fx, CARD_H + 24))
        surf.blit(fade, (WIN_W - 130 if right else 0, STRIP_Y - 12))


def draw_center_line(surf):
    top, bot = STRIP_Y - 20, STRIP_Y + CARD_H + 20
    pygame.draw.line(surf, C_LINE, (CENTER_X, top), (CENTER_X, bot), 3)
    pygame.draw.polygon(surf, C_LINE, [(CENTER_X-10, top-2), (CENTER_X+10, top-2), (CENTER_X, top+12)])
    pygame.draw.polygon(surf, C_LINE, [(CENTER_X-10, bot+2), (CENTER_X+10, bot+2), (CENTER_X, bot-12)])


def draw_result_popup(surf, winner, images, fonts, alpha):
    rarity, color = RARITIES[winner["rarity"]], RARITIES[winner["rarity"]]["color"]
    pw, ph = 440, 280
    px, py = WIN_W // 2 - pw // 2, WIN_H // 2 - ph // 2

    panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
    panel.set_alpha(alpha)
    pygame.draw.rect(panel, (18, 22, 32, 240), panel.get_rect(), border_radius=16)
    pygame.draw.rect(panel, color, panel.get_rect(), 3, border_radius=16)
    surf.blit(panel, (px, py))

    if alpha < 255:
        return

    def blit_centered(text_surf, rel_y):
        surf.blit(text_surf, (WIN_W // 2 - text_surf.get_width() // 2, py + rel_y))

    blit_centered(fonts["lg"].render("YOU GOT", True, C_GOLD), 20)

    img = images.get(winner.get("image"))
    if img:
        surf.blit(img, (WIN_W // 2 - IMG_SIZE[0] // 2, py + 65))
    else:
        ph_r = pygame.Rect(WIN_W // 2 - 40, py + 65, 80, 80)
        rrect(surf, color, ph_r, r=8)

    blit_centered(fonts["md"].render(winner["name"], True, color), 158)
    blit_centered(fonts["md"].render(rarity["name"], True, tuple(min(255, c+80) for c in color)), 192)
    blit_centered(fonts["md"].render("[ SPACE ] to open another", True, C_GRAY), 236)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Brainrot Case Opener")
    clock  = pygame.time.Clock()

    fonts = {
        "lg": pygame.font.SysFont("consolas", 32, bold=True),
        "md": pygame.font.SysFont("consolas", 20, bold=True),
        "sm": pygame.font.SysFont("consolas", 14),
    }
    sounds = load_sounds()
    images = load_images()

    stars = [(random.randint(0, WIN_W), random.randint(0, WIN_H // 2 - 80),
              random.uniform(0.3, 1.2)) for _ in range(80)]
    btn   = pygame.Rect(WIN_W // 2 - 100, WIN_H - 88, 200, 44)

    # Game state
    phase        = "idle"
    strip        = []
    winner       = None
    scroll_x     = 0.0
    scroll_target= 0.0
    spin_start   = 0.0
    spin_dur     = 0.0
    popup_alpha  = 0
    last_tick_x  = 0.0
    total_opens  = 0

    def begin_spin():
        nonlocal phase, strip, winner, scroll_x, scroll_target
        nonlocal spin_start, spin_dur, popup_alpha, last_tick_x, total_opens

        winner        = pick_winner()
        strip         = build_strip(winner)
        winner_idx    = len(strip) - POST_WINNER_CARDS - 1
        winner_cx     = STRIP_START_X + winner_idx * CARD_W + CARD_W // 2
        scroll_target = winner_cx - CENTER_X + random.randint(-LAND_JITTER, LAND_JITTER)
        scroll_x      = 0.0
        spin_start    = time.time()
        spin_dur      = random.uniform(*SPIN_DURATION)
        popup_alpha   = 0
        last_tick_x   = 0.0
        total_opens  += 1
        phase         = "spinning"

    running = True
    while running:
        clock.tick(FPS)
        now = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE and phase in ("idle", "result"):
                    begin_spin()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn.collidepoint(event.pos) and phase in ("idle", "result"):
                    begin_spin()

        # Update
        if phase == "spinning":
            t        = min((now - spin_start) / spin_dur, 1.0)
            scroll_x = scroll_target * ease_out(t)

            if int(scroll_x // CARD_W) != int(last_tick_x // CARD_W):
                if sounds["tick"]:
                    sounds["tick"].set_volume(max(0.05, 1.0 - t))
                    sounds["tick"].play()
            last_tick_x = scroll_x

            if t >= 1.0:
                phase = "result"
                if sounds["win"]:
                    sounds["win"].set_volume(0.7)
                    sounds["win"].play()

        if phase == "result":
            popup_alpha = min(255, popup_alpha + 8)

        # Draw background
        screen.fill(C_BG_DARK)
        grad = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
        for sy in range(WIN_H):
            pygame.draw.line(grad, (30, 60, 120, int(40 * (1 - sy / WIN_H))), (0, sy), (WIN_W, sy))
        screen.blit(grad, (0, 0))

        for sx, sy, sp in stars:
            b = int(120 + 80 * math.sin(now * sp + sx))
            pygame.draw.circle(screen, (b, b, b), (sx, sy), int(sp))

        # Title & counter
        title = fonts["lg"].render("BRAINROT CASE OPENER", True, C_GOLD)
        screen.blit(title, (WIN_W // 2 - title.get_width() // 2, 18))
        counter = fonts["sm"].render(f"Cases opened: {total_opens}", True, C_GRAY)
        screen.blit(counter, (20, 20))

        # Strip, line, button
        if phase == "idle":
            draw_idle_strip(screen, fonts)
        elif strip:
            draw_strip(screen, strip, scroll_x, images, fonts, phase)
        draw_center_line(screen)

        # Rarity legend — centered, just below the strip
        legend_y = STRIP_Y + CARD_H + 30
        total_legend_w = len(RARITIES) * 130 - 16
        legend_x = WIN_W // 2 - total_legend_w // 2
        for i, r in enumerate(RARITIES):
            sx = legend_x + i * 130
            pygame.draw.rect(screen, r["color"], (sx, legend_y, 14, 14), border_radius=3)
            screen.blit(fonts["sm"].render(r["name"], True, r["color"]), (sx + 18, legend_y))

        # Open button — centered, below the legend
        hovered   = btn.collidepoint(pygame.mouse.get_pos())
        btn_color = C_GOLD_HI if hovered else C_GOLD
        rrect(screen, (40, 35, 15) if hovered else (28, 24, 10), btn, r=10, bw=2, bc=btn_color)
        label = fonts["md"].render("OPEN CASE" if phase in ("idle","result") else "SPINNING...", True, btn_color)
        screen.blit(label, (btn.centerx - label.get_width() // 2, btn.centery - label.get_height() // 2))

        if phase == "result" and winner:
            draw_result_popup(screen, winner, images, fonts, popup_alpha)

        # Hint — pinned to very bottom
        hint = fonts["sm"].render("SPACE or click to open  •  ESC to quit", True, C_SUBTLE)
        screen.blit(hint, (WIN_W // 2 - hint.get_width() // 2, WIN_H - 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()