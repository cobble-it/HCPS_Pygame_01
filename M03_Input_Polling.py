import pygame
import sys

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

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
            print(event)
            print(pygame.event.event_name(event.type))  # Console Info Display

            # For each box of text, create a 'Surface' with the desired contents.
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