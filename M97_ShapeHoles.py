# Watch Me

import pygame
import sys

# --- Initialization ---
pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
GRAY = (150, 150, 150)
RED = (235, 64, 52)      # Triangle
GREEN = (52, 235, 110)   # Square
BLUE = (52, 137, 235)    # Circle
TEXT_COLOR = (50, 50, 50)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Put the Shape in the Hole")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("arial", 32, bold=True)
small_font = pygame.font.SysFont("arial", 24)

# --- Classes ---
class Hole:
    def __init__(self, shape_type, x, y, size):
        self.type = shape_type
        self.rect = pygame.Rect(x, y, size, size)
        self.size = size
        self.color = GRAY
        self.thickness = 5

    def draw(self, surface):
        if self.type == "square":
            pygame.draw.rect(surface, self.color, self.rect, self.thickness)
        elif self.type == "circle":
            pygame.draw.circle(surface, self.color, self.rect.center, self.size // 2, self.thickness)
        elif self.type == "triangle":
            points = [
                (self.rect.centerx, self.rect.top),
                (self.rect.left, self.rect.bottom),
                (self.rect.right, self.rect.bottom)
            ]
            pygame.draw.polygon(surface, self.color, points, self.thickness)

class DraggableShape:
    def __init__(self, shape_type, color, x, y, size):
        self.type = shape_type
        self.color = color
        self.rect = pygame.Rect(x, y, size, size)
        self.start_x = x
        self.start_y = y
        self.size = size
        self.is_dragging = False
        self.is_placed = False

    def draw(self, surface):
        # Don't draw if it's already placed (it "falls" into the hole)
        if self.is_placed:
            return

        if self.type == "square":
            pygame.draw.rect(surface, self.color, self.rect)
        elif self.type == "circle":
            pygame.draw.circle(surface, self.color, self.rect.center, self.size // 2)
        elif self.type == "triangle":
            points = [
                (self.rect.centerx, self.rect.top),
                (self.rect.left, self.rect.bottom),
                (self.rect.right, self.rect.bottom)
            ]
            pygame.draw.polygon(surface, self.color, points)

    def reset_position(self):
        self.rect.topleft = (self.start_x, self.start_y)

# --- Game Setup ---
shape_size = 100

# Create Holes (Top of the screen)
holes = [
    Hole("circle", 150, 100, shape_size),
    Hole("square", 350, 100, shape_size),
    Hole("triangle", 550, 100, shape_size)
]

# Create Shapes (Bottom of the screen)
shapes = [
    DraggableShape("circle", BLUE, 150, 400, shape_size),
    DraggableShape("square", GREEN, 350, 400, shape_size),
    DraggableShape("triangle", RED, 550, 400, shape_size)
]

message = "Drag the shapes into the correct holes!"
message_color = TEXT_COLOR
meme_triggered = False

# --- Main Game Loop ---
running = True
while running:
    screen.fill(WHITE)

    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                # Check backwards to grab the shape drawn on top
                for shape in reversed(shapes):
                    if shape.rect.collidepoint(event.pos) and not shape.is_placed:
                        shape.is_dragging = True
                        
                        # Move the clicked shape to the end of the list so it renders on top
                        shapes.remove(shape)
                        shapes.append(shape)
                        break 

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for shape in shapes:
                    if shape.is_dragging:
                        shape.is_dragging = False
                        
                        # Check if dropped in a hole
                        dropped_in_hole = False
                        for hole in holes:
                            # If the mouse cursor is inside a hole's area
                            if hole.rect.collidepoint(event.pos):
                                dropped_in_hole = True
                                
                                # Normal Win Condition
                                if shape.type == hole.type:
                                    shape.is_placed = True
                                    shape.rect.center = hole.rect.center
                                    message = "Perfect fit!"
                                    message_color = GREEN
                                
                                # Meme Win Condition: Everything goes in the square hole
                                elif hole.type == "square":
                                    shape.is_placed = True
                                    shape.rect.center = hole.rect.center
                                    message = "That's right. It goes in the square hole."
                                    message_color = RED
                                    meme_triggered = True
                                
                                # Wrong hole
                                else:
                                    shape.reset_position()
                                    message = "Nope, try again!"
                                    message_color = BLACK
                                break
                        
                        # If dropped in empty space
                        if not dropped_in_hole:
                            shape.reset_position()

        elif event.type == pygame.MOUSEMOTION:
            for shape in shapes:
                if shape.is_dragging:
                    # Center the shape on the mouse cursor
                    shape.rect.centerx = event.pos[0]
                    shape.rect.centery = event.pos[1]

    # 2. Check Win Condition
    all_placed = all(shape.is_placed for shape in shapes)
    if all_placed:
        if meme_triggered:
            message = "GAME OVER. Everything is in the square hole."
        else:
            message = "YOU WIN! All shapes sorted correctly!"

    # 3. Drawing
    # Draw Holes
    for hole in holes:
        hole.draw(screen)

    # Draw Shapes
    for shape in shapes:
        shape.draw(screen)

    # Draw Text
    text_surface = font.render(message, True, message_color)
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 30))

    if all_placed:
        restart_text = small_font.render("Press 'R' to Restart", True, GRAY)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 70))

    # Restart logic
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r] and all_placed:
        for shape in shapes:
            shape.is_placed = False
            shape.reset_position()
        message = "Drag the shapes into the correct holes!"
        message_color = TEXT_COLOR
        meme_triggered = False

    pygame.display.flip()
    clock.tick(FPS)

# --- Cleanup ---
pygame.quit()
sys.exit()
