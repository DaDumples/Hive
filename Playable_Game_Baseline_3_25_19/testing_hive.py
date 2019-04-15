import pygame
import sys
from numpy import *
from Hive_funcs import *

win_size = (1080,720)

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode(win_size)

	queen = Queen(1,(1,0),screen)
	beetle = Beetle(-1,(0,4,0),screen)
	ant = Ant(-1,(2,0,0),screen)
	spider = Spider(1,(1,-2),screen)
	grasshopper = Grasshopper(-1,(0,-2,0),screen)

	state = [(0,1,0),
			 (1,-1,0),
			 (0,-1,0),
			 (-1,1,0),
			 (2,-2,0),
			 (1,-3,0),
			 (-1,-1,0),
			 (2,-3,0)]

	board = Board(screen)
	p = 1
	for tile in state:
		board.add( Ant(p,tile,screen))
		p = -p
	board.add(queen)
	board.add(beetle)
	board.add(ant)
	board.add(spider)
	board.add(grasshopper)
	board.move((2,0,0),(0,0,0))

	board.move((0,4,0),(0,1,1))
	board.move((0,1,1),(1,0,1))
	#board.move((1,0,1),(2,0,0))

	
	moves = board.valid_placements(-1)
	print(moves)


	options = []
	for move in moves:
		temp = Hex(move,screen,color = (0,255,0))
		options.append(temp)


	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		screen.fill((150,150,150))
		board.draw(pygame.mouse.get_pos())
		for option in options:
			option.draw()
		pygame.display.flip()