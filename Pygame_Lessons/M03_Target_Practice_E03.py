# target_shooter.py
# A target shooting game. Click on the target to score points.
# The target starts moving from level 2 and gets faster each level.
#
# Controls:  left-click to shoot  |  R to restart  |  Esc to quit

import pygame
import math
import random
import sys

# ---------------------------------------------------------------------------
# SETTINGS  -- change any of these numbers to tweak how the game feels
# ---------------------------------------------------------------------------

SCREEN_WIDTH    = 900
SCREEN_HEIGHT   = 650
FRAMES_PER_SEC  = 60
SHOTS_PER_LEVEL = 5
TOTAL_LEVELS    = 5

# ---------------------------------------------------------------------------
# COLORS  -- every color used in the game, as (Red, Green, Blue) tuples
# ---------------------------------------------------------------------------

NAVY          = (18,  22,  32)    # main background and dot grid
DARK_PANEL    = (28,  34,  48)    # top HUD bar and outer black ring
GOLD          = (255, 200,  50)   # titles and highlights
DIM_GRAY      = (80,  90, 110)    # muted text and grade C color
BRIGHT_GREEN  = (100, 255, 160)   # hit feedback color
BRIGHT_RED    = (255,  80,  80)   # miss feedback color
RING_RED      = (220,  30,  30)   # bullseye and inner red rings
RING_WHITE    = (240, 240, 240)   # white rings
DARK_GRAY     = (65,  65,  65)    # ring borders and crosshair lines
LIGHT_TEXT    = (220, 225, 240)   # all general light text in the HUD
LIGHT_BLUE    = (100, 180, 255)   # prompts and grade B color
OVERLAY_BLACK = (0,   0,   0, 185)  # summary backdrop -- fourth value is transparency (0=clear, 255=solid)

# ---------------------------------------------------------------------------
# TARGET RINGS  -- listed from the smallest (bullseye) to the largest
#
# Each row:  ( radius in pixels,  fill color,   points it scores,  name )
# ---------------------------------------------------------------------------

TARGET_RINGS = [
    ( 18,  RING_RED,    100,  "Bullseye!"  ),
    ( 36,  RING_RED,     80,  "Inner Red"  ),
    ( 60,  RING_WHITE,   60,  "White Ring" ),
    ( 90,  RING_WHITE,   40,  "White Ring" ),
    (126,  DARK_PANEL,   20,  "Black Ring" ),
    (155,  NAVY,          5,  "Near Miss"  ),  # invisible buffer ring
]
# A click beyond all rings scores 0 and is labelled "Miss!"

# The radius of the outermost VISIBLE ring -- used for spacing and bounce math
OUTER_RING_RADIUS = TARGET_RINGS[-2][0]   # -2 skips the invisible near-miss ring

# How close to the edge the target centre is kept so the full target stays on screen
TARGET_PADDING = OUTER_RING_RADIUS + 20

# ---------------------------------------------------------------------------
# SCORING  -- figures out what a single click is worth
# ---------------------------------------------------------------------------

# -- Measure how far the click was from the target centre,
# -- then return the matching (points, result_label).
# -- math.hypot calculates straight-line distance using the Pythagorean theorem:
# --   distance = sqrt( (click_x - target_x)^2 + (click_y - target_y)^2 )
def get_shot_score(click_x, click_y, target_x, target_y):
    distance = math.hypot(click_x - target_x, click_y - target_y)

    # Check each ring smallest to largest -- first match wins
    for ring_radius, _, ring_points, ring_name in TARGET_RINGS:
        if distance <= ring_radius:
            return ring_points, ring_name

    return 0, "Miss!"

# ---------------------------------------------------------------------------
# DRAWING FUNCTIONS  -- each one is responsible for drawing one thing
# ---------------------------------------------------------------------------

