import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Define colors
DARK_GREY = (50, 50, 50)  # Swordsman color
WHITE = (255, 255, 255)  # Background
STEEL_BLUE = (70, 130, 180)  # Sword color

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.fill(WHITE)

    # Draw the swordsman's body
    body_center = (screen_width // 2, screen_height // 2)
    body_size = (20, 40)  # Width and height of the body rectangle
    body_rect = pygame.Rect(body_center[0] - body_size[0] // 2, body_center[1] - body_size[1] // 2, *body_size)
    pygame.draw.rect(screen, DARK_GREY, body_rect)

    # Draw the swordsman's head
    head_radius = 10
    pygame.draw.circle(screen, DARK_GREY, (body_center[0], body_center[1] - body_size[1] // 2 - head_radius), head_radius)

    # Draw the swordsman's sword
    sword_length = 40
    sword_width = 5
    sword_rect = pygame.Rect(body_center[0] - sword_width // 2, body_center[1] - body_size[1] // 2 - sword_length, sword_width, sword_length)
    pygame.draw.rect(screen, STEEL_BLUE, sword_rect)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
