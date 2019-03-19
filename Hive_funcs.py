import pygame
import sys
from numpy import *
from numpy.linalg import *



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
	contiguous_tiles = [floor_tiles[0]] #a list of all tiles that are touching the starting tile
	new_tiles = [floor_tiles[0]] #tiles on the edge of the search

	while len(new_tiles) != 0: #until there are no tiles left to check
		for tile in new_tiles: #for each tile to check
			for adj_tile in adjacent_tiles(tile): #check each tile adjacent to it
				if (adj_tile in state) and (adj_tile not in contiguous_tiles): #if it is filled and not already counted
					new_tiles.append(adj_tile) #add it to the search pile
					contiguous_tiles.append(adj_tile) #add it to the total touching tiles
			new_tiles.remove(tile) #Now that it is searched remove this tile from the search pool

	if len(contiguous_tiles) == len(floor_tiles): #if we didnt find all the tiles in our search, there must be a gap
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

def top_tile(pos, state):
	on_top = not state[pos].under_beetle
	top_tile = pos
	while not on_top:
		top_tile = (top_tile[0],top_tile[1], top_tile[2]+1)
		on_top = not state[top_tile].under_beetle
	return top_tile



class Outline():

	def __init__(self, pos, screen = None, color = (180,180,180), linewidth = 4):
		self.pos = pos
		self.screen = screen
		self.color = color
		self.linewidth = linewidth
		self.win_size = pygame.display.get_surface().get_size()
		self.r = self.win_size[1]*.95/44
		self.hex_points = [(self.r*cos(x), self.r*sin(x)) for x in linspace(0,2*pi, 7)+pi/6]

		self.hex_to_pix = array([[2*self.r, 2*self.r*cos(pi/3)],
				   				 [0, 		-2*self.r*sin(pi/3)]])
		self.pixelpos = self.hex_to_pix@array([self.pos[0],self.pos[1]]) #position of the hex center in pixels
		self.pointlist = [[int(x + self.win_size[0]/2 + self.pixelpos[0]),
						   int(y + self.win_size[1]/2 + self.pixelpos[1])] for x, y in self.hex_points]

	def draw(self):
		if self.screen != None:
			pygame.draw.polygon(self.screen, self.color, self.pointlist, self.linewidth)






class Hex():


	def __init__(self, pos, screen = None, im_file = None, color = (180,180,180), linecolor = (0,0,0), linewidth = 2):
		self.win_size = pygame.display.get_surface().get_size()
		if len(pos) == 2:
			self.pos = (pos[0],pos[1],0)
		elif len(pos) == 3:
			self.pos = pos

		self.r = self.win_size[1]*.95/44 #radius is so that 22 hexes can
									#fit on the screen with some margin
									#r is the apothem of the hexagon
		self.r_inner = self.r*.98
		self.screen = screen
		self.color = color
		self.linewidth = linewidth
		self.linecolor = linecolor
		
		self.hex_to_pix = array([[2*self.r, 2*self.r*cos(pi/3)],
				   				 [0, 		-2*self.r*sin(pi/3)]])

		self.vertical_offset = .15*self.r
		self.hex_points = [(self.r_inner*cos(x), self.r_inner*sin(x)) for x in linspace(0,2*pi, 7)+pi/6]
		self.pixelpos = self.hex_to_pix@array([self.pos[0],self.pos[1]]) #position of the hex center in pixels
		self.pointlist = [[int(x + self.win_size[0]/2 + self.pixelpos[0] + self.vertical_offset*self.pos[2]),
						   int(y + self.win_size[1]/2 + self.pixelpos[1] - self.vertical_offset*self.pos[2])] for x, y in self.hex_points]

		if im_file == None:
			self.im = None
		else:
			self.im = pygame.transform.scale(pygame.image.load(im_file).convert(),(20,20))
			self.im_size = self.im.get_rect().size
			self.im_pos = [self.pixelpos[0] - self.im_size[0]/2 + self.win_size[0]/2 + self.vertical_offset*self.pos[2],
						   self.pixelpos[1] - self.im_size[1]/2 + self.win_size[1]/2 - self.vertical_offset*self.pos[2]]

	def draw(self):
		
		if self.screen != None:
			pygame.draw.polygon(self.screen, self.color, self.pointlist, 0)
			pygame.draw.polygon(self.screen, self.linecolor, self.pointlist, self.linewidth)
			if self.im != None:
				self.screen.blit(self.im, self.im_pos)

	def move_to(self, position):
		self.pos = position
		self.pixelpos = self.hex_to_pix@array([self.pos[0],self.pos[1]]) #position of the hex center in pixels
		self.pointlist = [[int(x + self.win_size[0]/2 + self.pixelpos[0] + self.vertical_offset*self.pos[2]),
						   int(y + self.win_size[1]/2 + self.pixelpos[1] - self.vertical_offset*self.pos[2])] for x, y in self.hex_points]
		if self.im != None:
			self.im_pos = [self.pixelpos[0] - self.im_size[0]/2 + self.win_size[0]/2 + self.vertical_offset*self.pos[2],
						   self.pixelpos[1] - self.im_size[1]/2 + self.win_size[1]/2 - self.vertical_offset*self.pos[2]]

