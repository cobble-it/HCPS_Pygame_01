import pygame
import random
import sys

pygame.init()

#📱 Screen
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack-a-Mole")

#🏳️‍🌈 Colors
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 220, 50)
BLACK = (0, 0, 0)

#𝄜 Grid
ROWS, COLS = 3, 3
CELL_SIZE = WIDTH // COLS

#ඞ Fonts
font = pygame.font.SysFont(None, 80)
score_font = pygame.font.SysFont(None, 40)

clock = pygame.time.Clock()

#⚙️ Settings
MAX_MOLES = 4
SPAWN_MIN_DELAY = 400
SPAWN_MAX_DELAY = 1200
UP_DURATION = 300
DOWN_DURATION = 700

# -----------------------------
#🗃️ Mole data (parallel lists)
# -----------------------------
rows = []
cols = []
states = []
alive = []
hit = []
timers = []
offsets = []

# -----------------------------
#🛠️ Functions
# -----------------------------

def create_mole(r, c):
    rows.append(r)
    cols.append(c)
    states.append("up")
    alive.append(True)
    hit.append(False)
    timers.append(pygame.time.get_ticks())
    offsets.append(CELL_SIZE // 2)

def update_mole(i):
    now = pygame.time.get_ticks()

    if states[i] == "up":
        progress = (now - timers[i]) / UP_DURATION
        progress = min(progress, 1)
        offsets[i] = (1 - progress) * (CELL_SIZE // 2)

        if progress >= 1:
            states[i] = "stay"
            timers[i] = now

    elif states[i] == "stay":
        if now - timers[i] > random.randint(500, 1000):
            states[i] = "down"
            timers[i] = now

    elif states[i] == "down":
        progress = (now - timers[i]) / DOWN_DURATION
        progress = min(progress, 1)
        offsets[i] = progress * (CELL_SIZE // 2)

        if progress >= 1:
            alive[i] = False

def draw_mole(i):
    x = cols[i] * CELL_SIZE + CELL_SIZE // 2
    y = rows[i] * CELL_SIZE + CELL_SIZE // 2 + offsets[i]
    #     use your super cool image here 👇
    myimage = pygame.image.load("./img/pancake_whacker_monster_t.png")
    imagerect = myimage.get_rect(center=(x, y))
    SCREEN.blit(myimage, imagerect)

def mole_is_hit(i, pos):
    x = cols[i] * CELL_SIZE + CELL_SIZE // 2
    y = rows[i] * CELL_SIZE + CELL_SIZE // 2 + offsets[i]

    return (
        abs(pos[0] - x) < CELL_SIZE // 4 and
        abs(pos[1] - y) < CELL_SIZE // 4
    )

def cleanup():
    global rows, cols, states, alive, hit, timers, offsets

    rows2, cols2, states2 = [], [], []
    alive2, hit2, timers2, offsets2 = [], [], [], []

    for i in range(len(rows)):
        if alive[i]:
            rows2.append(rows[i])
            cols2.append(cols[i])
            states2.append(states[i])
            alive2.append(alive[i])
            hit2.append(hit[i])
            timers2.append(timers[i])
            offsets2.append(offsets[i])

    rows, cols, states = rows2, cols2, states2
    alive, hit, timers, offsets = alive2, hit2, timers2, offsets2

# -----------------------------
#🎨 Drawing helpers
# -----------------------------

def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(SCREEN, GREEN, rect)
            pygame.draw.rect(SCREEN, BLACK, rect, 2)

def draw_score(score):
    text = score_font.render(f"Score: {score}", True, BLACK)
    SCREEN.blit(text, (10, 10))

# -----------------------------
#🎮 Game state
# -----------------------------

score = 0
next_spawn_time = pygame.time.get_ticks() + random.randint(SPAWN_MIN_DELAY, SPAWN_MAX_DELAY)

# -----------------------------
#🎮 Game loop
# -----------------------------

running = True
while running:
    clock.tick(60)
    SCREEN.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(rows)):
                if mole_is_hit(i, pygame.mouse.get_pos()) and not hit[i]:
                    score += 1
                    hit[i] = True

                    if states[i] != "down":
                        states[i] = "down"
                        timers[i] = pygame.time.get_ticks()

    now = pygame.time.get_ticks()

    #🎯 Spawn
    if now >= next_spawn_time and len(rows) < MAX_MOLES:
        occupied = {(rows[i], cols[i]) for i in range(len(rows)) if alive[i]}
        free_cells = [(r, c) for r in range(ROWS) for c in range(COLS) if (r, c) not in occupied]

        if free_cells:
            r, c = random.choice(free_cells)
            create_mole(r, c)

        next_spawn_time = now + random.randint(SPAWN_MIN_DELAY, SPAWN_MAX_DELAY)

    #🔄 Update
    for i in range(len(rows)):
        update_mole(i)

    #🧹 Cleanup dead
    cleanup()

    #🎨 Draw
    draw_grid()
    for i in range(len(rows)):
        draw_mole(i)
    draw_score(score)

    pygame.display.flip()

pygame.quit()
sys.exit()
