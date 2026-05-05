import pygame
import random

# --- Setup ---
pygame.init()

WIDTH, HEIGHT = 480, 360
CELL = 20
COLS = WIDTH // CELL
ROWS = HEIGHT // CELL
FPS = 10  # Works great at 10 FPS — one move per frame

screen = pygame.display.set_mode((WIDTH, HEIGHT + 40))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# --- Colors ---
BLACK  = (0,   0,   0)
GREEN  = (50,  200, 50)
DGREEN = (30,  140, 30)
RED    = (220, 50,  50)
WHITE  = (255, 255, 255)
GRAY   = (30,  30,  30)

def draw_cell(x, y, color):
    rect = pygame.Rect(x * CELL, y * CELL, CELL - 1, CELL - 1)
    pygame.draw.rect(screen, color, rect, border_radius=3)

def random_food(snake):
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in snake:
            return pos

def game_loop():
    snake = [(COLS // 2, ROWS // 2)]
    direction = (1, 0)
    next_dir = direction
    food = random_food(snake)
    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(FPS)

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # quit entirely
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        return True  # restart
                else:
                    if event.key == pygame.K_UP    and direction != (0, 1):
                        next_dir = (0, -1)
                    elif event.key == pygame.K_DOWN  and direction != (0, -1):
                        next_dir = (0, 1)
                    elif event.key == pygame.K_LEFT  and direction != (1, 0):
                        next_dir = (-1, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                        next_dir = (1, 0)

        if not game_over:
            direction = next_dir
            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

            # Wall or self collision
            if (head[0] < 0 or head[0] >= COLS or
                head[1] < 0 or head[1] >= ROWS or
                head in snake):
                game_over = True
            else:
                snake.insert(0, head)
                if head == food:
                    score += 1
                    food = random_food(snake)
                else:
                    snake.pop()

        # --- Draw ---
        screen.fill(GRAY)

        # Grid (subtle)
        for gx in range(COLS):
            for gy in range(ROWS):
                r = pygame.Rect(gx * CELL, gy * CELL, CELL, CELL)
                pygame.draw.rect(screen, (35, 35, 35), r, 1)

        # Food
        draw_cell(food[0], food[1], RED)

        # Snake
        for i, (sx, sy) in enumerate(snake):
            color = GREEN if i > 0 else DGREEN
            draw_cell(sx, sy, color)

        # Score bar
        pygame.draw.rect(screen, BLACK, (0, HEIGHT, WIDTH, 40))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT + 8))

        if game_over:
            # Overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            msg1 = font.render("Game Over!", True, WHITE)
            msg2 = font.render(f"Score: {score}  —  Press R to restart", True, WHITE)
            screen.blit(msg1, (WIDTH // 2 - msg1.get_width() // 2, HEIGHT // 2 - 30))
            screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 + 5))

        pygame.display.flip()
        
        # Delay (reduce difficulty)
        pygame.time.delay(300)  # 300ms delay

    return False

# --- Main ---
restart = True
while restart:
    restart = game_loop()

pygame.quit()