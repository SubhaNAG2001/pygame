import pygame
import random
import math
from pygame import mixer

pygame.init() 
pygame.font.init()

color = (255, 0, 0)

screen=pygame.display.set_mode((500, 500))
pygame.display.set_caption("HARM TARGET")


icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

player_char = pygame.image.load('hat.png')

mixer.music.load('background2.mp3')
mixer.music.play(-1)


initial_x = 220
initial_y = 430
posi_x = initial_x
posi_y = initial_y
posi_change =0

enemy_char = []
eposi_x = []
eposi_y = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemy_char.append(pygame.image.load('doll1.png')) 
    eposi_x.append(random.randint(0, 436))
    eposi_y.append(random.randint(0, 75))
    enemyX_change.append(0.2)
    enemyY_change.append(7)

background = pygame.image.load('backg.png')

fire = pygame.image.load('fire.png')
finitial_x = 0
finitial_y = initial_y
fire_x = finitial_x
fire_y = finitial_y
fire_state = "ready"
fireX_change = 0
fireY_change = 1


def player(x , y):
    screen.blit(player_char , (x , y))

def enemy(x, y, i):
    screen.blit(enemy_char[i], (x, y))

def firing(x, y):
    global fire_state
    fire_state = "shoot"
    screen.blit(fire, (x + 16, y + 35))

def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2))+ (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32 )
textposi_X = 10
textposi_Y = 10

def showscore(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

overfont = pygame.font.Font('freesansbold.ttf',50)


def game_over():
    mixer.music.stop()
    gameover_sound = mixer.Sound('gameover.mp3')
    gameover_sound.play()
    game_over_text = overfont.render("GAME OVER!!!", True, (0,0,0))
    screen.blit(game_over_text, (100, 250))

running = True
pygame.time.wait(500)


while running:
    screen.fill(color)
    screen.blit(background, (0, 0)) 
    background.set_alpha(200)

    for events in pygame.event.get():
       if events.type == pygame.QUIT:
           running = False
        

       if events.type == pygame.KEYDOWN:
            print("A key has been pressed")
            if events.key == pygame.K_LEFT: 
                movement = mixer.Sound('movement.mp3')
                movement.play()
                print("left arrow key is pressed")
                posi_change = -1
            if events.key == pygame.K_RIGHT:
                movement = mixer.Sound('movement.mp3')
                movement.play()
                print("right arrow key is pressed")
                posi_change = 1
            if events.key == pygame.K_SPACE:
                if fire_state == "ready":
                    bullet_sound = mixer.Sound('bullet2.mp3')
                    bullet_sound.play()
                    print("Shooting the fire")
                    fire_x = posi_x
                    firing(fire_x, fire_y)


       if events.type == pygame.KEYUP:
            if events.key == pygame.K_LEFT or events.key == pygame.K_RIGHT:
                print("key is unpressed")
                posi_change = 0
            

    posi_x += posi_change 

    if posi_x <=0:
        posi_x = initial_x
    elif posi_x >=436:
        posi_x = initial_x

    for i in range(num_enemies):

        if eposi_y[i] >= 365 :
            for j in range (num_enemies):
                eposi_y[j] = 2000
                posi_y = 2000
            game_over()
            break

        if eposi_x[i] <= 0:
            enemyX_change[i] = 0.6
            if eposi_y[i] <= 363:
                eposi_y[i] += enemyY_change[i]
            else :
                print("GAME OVER")

            
        elif eposi_x[i] >= 436:
            enemyX_change[i] = -0.6
            if eposi_y[i] <= 363:
                eposi_y[i] += enemyY_change[i]
            else:
                print("GAME OVER")

        collision = iscollision(eposi_x[i], eposi_y[i], fire_x, fire_y)
        if collision:
            explosin_sound = mixer.Sound('explosion.mp3')
            explosin_sound.play()
            fire_y = 430
            fire_state = "ready"
            score_value += 1
            eposi_x[i] = random.randint(0, 436)
            eposi_y[i] = random.randint(0, 75)

        enemy(eposi_x[i], eposi_y[i], i)
    
        eposi_x[i] += enemyX_change[i]

    if fire_y <=0:
        fire_state = "ready"
        fire_y = finitial_y

        


    if fire_state == "shoot":
        firing(fire_x, fire_y)
        fire_y -= fireY_change

    
    
    showscore(textposi_X, textposi_Y)
    player(posi_x, posi_y)

    pygame.display.update()  


