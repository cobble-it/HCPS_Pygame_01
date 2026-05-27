##########################################################
# try to make the rectangular obstacles a different size #
##########################################################
import pygame
import random
import sys

pygame.init()

# ---🔧 Setup ---
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Runner")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# ---🎨 Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ---📏 Constants ---
GROUND_Y = HEIGHT - 20
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 40

START_SPEED = 5
GRAVITY = 0.8
JUMP_STRENGTH = -15
SPAWN_DELAY = 1500

# ---🧍 Player (raw values) ---
player_x = 50
player_y = GROUND_Y - PLAYER_HEIGHT
velocity_y = 0
on_ground = True

# ---🪨 Obstacles (parallel lists) ---
obs_x = []
obs_y = []
obs_w = []
obs_h = []

# ---🎮 Game State ---
spawn_timer = 0
speed = START_SPEED
score = 0
game_active = False

# -----------------------------
# 🛠️ Helper functions
# -----------------------------

def draw_text(text, x, y):
    img = font.render(text, True, BLACK)
    screen.blit(img, (x, y))

def reset_game():
    global obs_x, obs_y, obs_w, obs_h
    global spawn_timer, speed, score
    global velocity_y, on_ground, player_y

    obs_x.clear()
    obs_y.clear()
    obs_w.clear()
    obs_h.clear()

    spawn_timer = 0
    speed = START_SPEED
    score = 0

    velocity_y = 0
    on_ground = True
    player_y = GROUND_Y - PLAYER_HEIGHT

def spawn_obstacle():
    #changed to a greater height
    height = random.randint(50, 70)

    obs_x.append(WIDTH)
    obs_y.append(GROUND_Y - height)
    obs_w.append(20)
    obs_h.append(height)

def update_player():
    global velocity_y, player_y, on_ground

    velocity_y += GRAVITY
    player_y += velocity_y

    if player_y + PLAYER_HEIGHT >= GROUND_Y:
        player_y = GROUND_Y - PLAYER_HEIGHT
        velocity_y = 0
        on_ground = True

def update_obstacles(dt):
    global obs_x, obs_y, obs_w, obs_h

    #🏃🏼‍ move
    for i in range(len(obs_x)):
        obs_x[i] -= speed

    #🧹 cleanup (manual)
    new_x, new_y, new_w, new_h = [], [], [], []

    for i in range(len(obs_x)):
        if obs_x[i] + obs_w[i] > 0:
            new_x.append(obs_x[i])
            new_y.append(obs_y[i])
            new_w.append(obs_w[i])
            new_h.append(obs_h[i])

    obs_x, obs_y, obs_w, obs_h = new_x, new_y, new_w, new_h

def check_collision():
    retVal=False
    for i in range(len(obs_x)):
        if (
            player_x < obs_x[i] + obs_w[i] and
            player_x + PLAYER_WIDTH > obs_x[i] and
            player_y < obs_y[i] + obs_h[i] and
            player_y + PLAYER_HEIGHT > obs_y[i]
        ):
            retVal=True
    return retVal

def draw_player():
    pygame.draw.rect(screen, BLACK, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

def draw_obstacles():
    for i in range(len(obs_x)):
        pygame.draw.rect(screen, BLACK, (obs_x[i], obs_y[i], obs_w[i], obs_h[i]))

# -----------------------------
# 🎮 Game loop
# -----------------------------

running = True
while running:
    dt = clock.tick(60)
    screen.fill(WHITE)

    # ---📝 Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_active and event.key == pygame.K_SPACE:
                game_active = True
                reset_game()

            elif game_active:
                if event.key == pygame.K_SPACE and on_ground:
                    velocity_y = JUMP_STRENGTH
                    on_ground = False


    if game_active:
        # ---🧍 Player ---
        update_player()

        # ---🪨 Spawn ---
        spawn_timer += dt
        if spawn_timer > SPAWN_DELAY:
            spawn_obstacle()
            spawn_timer = 0

        # ---🪨 Obstacles ---
        update_obstacles(dt)

        # ---💥 Collision ---
        if check_collision():
            game_active = False

        # ---🏆 Score ---
        score += dt // 10
        speed += 0.001 * dt

        # ---🎨 Draw ---
        pygame.draw.line(screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
        draw_player()
        draw_obstacles()
        draw_text(f"Score: {score}", 10, 10)

    else:
        draw_text("Press SPACE to Start", WIDTH // 2 - 150, HEIGHT // 2 - 20)
        draw_text(f"Score: {score}", WIDTH // 2 - 50, HEIGHT // 2 + 60)

    pygame.display.flip()

pygame.quit()
sys.exit()