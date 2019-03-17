import pygame
import sys
from numpy import *

win_size = (1080,720)

def adjacent_tiles(pos):
	x = pos[0]
	y = pos[1]
	return [(x+1, y),
		    (x-1, y),
		    (x,   y+1),
		    (x,   y-1),
		    (x-1, y+1),
		    (x+1, y-1)]

def can_squeeze(p1,p2,state):
	direction = (p2[0] - p1[0], p2[1] - p1[1])
	if direction == (1,0):
		left = (p1[0]+0,p1[1]+1)
		right = (p1[0]+1,p1[1]-1)
		if (left in state) and (right in state):
			return False
	elif direction == (1,-1):
		left = (p1[0]+1,p1[1]+0)
		right = (p1[0]+0,p1[1]-1)
		if (left in state) and (right in state):
			return False
	elif direction == (0,-1):
		left = (p1[0]+1,p1[1]-1)
		right = (p1[0]-1,p1[1]+0)
		if (left in state) and (right in state):
			return False
	elif direction == (-1,-0):
		left = (p1[0]+0,p1[1]-1)
		right = (p1[0]-1,p1[1]+1)
		if (left in state) and (right in state):
			return False
	elif direction == (-1,1):
		left = (p1[0]-1,p1[1]+0)
		right = (p1[0]+0,p1[1]+1)
		if (left in state) and (right in state):
			return False
	elif direction == (0,1):
		left = (p1[0]-1,p1[1]+1)
		right = (p1[0]+1,p1[1]+0)
		if (left in state) and (right in state):
			return False
	else:
		print('can_squeeze takes two adjacent points bro.')
		print('These are at a distance of: '+str(direction))
		return False
	return True

def is_contiguous(state):
	seed = state[0] #random starting tile
	contiguous_tiles = [seed] #a list of all tiles that are touching the starting tile
	new_tiles = [] #tiles on the edge of the search
	for tile in adjacent_tiles(seed):
		if tile in state: #for every existing tile adjacent to the seed
			new_tiles.append(tile) #add the adjacent tile to the search
			contiguous_tiles.append(tile) #add the adjacent tile to the list of touching tiles

	while len(new_tiles) != 0: #until there are no tiles left to check
		for tile in new_tiles: #for each tile to check
			for adj_tile in adjacent_tiles(tile): #check each tile adjacent to it
				if (adj_tile in state) and (adj_tile not in contiguous_tiles): #if it is filled and not already counted
					new_tiles.append(adj_tile) #add it to the search pile
					contiguous_tiles.append(adj_tile) #add it to the total touching tiles
			new_tiles.remove(tile) #Now that it is searched remove this tile from the search pool

	if len(contiguous_tiles) == len(state): #if we didnt find all the tiles in our search, there must be a gap
		return True
	else:
		return False



class Hex():

	def __init__(self, pos, screen, im_file = None, color = (180,180,180), linewidth = 0):
		self.x = pos[0]
		self.y = pos[1]
		self.pos = pos
		self.z = -(pos[0] + pos[1]) #for whenever you want to use a three axis coordinate system
		self.r = win_size[1]*.95/22 #radius is so that 22 hexes can
									#fit on the screen with some margin
									#r is the apothem of the hexagon
		self.screen = screen
		self.color = color
		self.linewidth = linewidth

		radius = self.r*.98
		points =[(radius*cos(x), radius*sin(x)) for x in linspace(0,2*pi, 7)+pi/6]
		self.hex_to_pix = array([[2*self.r, 2*self.r*cos(pi/3)],
				   				 [0, 		-2*self.r*sin(pi/3)]])

		pixelpos = self.hex_to_pix@array([self.x,self.y]) #position of the hex center in pixels

		self.pointlist = [(int(x + win_size[0]/2 + pixelpos[0]), int(y + win_size[1]/2 + pixelpos[1])) for x, y in points]

		if im_file == None:
			self.im = None
		else:
			self.im = pygame.image.load(im_file).convert()
			size = self.im.get_rect().size
			self.im_pos = (pixelpos[0] - size[0]/2 + win_size[0]/2, pixelpos[1] - size[1]/2 + win_size[1]/2)

	def draw(self):
		pygame.draw.polygon(self.screen, self.color, self.pointlist, self.linewidth)
		if self.im != None:
			self.screen.blit(self.im, self.im_pos)

class Queen(Hex):

	def __init__(self, player, pos, screen):
		if player == 1:
			color = (210,180,140)
			linewidth = 0
		elif player == -1:
			color = (25,25,25)
			linewidth = 0
		self.player = player
		Hex.__init__(self, pos, screen, 'bee.png', color, linewidth)

	def valid_moves(self, pieces):

		open_tiles = [] #all the tiles that you could place the tile
		accessible_tiles = [] #all the tiles that you can slide into
		valid_moves = [] #all the tiles that you can slide into that dont disconnect the board
		#find all unoccupied pieces adjacent to another piece that the piece can move to
		for tile in adjacent_tiles(self.pos):
			if (tile not in pieces) : #if the tile is not occupied and hasnt already been counted
				for anchor_tile in adjacent_tiles(tile):
					if anchor_tile == (self.pos):
						continue
					if (anchor_tile in pieces) and (tile not in open_tiles): #if the vacant tile is adjacent to a tile that is not the queen
						print(tile)
						open_tiles.append(tile)

		print('All Open Tiles:')
		print(open_tiles)

		#Check to see if you can squeeze into these spots
		
		for tile in open_tiles:
			if can_squeeze(self.pos,tile,pieces):
				accessible_tiles.append(tile)

		#for each potential state created by a move, evaluate wheter the board is still contiguous
		for move in accessible_tiles:
			state = pieces.copy()
			state.remove(self.pos)
			state.append(move) #If the board must stay connected while moving remove this
			print('Possible state:')
			print(state)
			if is_contiguous(state):
				valid_moves.append(move) #remove this move because it must violate the rules

		return valid_moves


if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode(win_size)



	player = Queen(1,(1,0),screen)


	state = [(0,1),
			 (1,-1),
			 (0,-1)]

	state.append(player.pos)
	obstacles = []
	for tile in state:
		obstacles.append(Hex(tile,screen))

	moves = player.valid_moves(state)
	options = []
	for move in moves:
		temp = Hex(move,screen)
		temp.color = (0,255,0)
		options.append(temp)


	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		screen.fill((250,250,250))
		
		for obstacle in obstacles:
			obstacle.draw()
		player.draw()
		for option in options:
			option.draw()
		pygame.display.flip()