# -- Draw all the rings that make up the target.
# -- We draw from largest to smallest so smaller rings appear on top.
def draw_target(screen, center_x, center_y):
    for ring_radius, ring_color, _, _ in reversed(TARGET_RINGS[:-1]):
        pygame.draw.circle(screen, ring_color, (center_x, center_y), ring_radius)
        pygame.draw.circle(screen, DARK_GRAY, (center_x, center_y), ring_radius, 1)

    # horizontal and vertical crosshair lines through the centre
    pygame.draw.line(screen, DARK_GRAY,
                    (center_x - OUTER_RING_RADIUS, center_y),
                    (center_x + OUTER_RING_RADIUS, center_y), 1)
    pygame.draw.line(screen, DARK_GRAY,
                    (center_x, center_y - OUTER_RING_RADIUS),
                    (center_x, center_y + OUTER_RING_RADIUS), 1)

# -- Draw an X shape at the given position to show where the player clicked.
def draw_shot_marker(screen, x, y, color):
    arm = 8
    pygame.draw.line(screen, color, (x - arm, y - arm), (x + arm, y + arm), 3)
    pygame.draw.line(screen, color, (x + arm, y - arm), (x - arm, y + arm), 3)

# -- Draw a text string on screen.
# -- anchor="center"   means (x, y) is the middle of the text.
# -- anchor="midright" means (x, y) is the right-center edge of the text.
def draw_text(screen, message, font, color, x, y, anchor="center"):
    text_image = font.render(message, True, color)
    text_rect  = text_image.get_rect(**{anchor: (x, y)})
    screen.blit(text_image, text_rect)

# -- Draw a faint grid of tiny dots across the whole background.
def draw_dot_grid(screen):
    for grid_x in range(0, SCREEN_WIDTH, 40):
        for grid_y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.circle(screen, NAVY, (grid_x, grid_y), 1)

# ---------------------------------------------------------------------------
# GAME STATE  -- one dictionary holds everything about the current game
# ---------------------------------------------------------------------------

# -- Build and return a dictionary that describes the current game.
# -- Called at startup and whenever a new level begins.
# --   starting_level   -- which level we are on (1 to TOTAL_LEVELS)
# --   carry_over_score -- points earned in previous levels
def make_fresh_game_state(starting_level=1, carry_over_score=0):

    # Pick a random position that keeps the full target on screen
    target_x = random.randint(TARGET_PADDING, SCREEN_WIDTH  - TARGET_PADDING)
    target_y = random.randint(TARGET_PADDING + 55, SCREEN_HEIGHT - TARGET_PADDING - 55)

    # Speed increases each level. Level 1 is stationary (speed = 0).
    target_speed = (starting_level - 1) * 1.4
    move_angle   = random.uniform(0, 2 * math.pi)  # random direction in radians

    return {
        # --- game flow ---
        "screen_state":    "playing",   # "playing", "summary", or "game_over"
        "current_level":   starting_level,
        "total_score":     carry_over_score,
        "shots_fired":     0,
        "shot_history":    [],          # one dict entry per shot this level

        # --- target position and movement (floats for smooth motion) ---
        "target_x":        target_x,
        "target_y":        target_y,
        "target_speed_x":  math.cos(move_angle) * target_speed,
        "target_speed_y":  math.sin(move_angle) * target_speed,

        # --- feedback shown briefly after each shot ---
        "feedback_label":  "",
        "feedback_points": 0,
        "feedback_frames": 0,   # counts down to 0, then feedback disappears
    }

# ---------------------------------------------------------------------------
# MAIN GAME LOOP
# ---------------------------------------------------------------------------

