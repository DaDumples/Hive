from Hive import *
import pygame
import numpy
import time
import sys


win_size = (1080,720)
pygame.init()
screen = pygame.display.set_mode(win_size)

def draw_everything(obstacles, highlights, screen):
	screen.fill((255,255,255))
	for Hex in obstacles.values():
		Hex.draw()
	for Hex in highlights.values():
		Hex.draw()
	pygame.display.flip()


def highlight_hexes(coords):
	hexs = {}
	for coord in coords:
		temp = Hex(coord, screen)
		temp.color = (0,255,0)
		hexs[coord] = temp
	return hexs


state = [(0,1,0),
			 (1,-1,0),
			 (0,-1,0),
			 (-1,1,0),
			 (2,-2,0),
			 (1,-3,0),
			 (-1,-1,0),
			 (2,-3,0)]

obstacles = {}
for x in state:
	temp = Hex(x,screen)
	temp.color = (255,0,0)
	obstacles[x] = temp

seed = (0,-3,0)
obstacles[seed] = Hex(seed,screen,color = (0,0,255))

highlights = {}

seed_tiles = [seed]
prev_moves = []
count = 0
while (len(seed_tiles) != 0) and (count < 3): #While there are still valid tiles that are new
	highlights = highlight_hexes(seed_tiles)
	draw_everything(obstacles, highlights, screen)
	time.sleep(1)

	new_tiles = []
	
	for tile in seed_tiles:
		for x in get_adjacent_valid_vacancies(tile, state):
			if can_squeeze(tile, x, state) and not is_jump(tile, x, state) and (not x in prev_moves):
				new_tiles.append(x)
				
	prev_moves = seed_tiles.copy()
	seed_tiles = new_tiles.copy()

	print(len(seed_tiles))
	print(count)
	count +=1

highlights = highlight_hexes(seed_tiles)
draw_everything(obstacles, highlights, screen)
time.sleep(1)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()