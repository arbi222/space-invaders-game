import pygame
import random
import math
from pygame import mixer


# initialize the pygame 
pygame.init()

# creating the screen             w   h
screen = pygame.display.set_mode((800,600))

# background
background = pygame.image.load('1234.jpg')

# background sound 
mixer.music.load('background.mp3')
mixer.music.play(-1) # play the song all the time 

# title and icon
pygame.display.set_caption('Space invaders')
icon = pygame.image.load('laser-gun.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 500
playerX_change = 0

# Enemy
enemyImg =[]
enemyX = []

enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemys = 7

for i in range(num_of_enemys):
	enemyImg.append(pygame.image.load('alien.png')) 
	enemyX.append(random.randint(0,735))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(0.25)
	enemyY_change.append(40)


# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.8
bullet_state = 'ready'

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# game over text 
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
	score = font.render('Score : ' + str(score_value) , True, (255,255,255))
	screen.blit(score , (x , y)) 

def game_over_text():
	over_text = over_font.render('GAME OVER' , True , (255, 255, 255))
	screen.blit(over_text , (200 , 250))


def player(x,y):
	screen.blit(playerImg , (x , y))

def enemy(x,y ,i):
	screen.blit(enemyImg[i], (x , y))

def fire_bullet(x,y):
	global bullet_state
	bullet_state = 'fire'
	screen.blit(bulletImg, (x + 16, y + 10))

def iscollision(enemyX , enemyY , bulletX , bulletY):
	distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2)))
	if distance < 27:
		return True
	else:
		return False	

running = True
while running:
	# RGB = RED , GREEN , BLUE ,,  	255 the biggest value
	screen.fill((0,0,0))
	# background image
	screen.blit(background,(0,0))


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
		# if keystroke is pressed check where its right or left 
		if event.type == pygame.KEYDOWN:
			# player
			if event.key == pygame.K_LEFT:
				playerX_change = -0.3
			if event.key == pygame.K_RIGHT:
				playerX_change = 0.3

			# multiple bullets
			if bulletY <= 0:
				bulletY = 480
				bullet_state = 'ready'	
			if event.key == pygame.K_SPACE:
				if bullet_state == 'ready':
					bullet_sound = mixer.Sound('laser.wav')
					bullet_sound.play()
					bulletX = playerX
					fire_bullet(bulletX , bulletY)


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0
	
	# checking for boundaries 
	playerX += playerX_change

	if playerX <= 0:
		playerX = 0
	elif playerX >= 736:
		playerX = 736	

	# enemy boundairies
	for i in range(num_of_enemys):
		
		# game over
		if enemyY[i] > 440:
			for j in range(num_of_enemys):
				enemyY[j] = 2000
			game_over_text()
			break

		enemyX[i] += enemyX_change[i]
		if enemyX[i] <= 0:
			enemyX_change[i] = 0.25
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 736:
			enemyX_change[i] = -0.25
			enemyY[i] += enemyY_change[i]	


		# collision
		collision = iscollision(enemyX[i] , enemyY[i] , bulletX , bulletY)
		if collision:
			explosion_sound = mixer.Sound('explosion.wav')
			explosion_sound.play()
			bulletY = 480
			bullet_state = 'ready'
			score_value += 1
			enemyX[i] = random.randint(0,735)
			enemyY[i] = random.randint(50,150)

		enemy(enemyX[i] , enemyY[i] , i)
	

	# bullet movement
	if bullet_state == 'fire':
		fire_bullet(bulletX , bulletY)
		bulletY -= bulletY_change		
	
	
	

	player(playerX,playerY)
	show_score(textX , textY)
	pygame.display.update()