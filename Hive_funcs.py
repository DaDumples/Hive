import pygame
import sys
from numpy import *

def adjacent_tiles(pos):
	x = pos[0]
	y = pos[1]
	z = pos[2]
	return [(x+1, y,   z),
		    (x-1, y,   z),
		    (x,   y+1, z),
		    (x,   y-1, z),
		    (x-1, y+1, z),
		    (x+1, y-1, z)]

def can_squeeze(p1,p2,state):
	direction = (p2[0] - p1[0], p2[1] - p1[1])
	if direction == (1,0):
		left = (p1[0]+0, p1[1]+1, p1[2])
		right = (p1[0]+1,p1[1]-1, p1[2])
		if (left in state) and (right in state):
			return False
	elif direction == (1,-1):
		left = (p1[0]+1, p1[1]+0, p1[2])
		right = (p1[0]+0,p1[1]-1, p1[2])
		if (left in state) and (right in state):
			return False
	elif direction == (0,-1):
		left = (p1[0]+1, p1[1]-1, p1[2])
		right = (p1[0]-1,p1[1]+0, p1[2])
		if (left in state) and (right in state):
			return False
	elif direction == (-1,-0):
		left = (p1[0]+0, p1[1]-1, p1[2])
		right = (p1[0]-1,p1[1]+1, p1[2])
		if (left in state) and (right in state):
			return False
	elif direction == (-1,1):
		left = (p1[0]-1, p1[1]+0, p1[2])
		right = (p1[0]+0,p1[1]+1, p1[2])
		if (left in state) and (right in state):
			return False
	elif direction == (0,1):
		left = (p1[0]-1, p1[1]+1, p1[2])
		right = (p1[0]+1,p1[1]+0, p1[2])
		if (left in state) and (right in state):
			return False
	else:
		print('can_squeeze takes two adjacent points bro.')
		print('These are at a distance of: '+str(direction))
		return False
	return True

def is_jump(p1,p2,state):
	direction = (p2[0] - p1[0], p2[1] - p1[1])
	if direction == (1,0):
		left = (p1[0]+0, p1[1]+1, p1[2])
		right = (p1[0]+1,p1[1]-1, p1[2])
		if (left in state) or (right in state):
			return False
	elif direction == (1,-1):
		left = (p1[0]+1, p1[1]+0, p1[2])
		right = (p1[0]+0,p1[1]-1, p1[2])
		if (left in state) or (right in state):
			return False
	elif direction == (0,-1):
		left = (p1[0]+1, p1[1]-1, p1[2])
		right = (p1[0]-1,p1[1]+0, p1[2])
		if (left in state) or (right in state):
			return False
	elif direction == (-1,-0):
		left = (p1[0]+0, p1[1]-1, p1[2])
		right = (p1[0]-1,p1[1]+1, p1[2])
		if (left in state) or (right in state):
			return False
	elif direction == (-1,1):
		left = (p1[0]-1, p1[1]+0, p1[2])
		right = (p1[0]+0,p1[1]+1, p1[2])
		if (left in state) or (right in state):
			return False
	elif direction == (0,1):
		left = (p1[0]-1, p1[1]+1, p1[2])
		right = (p1[0]+1,p1[1]+0, p1[2])
		if (left in state) or (right in state):
			return False
	else:
		print('is_jump takes two adjacent points bro.')
		print('These are at a distance of: '+str(direction))
		return True
	return True

def unit_rotate(direct, direct_string, num_rots = 1):
	temp = list(direct)
	if direct_string.lower() == 'left':
		for i in range(num_rots):
			z = -(temp[0] + temp[1])
			temp[0] = -temp[1]
			temp[1] = -z
	elif direct_string.lower() == 'right':
		for i in range(num_rots):
			z = -(temp[0] + temp[1])
			temp[1] = -temp[0]
			temp[0] = -z
	else:
		print('What direction did you mean? '+str(direct_string))
			

	return (temp[0], temp[1])

def is_contiguous(state):
	floor_tiles = [x for x in state if x[2] == 0]
	seed = floor_tiles[0] #random starting tile
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

def get_adjacent_valid_vacancies(pos,state):
	open_tiles = []
	for tile in adjacent_tiles(pos):
			if (tile not in state): #if the tile is not occupied and hasnt already been counted
				for anchor_tile in adjacent_tiles(tile):
					if anchor_tile == (pos): #We arent interested in the center tile
						continue
					if (anchor_tile in state) and (tile not in open_tiles): #if the vacant tile is adjacent to a tile and is new
						open_tiles.append(tile)
						break
	return open_tiles

class Hex():

	def __init__(self, pos, screen, im_file = None, color = (180,180,180), linewidth = 0):
		win_size = pygame.display.get_surface().get_size()
		if len(pos) == 2:
			self.pos = (pos[0],pos[1],0)
		elif len(pos) == 3:
			self.pos = pos

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

		pixelpos = self.hex_to_pix@array([self.pos[0],self.pos[1]]) #position of the hex center in pixels

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

	def move(self, position):
		self.position = position



