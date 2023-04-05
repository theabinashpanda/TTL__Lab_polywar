import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))

# Set up the game clock
clock = pygame.time.Clock()

# Set the window title
pygame.display.set_caption("Space War")

# Set up the player
player_image = pygame.image.load("player.png")
player_x = 370
player_y = 480
player_x_change = 0

# Set up the enemy
enemy_images = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_health = []
num_enemies = 1

for i in range(num_enemies):
    # choose random health for each enemy
    health = random.choice([1, 2, 3])
    enemy_images.append(pygame.image.load(f"enemy{health}.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)
    enemy_health.append(health)

# Set up the bullet
bullet_image = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_y_change = 10
bullet_state = "ready"

# Set up the score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(player_image, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_images[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 16, y - 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = ((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)**0.5
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:
    # Fill the screen with black
    screen.fill((0, 0, 0))
    
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:  # <--- This is the key for firing the bullet
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
                        
        # Check for key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

                
    # Move the player
    player_x += player_x_change
    
    # Restrict the player to the screen
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736
# Move the enemy
for i in range(num_enemies):
    # Check if game over
    if enemy_y[i] > 440:
        for j in range(num_enemies):
            enemy_y[j] = 2000
        game_over_text = font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(game_over_text, (200, 250))
        break
        
    enemy_x[i] += enemy_x_change[i]
    if enemy_x[i] <= 0:
        enemy_x_change[i] = 4
        enemy_y[i] += enemy_y_change[i]
    elif enemy_x[i] >= 736:
        enemy_x_change[i] = -4
        enemy_y[i] += enemy_y_change[i]
        
    # Check for collision
    collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
    if collision:
        bullet_y = 480
        bullet_state = "ready"
        score_value += enemy_health[i]
        enemy_health[i] = 0
        enemy_x[i] = random.randint(0, 736)
        enemy_y[i] = random.randint(50, 150)
        
    # Draw the enemy
    enemy(enemy_x[i], enemy_y[i], i)

# Move the bullet
if bullet_y <= 0:
    bullet_y = 480
    bullet_state = "ready"
    
if bullet_state == "fire":
    fire_bullet(bullet_x, bullet_y)
    bullet_y -= bullet_y_change
    
# Draw the player
player(player_x, player_y)

# Draw the score
show_score(text_x, text_y)

# Update the display
pygame.display.update()

# Set the frame rate
clock.tick(60)
