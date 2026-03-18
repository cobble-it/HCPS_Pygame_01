### Overview
<details>
    <summary>
    Lesson Summary
    </summary>

```
HCPS Pygame Curricular Project
Title: Lesson 01 - Hello World
Description: This lesson reviews foundational Pygame concepts by taking students
             through the development of a sample "Hello World" program in Pygame.
Author: Mark Dencler
Date: 2026-03-18
```
</details>

<!-- BEGIN - Sample Text and Code -->
#### <u>SCRIPT FILE - "HELLO WORLD"</u>
When you start programming, you always write a "Hello World" program.  Here is what "Hello World"
looks like in Pygame.

<u>M01_Hello_World.py</u>
```py
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
<!-- END - Sample Text and Code -->
```

Start by taking this script and running it in the CodeHS interactive environment.  If you run things successfully you should see an image in the output window that looks like this:

<!-- M01_Hello_World - Sample Output -->
Now let's show it with a &ltimg&gt tag.  This let's you mess with the size.\
<img src="../img/samurai_cat.png" width="200"></img>