import pygame
import random
import math
import sys

# --- Initialization ---
pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("courier", 24, bold=True)
big_font = pygame.font.SysFont("courier", 48, bold=True)

# --- Classes ---
class Ship:
    def __init__(self):
        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.radius = 15
        self.is_thrusting = False

    def draw(self, surface):
        # Calculate the 3 points of the ship triangle based on angle
        tip = self.pos + pygame.Vector2(0, -20).rotate(self.angle)
        left = self.pos + pygame.Vector2(-15, 15).rotate(self.angle)
        right = self.pos + pygame.Vector2(15, 15).rotate(self.angle)
        
        # Draw hollow triangle
        pygame.draw.polygon(surface, WHITE, [tip, left, right], 2)
        
        # Draw thrust flame if moving
        if self.is_thrusting:
            flame_tip = self.pos + pygame.Vector2(0, 25).rotate(self.angle)
            flame_left = self.pos + pygame.Vector2(-8, 15).rotate(self.angle)
            flame_right = self.pos + pygame.Vector2(8, 15).rotate(self.angle)
            pygame.draw.polygon(surface, WHITE, [flame_tip, flame_left, flame_right], 1)

    def update(self, keys):
        self.is_thrusting = False
        
        # Rotation
        if keys[pygame.K_LEFT]:
            self.angle -= 5
        if keys[pygame.K_RIGHT]:
            self.angle += 5
            
        # Thrust
        if keys[pygame.K_UP]:
            self.is_thrusting = True
            thrust = pygame.Vector2(0, -0.2).rotate(self.angle)
            self.vel += thrust

        # Apply velocity and friction (space drag)
        self.pos += self.vel
        self.vel *= 0.99 

        # Screen Wrap
        self.pos.x = self.pos.x % WIDTH
        self.pos.y = self.pos.y % HEIGHT

class Asteroid:
    def __init__(self, x, y, size):
        self.pos = pygame.Vector2(x, y)
        self.size = size  # 3 = Large, 2 = Medium, 1 = Small
        self.radius = size * 20
        
        # Random speed based on size (smaller = faster)
        speed = random.uniform(1, 3) + (3 - size) * 0.5
        angle = random.uniform(0, 360)
        self.vel = pygame.Vector2(speed, 0).rotate(angle)

    def draw(self, surface):
        # Drawing a simple hollow circle to mimic vector graphics
        pygame.draw.circle(surface, WHITE, (int(self.pos.x), int(self.pos.y)), int(self.radius), 2)

    def update(self):
        self.pos += self.vel
        self.pos.x = self.pos.x % WIDTH
        self.pos.y = self.pos.y % HEIGHT

class Bullet:
    def __init__(self, pos, angle):
        self.pos = pygame.Vector2(pos)
        # Bullet travels in the direction the ship is facing
        self.vel = pygame.Vector2(0, -10).rotate(angle)
        self.timer = 45  # Disappears after 45 frames

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.pos.x), int(self.pos.y)), 3)

    def update(self):
        self.pos += self.vel
        self.pos.x = self.pos.x % WIDTH
        self.pos.y = self.pos.y % HEIGHT
        self.timer -= 1

# --- Game Variables ---
def reset_game():
    global ship, asteroids, bullets, score, lives, game_over
    ship = Ship()
    bullets = []
    asteroids = []
    score = 0
    lives = 3
    game_over = False
    
    # Spawn initial large asteroids away from the center
    for _ in range(4):
        x, y = WIDTH // 2, HEIGHT // 2
        while WIDTH // 2 - 100 < x < WIDTH // 2 + 100 and HEIGHT // 2 - 100 < y < HEIGHT // 2 + 100:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
        asteroids.append(Asteroid(x, y, 3))

reset_game()
shoot_cooldown = 0

# --- Main Game Loop ---
running = True
while running:
    screen.fill(BLACK)

    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        # 2. Player Input & Shooting
        ship.update(keys)
        
        if shoot_cooldown > 0:
            shoot_cooldown -= 1
            
        if keys[pygame.K_SPACE] and shoot_cooldown == 0:
            # Tip of the ship
            spawn_pos = ship.pos + pygame.Vector2(0, -20).rotate(ship.angle)
            bullets.append(Bullet(spawn_pos, ship.angle))
            shoot_cooldown = 15  # Limit fire rate

        # 3. Update Entities
        for bullet in bullets[:]:
            bullet.update()
            if bullet.timer <= 0:
                bullets.remove(bullet)

        for ast in asteroids:
            ast.update()

        # 4. Collision Detection
        # Bullet vs Asteroid
        for bullet in bullets[:]:
            for ast in asteroids[:]:
                if bullet.pos.distance_to(ast.pos) < ast.radius:
                    if bullet in bullets:
                        bullets.remove(bullet)
                    asteroids.remove(ast)
                    
                    score += (4 - ast.size) * 100  # More points for smaller asteroids
                    
                    # Split asteroid if it's large enough
                    if ast.size > 1:
                        asteroids.append(Asteroid(ast.pos.x, ast.pos.y, ast.size - 1))
                        asteroids.append(Asteroid(ast.pos.x, ast.pos.y, ast.size - 1))
                    break

        # Ship vs Asteroid
        for ast in asteroids:
            if ship.pos.distance_to(ast.pos) < ast.radius + ship.radius:
                lives -= 1
                if lives > 0:
                    ship = Ship() # Reset ship to middle
                    bullets.clear()
                else:
                    game_over = True
                break

        # Spawn new wave if all asteroids destroyed
        if len(asteroids) == 0:
            for _ in range(5):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                asteroids.append(Asteroid(x, y, 3))

        # 5. Drawing
        ship.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for ast in asteroids:
            ast.draw(screen)

        # UI
        score_text = font.render(f"SCORE: {score}", True, WHITE)
        lives_text = font.render(f"LIVES: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 150, 10))

    else:
        # Game Over Screen
        go_text = big_font.render("GAME OVER", True, WHITE)
        score_info = font.render(f"FINAL SCORE: {score}", True, WHITE)
        restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
        
        screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_info, (WIDTH // 2 - score_info.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

        if keys[pygame.K_r]:
            reset_game()
        if keys[pygame.K_q]:
            running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
