###################################################################################################
# Exercise 1: changing and checking for left mouse click and right mouse click                    # 
###################################################################################################

# Libraries
import pygame
import sys

# Constants
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

# Main function
def main(): 
    # Initialize Pygame
    pygame.init()

    # Create window
    width, height = 480, 360
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hello World")

    # Set up font
    font = pygame.font.SysFont(None, 48)

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            
            # Render the text for each event and its associated attributes.
            
            #nested if statement
            if event.type == pygame.MOUSEBUTTONDOWN:
                # printing out the left button to the console 
                if event.button == 1:  
                    print("Left mouse button clicked")
                # printing out the right button to the console
                elif event.button == 3:  
                    print("Right mouse button clicked")
   
            print(pygame.event.event_name(event.type))  # Console Info Display

            # For each box of text, create a 'Surface' with the desired contents.
            # printing out the left click to the api window and telling the user
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                 text_event       = font.render("Left Click", True, COLOR_BLACK)
                 text_attribute_1 = font.render(str(event.type) , True, COLOR_BLACK)
            # printing out the right click to the api window and telling the user
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
               text_event       = font.render("Right Click", True, COLOR_BLACK)
               text_attribute_1 = font.render(str(event.type) , True, COLOR_BLACK)
            # printing out the event type to the api window and telling the user
            else:
                text_event       = font.render(pygame.event.event_name(event.type), True, COLOR_BLACK)
                text_attribute_1 = font.render(str(event.type)                    , True, COLOR_BLACK)
                         
            
            
            # Process the QUIT event.
            if event.type == pygame.QUIT:
                running = False

        # Fill background
        screen.fill(COLOR_WHITE)

        # Draw text boxes
        text_rect_event = text_event.get_rect(center=(width // 2, int(height * 0.25)))
        screen.blit(text_event, text_rect_event)

        text_rect_event_A1 = text_attribute_1.get_rect(center=(width // 2, int(height * 0.75)))
        screen.blit(text_attribute_1, text_rect_event_A1)

        # Update display (page flip)
        pygame.display.flip()

    # Clean up
    pygame.quit()

main()