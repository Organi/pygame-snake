import pygame
import time
import random

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

fps = 15
block_size = 10
apple_size = 10
snap_apple_to_grid = False
display_width = 800
display_height = int(display_width / 16 * 9)
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Slither')

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)

def snake(snakelist):
	for xy in snakelist:
		pygame.draw.rect(gameDisplay, black, [xy[0], xy[1], block_size, block_size])

def apple(randAppleX, randAppleY):
	pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, apple_size, apple_size])

def text_objects(text, colour):
	textSurface = font.render(text, True, colour)
	return textSurface, textSurface.get_rect()

def message_to_screen(msg, colour):
	textSurface, textRect = text_objects(msg, colour)
	textRect.center = int(display_width/2), int(display_height/2)
	gameDisplay.blit(textSurface, textRect)

def gameLoop():
	# Game Loop
	gameExit = False
	gameOver = False
	
	# Snake Variables
	snake_list = []
	snake_length = 1
	lead_x = round(int(display_width / 2) / float(block_size)) * float(block_size)
	lead_y = round(int(display_height / 2) / float(block_size)) * float(block_size)
	lead_x_change = 0
	lead_y_change = 0

	if snap_apple_to_grid == True:
		randAppleX = random.randrange(0, display_width-apple_size, apple_size)
		randAppleY = random.randrange(0, display_height-apple_size, apple_size)
	else:
		randAppleX = random.randrange(0, display_width-apple_size)
		randAppleY = random.randrange(0, display_height-apple_size)


	while not gameExit:

		while gameOver == True:
			gameDisplay.fill(white)
			message_to_screen("Game over, please C to play again or Q to quit", red)
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameExit = True
					gameOver = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False
					elif event.key == pygame.K_c:
						gameLoop()

		# Handle Input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					lead_x_change = -block_size
					lead_y_change = 0
				elif event.key == pygame.K_RIGHT:
					lead_x_change = block_size
					lead_y_change = 0
				elif event.key == pygame.K_UP:
					lead_y_change = -block_size
					lead_x_change = 0
				elif event.key == pygame.K_DOWN:
					lead_y_change = block_size
					lead_x_change = 0

		# Logic
		if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
			gameOver = True
	
		lead_x += lead_x_change
		lead_y += lead_y_change

		# Render Output
		gameDisplay.fill(green)
		apple(randAppleX, randAppleY)

		snake_head = []
		snake_head.append(lead_x)
		snake_head.append(lead_y)
		snake_list.append(snake_head)

		if len(snake_list) > snake_length:
			del snake_list[0]

		for segment in snake_list[:-1]:
			if segment == snake_head:
				gameOver = True

		snake(snake_list)
		pygame.display.update()

		# Snake has eaten an apple
		if (lead_x >= randAppleX and lead_x < randAppleX + apple_size) or (lead_x + block_size >= randAppleX and lead_x + block_size < randAppleX + apple_size):
			if (lead_y >= randAppleY and lead_y < randAppleY + apple_size) or (lead_y + block_size >= randAppleY and lead_y + block_size < randAppleY + apple_size):
				if snap_apple_to_grid == True:
					randAppleX = random.randrange(0, display_width-apple_size, apple_size)
					randAppleY = random.randrange(0, display_height-apple_size, apple_size)
				else:
					randAppleX = random.randrange(0, display_width-apple_size)
					randAppleY = random.randrange(0, display_height-apple_size)
				snake_length += 1

		# FPS
		clock.tick(fps)

	pygame.quit()
	quit()

gameLoop()
