import pygame
import sys

# Initialize pygame and create the main window
def init_pygame(width=800, height=600):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Basic Pygame Setup")
    return screen

# Handle all events (like quitting the game)
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Update game state (placeholder for future logic)
def update():
    pass

# Draw everything on the screen
def draw(screen):
    screen.fill((30, 30, 30))  # Fill the screen with a dark color
    pygame.display.flip()      # Update the display

# Main game loop
def main():
    screen = init_pygame()
    clock = pygame.time.Clock()
    while True:
        handle_events()    # Check for quit or other events
        update()           # Update game state
        draw(screen)       # Draw everything
        clock.tick(60)     # Limit to 60 FPS

if __name__ == "__main__":
    main()
