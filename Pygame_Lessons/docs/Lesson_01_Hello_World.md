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
Author: Mark Dencler (mdencler@harford.edu)
Date: 2026-03-18
```
</details>

When you start programming, it is traditional to write a "Hello World" program.  Here is what "Hello World"
looks like in Pygame.

<b>M01_Hello_World.py</b>
```py
import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()

    # Create window
    width, height = 480, 360
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hello World")

    # Set up font
    font = pygame.font.SysFont(None, 48)
    text = font.render("Hello, World!", True, (255, 255, 255))

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill background
        screen.fill((0, 0, 0))

        # Draw text (centered)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)

        # Update display (page flip)
        pygame.display.flip()

    # Clean up
    pygame.quit()

main()
```

Start by taking this script and running it in the CodeHS interactive environment.  Don't worry about what anything does yet.  Just copy and paste the text into the interactive sandbox and use the "▶RUN" button to observe the output.  Take note that you may have to click "STOP" and "▶RUN" a couple times to get the text to cetner on the screen.  Sometimes, during the initial run of a script, CodeHS will position elements incorrectly.  You can easily correct this issue by stopping and running the project one time.  Work until you are able to independently get things to run successfully, then we will begin breaking down the individual elements within the code to better understand how everything works.

<!-- IMAGE - M01_Hello_World - Sample Output -->
<img src="../img/M01_Hello_World_Output.png" width="600"></img>

Let's start by breaking down the beginning part of this script.

```py
import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()
    ...
```

Pygame is a specialized code library that runs within the Python interpreted environment.  Pygame provides access to a series of library functions that perform tasks related to drawing information on the screen, polling input devices, and producing hardware outputs commonly associated with games.  In order to use Pygame in our scripts, we need to link the library within the Python interpreter.  In CodeHS, the connectivity to the Pygame library is already setup, so we just need to include an "import" call in our script to access it.  However, if you want to write a Pygame program in another development enviroment, make sure the Pygame library has been properly installed and accessible to your script within your development environment.

In our scripts, we will be creating a main() function where the instructions for our program start.  After our import statements, we start the Pygame environment with the "pygame.init()" call.

After this, we need to set up some variables to hold information about the window environment.

```py
# Create window
width, height = 480, 360
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hello World")

# Set up font
font = pygame.font.SysFont(None, 48)
text = font.render("Hello, World!", True, (255, 255, 255))
```

We will make a couple variables that represent the display resolution.  For examples on CodeHS, things run most optimally at 480x360.  This corresponds to our 480px (pixels) of width and the 360px of height.  After we have these values established, we set the display mode within Pygame through the call:

```py
screen = pygame.display.set_mode((width, height))
```

We then set the value for the text that appears on the title bar for the display window with the call:

```py
pygame.display.set_caption("Hello World")
```

In CodeHS, you will not see this, but in any other windowed environment, it is important to show the proper program name on the window title.

After this, we will set up the parameters that will be used to display a small box of text on the screen that says "Hello World".  These lines don't display the text box itself, but set up things like the font, display method, and text contents:

```py
font = pygame.font.SysFont(None, 48)
text = font.render("Hello, World!", True, (255, 255, 255))
```

Don't worry about the details for all of the parameters in this part of the script, yet.  However, don't hesitate to try changing certain values to try and figure out how things are working.  For example, try modifying the line that looks like this:

```py
text = font.render("Hello, World!", True, (255, 255, 255))
```

into something that looks like one of these...

```py
text = font.render("Hello, World!", True, (175, 175, 175))
```

```py
text = font.render("Hello, World!", True, (255, 0, 0))
```

```py
text = font.render("Hello, World!", True, (200, 0, 200))
```

Run the script and observe the changes in the output.  Think about what the values in the three numbers represent and come up with combinations to make a predictable change in the output.  This sort of directed "trial and error" method for exploring programming syntax can be a quick and effective method for exploring how aspects of a library like Pygame work.

Now, let's move onto exploring the next part of the "Hello World" program.

```py
# Main loop (one frame in the game renders each time this loop runs)
running = True
while running:  # <-- The BIG LOOP.
    
    # Handle events (message pump)
    for event in pygame.event.get():    # <--- The LITTLE LOOP.
        if event.type == pygame.QUIT:   # <--- The only event we are processing is QUIT.
            running = False

    # Fill background
    screen.fill((0, 0, 0))

    # Draw text (centered)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)

    # Update display (page flip)
    pygame.display.flip()
```

This is probably the most complicated aspect of the script.  However, if you take the time to fully understand the basic straetgy being implemented in this part of the code, you have developed a working foundation for how the code in the majority of video games work -- including titles that have multi-million dollar production costs.

The basic idea is that video games are fundamentally a giant, infinite, loop.  The starting set of loops consists of a single "big loop" that contains an internal "little loop".  The "little loop" inside of the "big loop" is called the "message pump".  Every time the "big loop" runs, a single frame of your game is rendered and shown on the screen.  The "little loop" runs inside of the "big loop" and communicates with the Pygame library to get information about whatever the using is doing with the controls.  If there are still inputs to process for the current frame, the "little loop" will run through every event and give it a chance to be processed.  It could be things like hitting keys, moving the mouse, pressing the buttons on a controller, etc...  Pygame is going to act as the middleman in terms of code layers and make these communications easy for us to retrieve.

Right now, we are just going to write some handler code for a "QUIT" event.  Everything else gets processed in the "message pump" loop, but is ignored in the response code.  All we want "Hello World" to do is display a single message on the screen and let that same message render for every frame in the game.

```py
# Main loop (one frame in the game renders each time this loop runs)
running = True
while running:  # <-- The BIG LOOP.
    
    # Handle events (message pump)
    for event in pygame.event.get():    # <--- The LITTLE LOOP.
        if event.type == pygame.QUIT:   # <--- The only event we are processing is QUIT.
            running = False
```

After the message pump finishing processing events, the rest of the cycle for the primary game loop can finish.  We need to draw some color on the background, render the box that contains the text we set up earlier, and tell Pygame to display the new frame.

```py
# Fill background
screen.fill((0, 0, 0))

# Draw text (centered)
text_rect = text.get_rect(center=(width // 2, height // 2))
screen.blit(text, text_rect)

# Update display (page flip)
pygame.display.flip()
```

The final part of the code is just clean-up.  When the QUIT message is received, we want to make sure Pygame shuts down in a controlled manner and the program can cleanly close.  In CodeHS, you don't have this type of control, but in any other environment, there would be typically be a button to click that closes the window holding your game.  Hitting this button is typically associated with the posting of the QUIT event.

Here is the rest of the code:

```py
# Clean up
pygame.quit()
```

Now, we just have to go back and look at it all together again.  We have a basic understanding of the purpose each of the pieces is serving, so the process of changing the code to experiment and learn more about how things are working can begin.

```py
import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()

    # Create window
    width, height = 480, 360
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hello World")

    # Set up font
    font = pygame.font.SysFont(None, 48)
    text = font.render("Hello, World!", True, (255, 255, 255))

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill background
        screen.fill((0, 0, 0))

        # Draw text (centered)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)

        # Update display (page flip)
        pygame.display.flip()

    # Clean up
    pygame.quit()

main()
```