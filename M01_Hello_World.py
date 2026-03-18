import pygame
import sys

# Initialize Pygame
pygame.init()

# Create window
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hello World")

# Set up font
font = pygame.font.SysFont(None, 48)
text = font.render("Hello, World!", True, (255, 255, 255))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background
    screen.fill((0, 0, 0))

    # Draw text (centered)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)

    # Update display
    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()