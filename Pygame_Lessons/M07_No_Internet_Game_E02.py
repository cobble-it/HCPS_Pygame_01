###############################################
# try to make the obstacles a different shape #
###############################################
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
    # changed to fit the paramaters for .draw.circle
obs_center = [] 
obs_r = []

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
    global obs_center, obs_r
    global spawn_timer, speed, score
    global velocity_y, on_ground, player_y

    obs_center.clear()
    obs_r.clear()


    spawn_timer = 0
    speed = START_SPEED
    score = 0

    velocity_y = 0
    on_ground = True
    player_y = GROUND_Y - PLAYER_HEIGHT

def spawn_obstacle():
    radius = random.randint(30, 50)

    # in order to spawn off screen it must be spawned at the center of the circle + half the length of the circle (radius)
    obs_center.append(WIDTH + radius) 
    obs_r.append(radius)

def update_player():
    global velocity_y, player_y, on_ground

    velocity_y += GRAVITY
    player_y += velocity_y

    if player_y + PLAYER_HEIGHT >= GROUND_Y:
        player_y = GROUND_Y - PLAYER_HEIGHT
        velocity_y = 0
        on_ground = True

def update_obstacles(dt):
    global obs_center, obs_r

    #🏃🏼‍ move
    for i in range(len(obs_center)):
        obs_center[i] -= speed

    #🧹 cleanup (manual)
    new_center, new_r = [], []

    for i in range(len(obs_center)):
        if obs_center[i] + obs_r[i] > 0:
            new_center.append(obs_center[i])
            new_r.append(obs_r[i])

    obs_center, obs_r = new_center, new_r

def check_collision():
    retVal = False
    for i in range(len(obs_center)):
        if (
            player_x < obs_center[i] + obs_r[i] and
            player_x + PLAYER_WIDTH > obs_center[i] - obs_r[i] and
            player_y < GROUND_Y and
            player_y + PLAYER_HEIGHT > GROUND_Y - obs_r[i]
        ):
            retVal= True
    return retVal

def draw_player():
    pygame.draw.rect(screen, BLACK, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

def draw_obstacles():
    for i in range(len(obs_center)):
        pygame.draw.circle(screen, BLACK, (int(obs_center[i]), GROUND_Y - int(obs_r[i])), int(obs_r[i]))

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