class Queen(Hex):

	def __init__(self, player, pos, screen):
		if player == 1:
			color = (210,180,140)
			linewidth = 0
		elif player == -1:
			color = (25,25,25)
			linewidth = 0
		self.player = player
		self.under_beetle = False
		Hex.__init__(self, pos, screen, 'bee.png', color, linewidth)

	def valid_moves(self, pieces):

		if self.under_beetle:
			return []

		#evaluate wheter the board is still contiguous
		state = list(pieces.keys())
		state.remove(self.pos)
		if not is_contiguous(state):
			return [] #There are no valid moves

		valid_moves = [] #all the tiles that you can slide into that dont disconnect the board
		#find all unoccupied pieces adjacent to another piece that the piece can move to
		open_tiles = get_adjacent_valid_vacancies(self.pos, pieces) #all the tiles that you could place the tile

		#Check to see if you can squeeze into these spots
		for tile in open_tiles:
			if can_squeeze(self.pos,tile,pieces) and not is_jump(self.pos, tile, pieces):
				valid_moves.append(tile)
		
		return valid_moves

	def is_alive(self,state):
		for tile in adjacent_tiles(self.pos):
			if tile not in state:
				return True
		return False




class Ant(Hex):

	def __init__(self, player, pos, screen):
		if player == 1:
			color = (210,180,140)
			linewidth = 0
		elif player == -1:
			color = (25,25,25)
			linewidth = 0
		self.player = player
		self.under_beetle = False
		Hex.__init__(self, pos, screen, 'ant.png', color, linewidth)

	def valid_moves(self, state):

		if self.under_beetle:
			return []

		#evaluate wheter the board is still contiguous
		move_state = list(state.keys())
		move_state.remove(self.pos)
		if not is_contiguous(move_state):
			return [] #There are no valid moves

		valid_moves = []
		seed_tiles = [self.pos]

		while len(seed_tiles) != 0: #While there are still valid tiles that are new
			for tile in seed_tiles:
				new_tiles = get_adjacent_valid_vacancies(tile, move_state)
				if self.pos in new_tiles:
					new_tiles.remove(self.pos)

				dead_end = False
				possibilities = []
				for new_tile in new_tiles: #for each tile adjacent to the tile being checked
					if not can_squeeze(tile, new_tile, move_state): #If this tile is adjacent to a gap
						dead_end = True #the cant can not cross gaps
						break
					elif (new_tile not in valid_moves) and not is_jump(tile, new_tile, move_state):
						#if the tile is new and you dont have to jump to get it
						possibilities.append(new_tile)
				if not dead_end:
					#if the tile was not a dead end, add its valid adjacent tiles to the search space
					seed_tiles += possibilities
					valid_moves += possibilities
				seed_tiles.remove(tile)

		return valid_moves

class Beetle(Hex):

	def __init__(self, player, pos, screen):
		if player == 1:
			color = (210,180,140)
			linewidth = 0
		elif player == -1:
			color = (25,25,25)
			linewidth = 0
		self.player = player
		self.under_beetle = False
		self.stack_pos = 0
		Hex.__init__(self, pos, screen, 'ant.png', color, linewidth)

	def valid_moves(self, state):
		#evaluate wheter the board is still contiguous

		if self.under_beetle: #cant move if youre under a beetle
			return []

		state = state.copy()
		state.remove(self.pos)
		if not is_contiguous(state):
			return [] #There are no valid moves

		valid_moves = [] #all the tiles that you can slide into that dont disconnect the board
		#find all unoccupied pieces adjacent to another piece that the piece can move to
		open_tiles = get_adjacent_valid_vacancies(self.pos, state) #all the tiles that you could place the tile
		for tile in adjacent_tiles(self.pos, state): #add tiles that already have a bug on them since the
													 #the beetle can move over other peices
			if tile in state:
				open_tiles.append(tile)

		#If you are on ground level, check to see if you can squeeze into these spots
		for tile in open_tiles:
			if can_squeeze(self.pos,tile,pieces) and not is_jump(self.pos, tile, pieces):
				valid_moves.append(tile)
		
		return valid_moves

class Board():

	def __init__(self):
		self.turn = 1
		self.state = {}
		#State will be an dictionary
		#The keys are a tuple of position
		#The values are the objects themselves
		self.queen_pos = None
		self.queen_placed = False

	def valid_placements(self, player):
		valid_tiles = []
		#find all the tiles you are allowed to place next to
		player_tiles = [x.pos for x in self.state.values()
						 if x.player == player and x.pos[2] == 0]
		for player_tile in player_tiles:
			#all the open tiles adjacent to a 
			candidate_tiles = [x for x in adjacent_tiles(player_tile)
								 if x not in self.state]

			for tile in candidate_tiles:
				#if we have already confirmed it move on
				if tile in valid_tiles:
					continue

				valid = True
				for check in adjacent_tiles(tile):
					# if one tile adjacent to a candidate is an opponents
					# it is not a valid location to place a tile
					if check in self.state:
						if self.state[check].player != player:
							valid = False
							break
				#if its valid add it to the list
				if valid:
					valid_tiles.append(tile)

		return valid_tiles

	def add(self, game_piece):
		#if pos in self.valid_placements():
		self.state[game_piece.pos] = game_piece


	def move(self, start_pos, end_pos):
		if start_pos in self.state:
			self.state[start_pos].move(start_pos, end_pos)
			self.state[end_pos] = self.state.pop(start_pos) #delete old position and add new position

	def draw(self, mousepos = None):
		for piece in self.state.values():
			piece.draw()