class Queen(Hex):

	def __init__(self, player, pos, screen):
		if player == 1:
			color = (210,180,140)		
		elif player == -1:
			color = (25,25,25)

		linecolor = (255,215,0)
		self.player = player
		self.under_beetle = False
		Hex.__init__(self, pos, screen, 'bee.png', color, linecolor)

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
		elif player == -1:
			color = (25,25,25)

		linecolor = (0,191,255)
		self.player = player
		self.under_beetle = False
		Hex.__init__(self, pos, screen, 'ant.png', color, linecolor)

	def valid_moves(self, state):

		if self.under_beetle:
			return []

		#evaluate wheter the board is still contiguous
		state = state.copy()
		state.pop(self.pos)
		if not is_contiguous(state):
			return [] #There are no valid moves

		valid_moves = []
		seed_tiles = [self.pos]

		while len(seed_tiles) != 0: #While there are still valid tiles that are new
			for tile in seed_tiles:
				new_tiles = get_adjacent_valid_vacancies(tile, state)
				if self.pos in new_tiles:
					new_tiles.remove(self.pos)

				dead_end = False
				possibilities = []
				for new_tile in new_tiles: #for each tile adjacent to the tile being checked
					if not can_squeeze(tile, new_tile, state): #If this tile is adjacent to a gap
						dead_end = True #the cant can not cross gaps
						break
					elif (new_tile not in valid_moves) and not is_jump(tile, new_tile, state):
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
		elif player == -1:
			color = (25,25,25)

		linecolor = (153,50,204)
		self.player = player
		self.under_beetle = False
		self.stack_pos = 0
		Hex.__init__(self, pos, screen, 'beetle.png', color, linecolor)

	def valid_moves(self, state):
		#evaluate wheter the board is still contiguous

		if self.under_beetle: #cant move if youre under a beetle
			return []

		state = state.copy()
		state.pop(self.pos)
		if not is_contiguous(state):
			return [] #There are no valid moves

		valid_moves = [] #all the tiles that you can slide into that dont disconnect the board
		#find all unoccupied pieces adjacent to another piece that the piece can move to
		for tile in adjacent_tiles((self.pos[0], self.pos[1], 0)): #add tiles that already have a bug on them since the
											  #the beetle can move over other peices
			if tile in state:
				tippy_top = top_tile(tile, state)
				valid_moves.append((tippy_top[0],tippy_top[1], tippy_top[2]+1))
			else:
				for anchor in adjacent_tiles(tile):
					if anchor in state:
						valid_moves.append(tile)
						break
		
		return valid_moves

class Spider(Hex):

	def __init__(self, player, pos, screen):
		if player == 1:
			color = (210,180,140)
		elif player == -1:
			color = (25,25,25)

		linecolor = (139,69,19)
		self.player = player
		self.under_beetle = False
		self.stack_pos = 0
		Hex.__init__(self, pos, screen, 'spider.png', color, linecolor)

	def valid_moves(self, state):

		if self.under_beetle:
			return []

		#evaluate wheter the board is still contiguous
		state = state.copy()
		state.pop(self.pos)
		if not is_contiguous(state):
			return [] #There are no valid moves


		seed_tiles = [self.pos]
		count = 0
		while (len(seed_tiles) != 0) and (count < 3): #while we still have tiles to check
													  #while we have moved less than three spaces
			new_tiles = []
			for tile in seed_tiles:
				for x in get_adjacent_valid_vacancies(tile, state): #get the open spaces around each seed
					if can_squeeze(tile, x, state) and not is_jump(tile, x, state):
						#if you can get to this tile append it to the new tiles list
						new_tiles.append(x)
			seed_tiles = new_tiles #the new seeds are the possible moves from the last ones
			count +=1

		valid_moves = list(set(seed_tiles))

		return valid_moves

