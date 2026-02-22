import pygame
import sys

# 1. Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)

# 2. Ball Variables
ball_radius = 20
ball_pos = [WIDTH // 2, 50]  # [x, y]
velocity_y = 0               # Current speed
gravity = 0.5                # Acceleration (added to velocity every frame)
bounce_factor = -0.7         # Reverse and reduce speed on hit

# 3. Main Loop
while True:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Physics Logic ---
    velocity_y += gravity    # Apply gravity to velocity
    ball_pos[1] += velocity_y  # Apply velocity to position

    # --- Collision (Floor) ---
    if ball_pos[1] + ball_radius >= HEIGHT:
        ball_pos[1] = HEIGHT - ball_radius # Snap to floor
        velocity_y *= bounce_factor       # Reverse direction

        # Stop bouncing if velocity is tiny (prevents jitter)
        if abs(velocity_y) < 1:
            velocity_y = 0

    # --- Drawing ---
    pygame.draw.circle(screen, BLUE, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    pygame.display.flip()
    clock.tick(60) # Limits to 60 Frames Per Second