# -- Start pygame, then loop forever handling events, updating, and drawing.
def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Target Shooter")
    clock = pygame.time.Clock()

    font_huge   = pygame.font.SysFont(None, 54, bold=True)
    font_large  = pygame.font.SysFont(None, 36, bold=True)
    font_medium = pygame.font.SysFont(None, 26)
    font_small  = pygame.font.SysFont(None, 20)

    game = make_fresh_game_state()

    while True:

        # ==================================================================
        # 1. HANDLE INPUT  -- check for mouse clicks and key presses
        # ==================================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    game = make_fresh_game_state()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_x, click_y = event.pos

                # --- Player fires a shot ---
                if game["screen_state"] == "playing":
                    points, result_label = get_shot_score(
                        click_x, click_y,
                        int(game["target_x"]),
                        int(game["target_y"])
                    )

                    game["total_score"] += points
                    game["shots_fired"] += 1
                    game["shot_history"].append({
                        "click_x":      click_x,
                        "click_y":      click_y,
                        "points":       points,
                        "result_label": result_label,
                    })

                    game["feedback_label"]  = result_label
                    game["feedback_points"] = points
                    game["feedback_frames"] = 85   # visible for ~1.4 seconds at 60 fps

                    if game["shots_fired"] >= SHOTS_PER_LEVEL:
                        game["screen_state"] = "summary"

                # --- Click through the summary screen ---
                elif game["screen_state"] == "summary":
                    next_level = game["current_level"] + 1
                    if next_level > TOTAL_LEVELS:
                        game["screen_state"] = "game_over"
                    else:
                        game = make_fresh_game_state(
                            starting_level   = next_level,
                            carry_over_score = game["total_score"]
                        )

                # --- Click the game-over screen to restart ---
                elif game["screen_state"] == "game_over":
                    game = make_fresh_game_state()

        # ==================================================================
        # 2. UPDATE  -- move things and count down timers
        # ==================================================================

        if game["screen_state"] == "playing":

            # Move the target by its speed values each frame
            game["target_x"] += game["target_speed_x"]
            game["target_y"] += game["target_speed_y"]

            # Bounce off left/right edges
            if not (TARGET_PADDING < game["target_x"] < SCREEN_WIDTH - TARGET_PADDING):
                game["target_speed_x"] *= -1   # flip horizontal direction

            # Bounce off top/bottom edges (extra gap at top for the HUD bar)
            if not (TARGET_PADDING + 55 < game["target_y"] < SCREEN_HEIGHT - TARGET_PADDING - 55):
                game["target_speed_y"] *= -1   # flip vertical direction

            if game["feedback_frames"] > 0:
                game["feedback_frames"] -= 1

        # ==================================================================
        # 3. DRAW  -- paint everything onto the screen
        # ==================================================================

        screen.fill(NAVY)
        draw_dot_grid(screen)

        # Draw the target during play and while the summary is showing
        if game["screen_state"] in ("playing", "summary"):
            draw_target(screen, int(game["target_x"]), int(game["target_y"]))

        # Draw the X marker for the most recent shot while feedback is showing
        if game["feedback_frames"] > 0 and game["shot_history"]:
            last_shot    = game["shot_history"][-1]
            marker_color = BRIGHT_GREEN if last_shot["points"] > 0 else BRIGHT_RED
            draw_shot_marker(screen, last_shot["click_x"], last_shot["click_y"], marker_color)

        # --- HUD bar at the top ---
        pygame.draw.rect(screen, DARK_PANEL, (0, 0, SCREEN_WIDTH, 52))
        pygame.draw.line(screen, GOLD, (0, 52), (SCREEN_WIDTH, 52), 2)
        draw_text(screen, f"Level  {game['current_level']} / {TOTAL_LEVELS}",
                font_medium, GOLD, 110, 26)
        draw_text(screen, f"Shots  {game['shots_fired']} / {SHOTS_PER_LEVEL}",
                font_medium, LIGHT_TEXT, 340, 26)
        draw_text(screen, f"Score  {game['total_score']}",
                font_medium, BRIGHT_GREEN, 570, 26)
        draw_text(screen, "R = restart   Esc = quit",
                font_medium, LIGHT_TEXT, SCREEN_WIDTH - 10, 26, anchor="midright")

        # --- Floating score feedback after each shot ---
        if game["feedback_frames"] > 0 and game["screen_state"] == "playing":
            if game["feedback_points"] == 100:
                feedback_color = GOLD
            elif game["feedback_points"] > 0:
                feedback_color = BRIGHT_GREEN
            else:
                feedback_color = BRIGHT_RED

            feedback_y = int(game["target_y"]) - OUTER_RING_RADIUS - 28
            draw_text(screen, game["feedback_label"],
                    font_huge, feedback_color, int(game["target_x"]), feedback_y)
            draw_text(screen, f"+{game['feedback_points']} pts",
                    font_large, feedback_color, int(game["target_x"]), feedback_y + 44)

        # --- Level summary overlay ---
        if game["screen_state"] == "summary":
            dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            dark_overlay.fill(OVERLAY_BLACK)
            screen.blit(dark_overlay, (0, 0))

            draw_text(screen, f"Level {game['current_level']} Complete",
                      font_huge, GOLD, SCREEN_WIDTH // 2, 110)

            row_y = 175
            for shot_number, shot in enumerate(game["shot_history"]):
                row_color = BRIGHT_GREEN if shot["points"] > 0 else BRIGHT_RED
                distance  = math.hypot(shot["click_x"] - game["target_x"],
                                    shot["click_y"] - game["target_y"])
                row_text  = (f"Shot {shot_number + 1}:  {shot['result_label']:<14}"
                            f"  {shot['points']:>3} pts   ({distance:.0f} px off)")
                draw_text(screen, row_text, font_medium, row_color, SCREEN_WIDTH // 2, row_y)
                row_y += 30

            level_total = sum(shot["points"] for shot in game["shot_history"])
            draw_text(screen, f"Level total: {level_total}   Running total: {game['total_score']}",
                      font_medium, LIGHT_TEXT, SCREEN_WIDTH // 2, row_y + 18)

            if game["current_level"] < TOTAL_LEVELS:
                continue_prompt = "Click to continue"
            else:
                continue_prompt = "Click for final score"
            draw_text(screen, continue_prompt, font_small, LIGHT_BLUE,
                      SCREEN_WIDTH // 2, SCREEN_HEIGHT - 44)

        # --- Game over screen ---
        if game["screen_state"] == "game_over":
            screen.fill(NAVY)
            draw_dot_grid(screen)

            max_possible_score = SHOTS_PER_LEVEL * TOTAL_LEVELS * 100
            accuracy_percent   = int(game["total_score"] / max_possible_score * 100)

            draw_text(screen, "GAME OVER", font_huge, GOLD, SCREEN_WIDTH // 2, 120)
            draw_text(screen, f"Final Score:  {game['total_score']} / {max_possible_score}",
                      font_large, LIGHT_TEXT, SCREEN_WIDTH // 2, 210)
            draw_text(screen, f"Accuracy:  {accuracy_percent}%",
                      font_medium, LIGHT_TEXT, SCREEN_WIDTH // 2, 258)

            # Pick a grade based on how accurate the player was
            if accuracy_percent >= 80:
                grade_text, grade_color = "S  --  Sharpshooter!",     GOLD
            elif accuracy_percent >= 60:
                grade_text, grade_color = "A  --  Expert Marksman",   BRIGHT_GREEN
            elif accuracy_percent >= 40:
                grade_text, grade_color = "B  --  Steady Aim",        LIGHT_BLUE
            elif accuracy_percent >= 20:
                grade_text, grade_color = "C  --  Keep Practicing",   DIM_GRAY
            else:
                grade_text, grade_color = "D  --  Back to the Range", BRIGHT_RED

            draw_text(screen, grade_text, font_huge, grade_color, SCREEN_WIDTH // 2, 330)
            draw_text(screen, "Click to play again   R = restart   Esc = quit",
                      font_small, DIM_GRAY, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 44)

        # Push everything we drew onto the actual monitor
        pygame.display.flip()

        # Pause until it is time for the next frame
        clock.tick(FRAMES_PER_SEC)

# ---------------------------------------------------------------------------
# ENTRY POINT  -- Python runs this when you launch the file directly
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_game()