class Grasshopper(Hex):

	def __init__(self, player, pos, screen):
		if player == 1:
			color = (210,180,140)
		elif player == -1:
			color = (25,25,25)

		linecolor = (0,128,0)
		self.player = player
		self.under_beetle = False
		self.stack_pos = 0
		self.directions = [(1,0)]
		Hex.__init__(self, pos, screen, 'grasshopper.png', color, linecolor)

	def valid_moves(self, state):

		if self.under_beetle:
			return []

		#evaluate wheter the board is still contiguous
		state = state.copy()
		state.pop(self.pos)
		if not is_contiguous(state):
			return [] #There are no valid moves

		valid_moves = []
		directions = [[0,1],[0,-1],
					  [1,0],[-1,0],
					  [1,-1],[-1,1]]
		for x, y in directions:
			dist = 1
			if (self.pos[0]+x, self.pos[1]+y, 0) in state: #if there is a piece to jump over
				while (x*dist+self.pos[0], y*dist+self.pos[1], 0) in state:
					#keep jumping over pieces until there is an open space
					dist += 1
				valid_moves.append((x*dist+self.pos[0], y*dist+self.pos[1], 0))

		return valid_moves


class Board():

	def __init__(self, screen, bounds = (0,0,0,0)):
		self.turn = 1
		self.state = {}
		#State will be an dictionary
		#The keys are a tuple of position
		#The values are the objects themselves
		self.player = 1
		self.hex_to_pix = Hex((0,0)).hex_to_pix
		self.pix_to_hex = inv(self.hex_to_pix)
		self.screen = screen
		self.win_size = pygame.display.get_surface().get_size()

	def cart_to_hex(self, cart_pos):
		x, y = cart_pos
		x -= self.win_size[0]/2
		y -= self.win_size[1]/2
		return rint(self.pix_to_hex@array([x,y]))

	def valid_placements(self, player):

		if self.turn == 1:
			return [(0,0,0)]


		valid_tiles = []
		#find all the tiles you are allowed to place next to
		#get all the locations for the coordinates whose top tile is that players
		#only look at the tiles on the bottom layer
		player_tiles = [x for x in self.state
						 if (self.state[top_tile(x,self.state)].player == player) and
						 self.state[x].pos[2] == 0]

		for player_tile in player_tiles:
			#all the open tiles adjacent to a 
			candidate_tiles = [x for x in adjacent_tiles(player_tile)
								 if x not in self.state]

			for tile in candidate_tiles:
				#if we have already confirmed it, move on
				if tile in valid_tiles:
					continue

				valid = True
				for check in adjacent_tiles(tile):
					# if one tile adjacent to a candidate is an opponents
					# it is not a valid location to place a tile
					if check in self.state:
						tippy_top = top_tile(check, self.state)
						if self.state[tippy_top].player != player:
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
			self.state[start_pos].move_to(end_pos)
			self.state[end_pos] = self.state.pop(start_pos) #delete old position and add new position
			if end_pos[2] != 0:
				self.state[(end_pos[0], end_pos[1], end_pos[2]-1)].under_beetle = True
			if start_pos[2] != 0:
				self.state[(start_pos[0], start_pos[1], start_pos[2]-1)].under_beetle = False

		self.turn +=1
		self.player = -self.player

	def draw(self, mousepos):

		hex_coords = self.cart_to_hex(mousepos)
		highlight = Outline((hex_coords), self.screen, color = (0,255,0))
		highlight.draw()

		#draw the tiles from bottom to top
		bottom_tiles = [tile for tile in self.state.values() if tile.pos[2] == 0]
		level = 0
		while len(bottom_tiles) != 0:
			level += 1
			for piece in bottom_tiles:
				piece.draw()
			bottom_tiles = [tile for tile in self.state.values() if tile.pos[2] == level]
