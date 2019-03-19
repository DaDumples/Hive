import pygame
import sys
from numpy import *
from Hive_funcs import *

win_size = (1080,720)

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode(win_size)
	board = Board(screen)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		screen.fill((150,150,150))
		board.draw(pygame.mouse.get_pos())
		pygame.display.flip()