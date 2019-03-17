from Hive import *
import pygame
import numpy
import time
import sys


win_size = (1080,720)
pygame.init()
screen = pygame.display.set_mode(win_size)

def draw_everything(Hexs, screen):
	screen.fill((255,255,255))
	for Hex in Hexs:
		Hexs[Hex].draw()
	pygame.display.flip()

def highlight_hexes(Hexs, searching, checked):
	for Hex in Hexs:
		Hexs[Hex].color = (255,0,0)

	for tile in checked:
		Hexs[tile].color = (0,255,0)

	for tile in searching:
		Hexs[tile].color = (0,0,255)
	return Hexs


state = [(0,0),
		 (1,0),
		 (2,0),
		 (1,-1),
		 (2,-1),
		 (2,-2),
		 (1,-2),
		 (0,-2),
		 (0,-1),
		 (-1,0),
		 (-2,0),
		 (-2,1),
		 (-1,1),
		 (0,1),
		 (0,4)]

Hexs = {}
for tile in state:
	temp = Hex(tile,screen)
	temp.color = (255,0,0)
	Hexs[tile] = temp

draw_everything(Hexs,screen)
time.sleep(1)

seed = state[0] #random starting tile
contiguous_tiles = [seed] #a list of all tiles that are touching the starting tile
new_tiles = [] #tiles on the edge of the search

Hexs[seed].color = (0,255,0)
draw_everything(Hexs, screen)
time.sleep(1)

start = time.time()
for tile in adjacent_tiles(seed):
	if tile in state: #for every existing tile adjacent to the seed
		new_tiles.append(tile) #add the adjacent tile to the search
		contiguous_tiles.append(tile) #add the adjacent tile to the list of touching tiles
Hexs = highlight_hexes(Hexs, new_tiles, contiguous_tiles)
draw_everything(Hexs, screen)
time.sleep(1)

while len(new_tiles) != 0: #until there are no tiles left to check
	for tile in new_tiles: #for each tile to check
		for adj_tile in adjacent_tiles(tile): #check each tile adjacent to it
			if (adj_tile in state) and (adj_tile not in contiguous_tiles): #if it is filled and not already counted
				new_tiles.append(adj_tile) #add it to the search pile
				contiguous_tiles.append(adj_tile) #add it to the total touching tiles
		new_tiles.remove(tile) #Now that it is searched remove this tile from the search pool
		Hexs = highlight_hexes(Hexs, new_tiles, contiguous_tiles)
		draw_everything(Hexs, screen)
		time.sleep(1)

stop = time.time()
print('Done. Time elapsed: ')
print(stop-start)
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
