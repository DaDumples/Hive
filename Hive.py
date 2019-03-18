import pygame
import sys
from numpy import *
from Hive_funcs import *

win_size = (1080,720)

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode(win_size)

	queen = Queen(1,(1,0),screen)

	state = [(0,1,0),
			 (1,-1,0),
			 (0,-1,0),
			 (-1,1,0),
			 (2,-2,0),
			 (2,-3,0),
			 (1,-3,0),
			 (-1,-1,0)]
	# state = [(1,-1,0),
	# 		 (0,0,0),
	# 		 (2,0,0),
	# 		 (1,1,0)]

	board = Board()
	p = 1
	for tile in state:
		board.add( Ant(p,tile,screen))
		p = -p
	board.add(queen)

	
	moves = board.valid_placements(1)
	print(moves)


	options = []
	for move in moves:
		temp = Hex(move,screen,color = (0,255,0))
		options.append(temp)


	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		screen.fill((250,250,250))
		board.draw()
		for option in options:
			option.draw()
		pygame.display.flip()