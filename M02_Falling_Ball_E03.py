import pygame
import sys

# Constants
DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 360
DISPLAY_FPS = 10
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (0, 100, 255)
COLOR_RED = (255, 0, 0)

def main():
    # Initialize Pygame, setup environment variables, and initialize display.
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    clock = pygame.time.Clock()

    # Set up variables that govern the physics for both balls.
    ball_radius = 20                        # The draw radius for the ball (in pixels).
    ball_bounce_factor = -0.7               # Reverse and reduce speed on hit
    gravity = 0.5                           # Acceleration (added to velocity every frame)

    # Ball 1 starting state.
    ball_pos = [DISPLAY_WIDTH // 2, 50]     # The starting coordinates
    ball_velocity_y = 0                     # Current speed

    # Ball 2 starting state.
    ball2_pos = [DISPLAY_WIDTH // 4, 50]    # The starting coordinates
    ball2_velocity_y = 0                    # Current speed

    # Start the primary game loop. (one frame per iteration)
    running = True
    while running:
        screen.fill(COLOR_WHITE)

        # Message pump. This is where events coming in from Pygame are retrieved
        # and processed.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Ball 1 Physics ---
        ball_velocity_y += gravity          # Update the velocity to account for the
                                            # acceleration of gravity.
        ball_pos[1] += ball_velocity_y      # Update the position of the ball to create
                                            # movement based on the current velocity.
        # If ball 1 hit the floor, apply bouncing logic.
        if ball_pos[1] + ball_radius >= DISPLAY_HEIGHT:
            ball_pos[1] = DISPLAY_HEIGHT - ball_radius  # Snap the ball to the floor.
            ball_velocity_y *= ball_bounce_factor        # Reverse the ball's direction
                                                         # and reduce the velocity in
                                                         # a manner where velocity
                                                         # converges on zero.
            # Stop bouncing if velocity is tiny (less than 1).
            if abs(ball_velocity_y) < 1:
                ball_velocity_y = 0

        # --- Ball 2 Physics ---
        ball2_velocity_y += gravity         # Update the velocity to account for the
                                            # acceleration of gravity.
        ball2_pos[1] += ball2_velocity_y    # Update the position of the ball to create
                                            # movement based on the current velocity.
        # If ball 2 hit the floor, apply bouncing logic.
        if ball2_pos[1] + ball_radius >= DISPLAY_HEIGHT:
            ball2_pos[1] = DISPLAY_HEIGHT - ball_radius  # Snap the ball to the floor.
            ball2_velocity_y *= ball_bounce_factor        # Reverse the ball's direction
                                                          # and reduce the velocity in
                                                          # a manner where velocity
                                                          # converges on zero.
            # Stop bouncing if velocity is tiny (less than 1).
            if abs(ball2_velocity_y) < 1:
                ball2_velocity_y = 0

        # Draw both balls on the screen.
        pygame.draw.circle(screen, COLOR_BLUE, (int(ball_pos[0]),  int(ball_pos[1])),  ball_radius)
        pygame.draw.circle(screen, COLOR_RED,  (int(ball2_pos[0]), int(ball2_pos[1])), ball_radius)

        # Show the new frame with a page flip.
        pygame.display.flip()

        # The "clock.tick()" call is used to synchronize frames to create a consistent
        # FPS (frames per second) aesthetic in the display. This call creates a
        # stall in the program that will last as long as necessary to synchronize
        # the primary game loop to a maximum of 10 FPS. This calculation is performed
        # dynamically by Pygame during each individual frame's generation. For games
        # running within CodeHS, it is recommended to cap this value at 10 FPS.
        # However, when deploying in other environments, this value can be adjusted
        # to a higher value to create "smoother" gameplay.
        clock.tick(DISPLAY_FPS)

    # Shut down Pygame.
    pygame.quit()

# Start the script.
main()