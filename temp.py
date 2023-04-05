import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemies
enemies = []
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_type = random.choice(['enemy1', 'enemy2', 'enemy3','enemy4'])
    enemy_image = pygame.image.load(f'{enemy_type}.png')
    enemy_x = random.randint(0, 736)
    enemy_y = random.randint(50, 150)
    enemy_x_change = random.uniform(2.0, 6.0)
    enemy_y_change = random.uniform(20.0, 40.0)
    enemy_health = 1
    if enemy_type == 'enemy2':
        enemy_health = 2
    elif enemy_type == 'enemy3':
        enemy_health = 3
    enemies.append({
        'type':enemy_type,
        'image': enemy_image,
        'x': enemy_x,
        'y': enemy_y,
        'x_change': enemy_x_change,
        'y_change': enemy_y_change,
        'health': enemy_health
    })
    enemyX.append(enemy_x)
    enemyY.append(enemy_y)
    enemyX_change.append(enemy_x_change)
    enemyY_change.append(enemy_y_change)


# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))

theta = 0
def enemy(enemy_data,i):
    global theta
    theta += .005
    val = random.randint(100,200)
    enemy_data[i]['x'] = int(val*math.sin(theta*.1))
    enemy_data[i]['y'] = int(val*math.cos(theta*.1))
    screen.blit(enemy_data[i]['image'], (enemy_data[i]['x'], enemy_data[i]['y']))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemy_data, bulletX, bulletY):
    enemy_rect = pygame.Rect(enemy_data['x'], enemy_data['y'], enemy_data['image'].get_width(),
                            enemy_data['image'].get_height())
    bullet_rect = pygame.Rect(bulletX, bulletY, bulletImg.get_width(), bulletImg.get_height())
    return bullet_rect.colliderect(enemy_rect)


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletSound = mixer.Sound("laser.wav")
                bulletSound.play()
                
                # Get the current x cordinate of the spaceship
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = abs(enemyX_change[i])
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -abs(enemyX_change[i])
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemies[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemies[i]['health'] -= 1
            if enemies[i]['health'] <= 0:
                enemies.pop(i)
                num_of_enemies -= 1
            else:
                enemy_data = enemies[i]
                # enemy_data['image'] = pygame.image.load(f"{enemy_data['type']}_health{enemy_data['health']}.png")
                enemies[i] = enemy_data
        enemy(enemies,i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
