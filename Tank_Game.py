import pygame
import random
import math
import sys
import os

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
from pygame import mixer
from pygame.locals import *
# Intialize the pygame
pygame.init()

# Time
record = 0

# Create the Screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Background
background = pygame.image.load('pineapple.jpg')
size = (800, 600)
background = pygame.transform.scale(background, size)
# Caption and Icon
pygame.display.set_caption("坦克大战")
icon = pygame.image.load('tank.png')
pygame.display.set_icon(icon)

# Background Music & Font
mixer.music.load("春节序曲.mp3")
mixer.music.play(-1)
font = pygame.font.SysFont(None, 32)
over_font = pygame.font.SysFont(None, 128)
# Player
playerImg = pygame.image.load('tank player.png')
playerX = 370
playerY = 480
Delta_playerX = 0
Delta_playerY = 0
status = "top"

#Enemy
enemyImg = pygame.image.load('enemy.png')
size = (55, 55)
enemyImg = pygame.transform.scale(enemyImg, size)
enemyX = 250
enemyY = 400
Delta_enemyX = 0
Delta_enemyY = 0
enemystatus = "top"
last = ""
stats = ["top","down","left","right"]
enemies = 0

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 370
bulletY = 480
Delta_bulletX = 0
Delta_bulletY = 0
bullet_state = "ready"
dir = True
bulletstatus = "top"
lastbullet = ""
collision = 0

def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+5, y+5))

# Collision Detection Mechanism     
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 35:
        return True
    else:
        return False

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (76,230,0))
    screen.blit(over_text, (200, 250))

def win_text():
    win_text = over_font.render("YOU WIN!", True, (66,78,179))
    screen.blit(win_text, (200, 250))

def enemies_left(x,y,collision):
    enemies = 5 - collision
    ene = font.render("Enemies Left : " + str(enemies), True, (0, 200, 155))
    screen.blit(ene, (x, y))

