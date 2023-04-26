import pygame
import random
import math
from pygame import mixer

#initialize pygame
pygame.init() #must always have this line

#create the screen
screen = pygame.display.set_mode((800, 600))#(width, height)

#background
background = pygame.image.load('spacebackground.png')

# #Background music
# mixer.music.load("Hi.mp3")
# mixer.music.play(-1)

#title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

#Bullet
#Ready - You cant see the bullet on the screen
#Fire - The bullet is firing
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
bullet_state = 'ready'

#Score
score_value = 0
font = pygame.font.Font('Bubblegum.ttf',40)

textX = 10
textY = 10
#Game over text
game_over_font  = pygame.font.Font('Bubblegum.ttf', 64)

def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (250, 250))

def show_score(x,y):
    score = font.render('Score: '+ str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def Player(X, Y):
    screen.blit(playerImg,(X, Y)) 

def Enemy(X, Y, i):
    screen.blit(enemyImg[i], (X, Y))

def firebullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg,(x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 35:
        return True
    else:
        return False

#Game Loop
running = True
while running:
    #RGB = Red, Green, Blue
    screen.fill((141, 28, 212))
    #background image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if keystroke is pressed, check wether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    firebullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    #Checking for boundaries of spaceship so it doesnt go out of bounds
    playerX += playerX_change
    
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    #Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        firebullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    #Checking enemy boundaries
    for i in range(num_of_enemies):

        #Game over
        if enemyY[i] > 416:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] +=enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change [i]
        
        
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 10
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        Enemy(enemyX[i],enemyY[i],i)
    Player(playerX, playerY) 
    show_score(textX, textY)
    pygame.display.update() #must always have this line