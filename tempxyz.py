import pygame
import math

# Initialize Pygame
pygame.init()

# Set the screen size
screen_width = 640
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the enemy image
enemy_image = pygame.image.load('enemy1.png').convert_alpha()

# Set the initial position of the enemy
enemy_x = screen_width / 2
enemy_y = screen_height / 2

# Set the initial angle and radius of the spiral
angle = 0
radius = 10

# Set the speed of the spiral
speed = 0.001

# Start the Pygame game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Calculate the position of the enemy using the parametric equations for a spiral
    enemy_x = screen_width / 2 + radius * math.cos(angle)
    enemy_y = screen_height / 2 + radius * math.sin(angle)

    # Increment the angle and radius to move the enemy in a spiral
    angle += speed
    radius += speed * 5

    # Draw the enemy on the screen
    screen.blit(enemy_image, (enemy_x, enemy_y))
    enemy_x+=40
    enemy_y+-40

    # Update the screen
    pygame.display.flip()