# Game Loop
run = True
while run:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Detection of keyboard pressing to change the position of the player tank
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Delta_playerY -= 0.05
                Delta_playerX = 0
                if status == "top":
                    playerImg = pygame.transform.rotate(playerImg, 0)
                elif status == "right":
                    playerImg = pygame.transform.rotate(playerImg, 90)
                elif status == "left":
                    playerImg = pygame.transform.rotate(playerImg, -90)
                else:
                    playerImg = pygame.transform.rotate(playerImg, 180)
                status = "top"
            elif event.key == pygame.K_DOWN:
                Delta_playerY += 0.05
                Delta_playerX = 0
                if status == "top":
                    playerImg = pygame.transform.rotate(playerImg, 180)
                elif status == "right":
                    playerImg = pygame.transform.rotate(playerImg, -90)
                elif status == "left":
                    playerImg = pygame.transform.rotate(playerImg, 90)
                else:
                    playerImg = pygame.transform.rotate(playerImg, 0)
                status = "down"
            elif event.key == pygame.K_RIGHT:
                Delta_playerX += 0.05
                Delta_playerY = 0
                if status == "top":
                    playerImg = pygame.transform.rotate(playerImg, -90)
                elif status == "right":
                    playerImg = pygame.transform.rotate(playerImg, 0)
                elif status == "left":
                    playerImg = pygame.transform.rotate(playerImg, 180)
                else:
                    playerImg = pygame.transform.rotate(playerImg, 90)
                status = "right"
            elif event.key == pygame.K_LEFT:
                Delta_playerX -= 0.05
                Delta_playerY = 0
                if status == "top":
                    playerImg = pygame.transform.rotate(playerImg, 90)
                elif status == "right":
                    playerImg = pygame.transform.rotate(playerImg, 180)
                elif status == "left":
                    playerImg = pygame.transform.rotate(playerImg, 0)
                else:
                    playerImg = pygame.transform.rotate(playerImg, -90)
                status = "left"
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
                    dir = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                Delta_playerX = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                Delta_playerY = 0


    # Player Coordinate Updates    
    playerX += Delta_playerX
    playerY += Delta_playerY
    if playerX <= 0:
        playerX = 0
    elif playerX >= 740:
        playerX = 740
    if playerY <= 5:
        playerY = 5
    elif playerY >= 540:
        playerY = 540

    # Enemy Coordinate Updates  
    enemyX += Delta_enemyX
    enemyY += Delta_enemyY
    if enemyX <= 0:
        enemyX = 0
    elif enemyX >= 736:
        enemyX = 735
    if enemyY <= 10:
        enemyY = 10
    elif enemyY >= 550:
        enemyY = 550
    
    # Enemy movement mechanisms
    seconds=(pygame.time.get_ticks())/1000
    if seconds - record >= random.randint(1,5):
        if enemystatus == "top":
            Delta_enemyY = random.uniform(-0.06,0)
            Delta_enemyX = 0
            if last == "top":
                enemyImg = pygame.transform.rotate(enemyImg, 0)
            elif last == "right":
                enemyImg = pygame.transform.rotate(enemyImg, 90)
            elif last == "left":
                enemyImg = pygame.transform.rotate(enemyImg, -90)
            elif last == "down":
                enemyImg = pygame.transform.rotate(enemyImg, 180)
        elif enemystatus == "down":
            Delta_enemyY = random.uniform(0,0.07)
            Delta_enemyX = 0
            if last == "top":
                enemyImg = pygame.transform.rotate(enemyImg, 180)
            elif last == "right":
                enemyImg = pygame.transform.rotate(enemyImg, -90)
            elif last == "left":
                enemyImg = pygame.transform.rotate(enemyImg, 90)
            elif last == "down":
                enemyImg = pygame.transform.rotate(enemyImg, 0)
        elif enemystatus == "right":
            Delta_enemyX = random.uniform(0,0.07)
            Delta_enemyY = 0
            if last == "top":
                enemyImg = pygame.transform.rotate(enemyImg, -90)
            elif last == "right":
                enemyImg = pygame.transform.rotate(enemyImg, 0)
            elif last == "left":
                enemyImg = pygame.transform.rotate(enemyImg, 180)
            elif last == "down":
                enemyImg = pygame.transform.rotate(enemyImg, 90)
        elif enemystatus =="left":
            Delta_enemyX = random.uniform(-0.07,0)
            Delta_enemyY = 0
            if last == "top":
                enemyImg = pygame.transform.rotate(enemyImg, 90)
            elif last == "right":
                enemyImg = pygame.transform.rotate(enemyImg, 180)
            elif last == "left":
                enemyImg = pygame.transform.rotate(enemyImg, 0)
            elif last == "down":
                enemyImg = pygame.transform.rotate(enemyImg, -90)
        last = enemystatus
        enemystatus = stats[random.randint(0,3)]
        record = seconds

    # Bullet Movement 
    if bulletY <= 0 or bulletY >= 550 or bulletX <= 0 or bulletX >= 750:
        bulletY = playerY
        bulletX = playerX
        bullet_state = "ready"
        dir = True

    if bullet_state == "fire":
        if dir:
            bulletstatus = status
            dir = False
        fire_bullet(bulletX, bulletY)
        if bulletstatus == "down":
            Delta_bulletY = 0.05
            Delta_bulletX = 0
            if lastbullet == "top" or lastbullet == "" :
                bulletImg = pygame.transform.rotate(bulletImg, 180)
            elif lastbullet == "right":
                bulletImg = pygame.transform.rotate(bulletImg, -90)
            elif lastbullet == "left":
                bulletImg = pygame.transform.rotate(bulletImg, 90)
            elif last == "down":
                bulletImg = pygame.transform.rotate(bulletImg, 0)
            lastbullet = "down"
        elif bulletstatus == "top":
            Delta_bulletY = -0.05
            Delta_bulletX = 0
            if lastbullet == "top" or lastbullet == "" :
                bulletImg = pygame.transform.rotate(bulletImg, 0)
            elif lastbullet == "right":
                bulletImg = pygame.transform.rotate(bulletImg, 90)
            elif lastbullet == "left":
                bulletImg = pygame.transform.rotate(bulletImg, -90)
            elif last == "down":
                bulletImg = pygame.transform.rotate(bulletImg, 180)
            lastbullet = "top"
        elif bulletstatus == "left":
            Delta_bulletY = 0
            Delta_bulletX = -0.05
            if lastbullet == "top" or lastbullet == "" :
                bulletImg = pygame.transform.rotate(bulletImg, 90)
            elif lastbullet == "right":
                bulletImg = pygame.transform.rotate(bulletImg, 180)
            elif lastbullet == "left":
                bulletImg = pygame.transform.rotate(bulletImg, 0)
            elif last == "down":
                bulletImg = pygame.transform.rotate(bulletImg, -90)
            lastbullet = "left"
        elif bulletstatus == "right":
            Delta_bulletY = 0
            Delta_bulletX = 0.05
            if lastbullet == "top" or lastbullet == "" :
                bulletImg = pygame.transform.rotate(bulletImg, -90)
            elif lastbullet == "right":
                bulletImg = pygame.transform.rotate(bulletImg, 0)
            elif lastbullet == "left":
                bulletImg = pygame.transform.rotate(bulletImg, 180)
            elif last == "down":
                bulletImg = pygame.transform.rotate(bulletImg, 90)
            lastbullet = "right"
        bulletX += Delta_bulletX
        bulletY += Delta_bulletY

    bulletcollide = isCollision(enemyX, enemyY, bulletX, bulletY)
    if bulletcollide: 
        explosionSound = mixer.Sound("explosion.wav")
        explosionSound.play()
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)
        collision +=1 

    tankscollide = isCollision(playerX, playerY, enemyX, enemyY)
    if tankscollide:
        enemyImg = pygame.transform.scale (enemyImg, (0,0))
        playerImg = pygame.transform.scale (playerImg, (0,0))
        game_over_text()
        if seconds - record >= 5:
            break
    if collision >= 5:
        enemyImg = pygame.transform.scale (enemyImg, (0,0)) 
        playerImg = pygame.transform.scale (playerImg, (0,0))
        win_text()
        if seconds - record >= 5:
            break
    player(playerX,playerY)
    enemy(enemyX,enemyY)
    enemies_left(20,20,collision)
    pygame.display.update()