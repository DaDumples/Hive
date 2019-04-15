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

def rotate(direct, num_rots = 1, direct_string = 'left'):
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

class Queen():

	def __init__(self, player, pos):
		self.player = player
		self.under_beetle = False
		self.bug = 'queen'

		if len(pos) == 2:
			self.pos = (pos[0], pos[1], 0)
		elif len(pos) == 3:
			self.pos = pos

		if player == 1:
			self.color = (210,180,140)		
		elif player == -1:
			self.color = (25,25,25)

		self.linecolor = (255,215,0)
		self.im = pygame.image.load('bee.png').convert()
		self.im_size = self.im.get_rect().size


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


class Ant():

	def __init__(self, player, pos):
		self.player = player
		self.under_beetle = False
		self.bug = 'ant'

		if len(pos) == 2:
			self.pos = (pos[0], pos[1], 0)
		elif len(pos) == 3:
			self.pos = pos

		if player == 1:
			self.color = (210,180,140)
		elif player == -1:
			self.color = (25,25,25)

		self.linecolor = (0,191,255)
		self.im = pygame.image.load('ant.png').convert()
		self.im_size = self.im.get_rect().size

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


class Beetle():

	def __init__(self, player, pos):

		self.player = player
		self.under_beetle = False
		self.bug = 'beetle'

		if len(pos) == 2:
			self.pos = (pos[0], pos[1], 0)
		elif len(pos) == 3:
			self.pos = pos

		if player == 1:
			self.color = (210,180,140)
		elif player == -1:
			self.color = (25,25,25)

		self.linecolor = (153,50,204)
		self.im = pygame.image.load('beetle.png').convert()
		self.im_size = self.im.get_rect().size

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


class Spider():

	def __init__(self, player, pos):

		self.player = player
		self.under_beetle = False
		self.bug = 'spider'

		if len(pos) == 2:
			self.pos = (pos[0], pos[1], 0)
		elif len(pos) == 3:
			self.pos = pos

		if player == 1:
			self.color = (210,180,140)
		elif player == -1:
			self.color = (25,25,25)

		self.linecolor = (139,69,19)
		self.im = pygame.image.load('spider.png').convert()
		self.im_size = self.im.get_rect().size

	def valid_moves(self, state):

		if self.under_beetle:
			return []

		#evaluate wheter the board is still contiguous
		state = state.copy()
		state.pop(self.pos)
		if not is_contiguous(state):
			return [] #There are no valid moves


		seed_tiles = [self.pos]
		prev_moves = []
		count = 0
		while (len(seed_tiles) != 0) and (count < 3): #while we still have tiles to check
													  #while we have moved less than three spaces
			new_tiles = []
			
			for tile in seed_tiles:
				for x in get_adjacent_valid_vacancies(tile, state): #get the open spaces around each seed
					if can_squeeze(tile, x, state) and not is_jump(tile, x, state) and not (x in prev_moves):
						#if you can get to this tile, and you are moving forwards append it to the new tiles list
						new_tiles.append(x)
			prev_moves = seed_tiles
			seed_tiles = new_tiles #the new seeds are the possible moves from the last ones
			count +=1

		valid_moves = list(set(seed_tiles))

		return valid_moves


class Grasshopper():

	def __init__(self, player, pos):
		self.player = player
		self.under_beetle = False
		self.bug = 'grasshopper'

		if len(pos) == 2:
			self.pos = (pos[0], pos[1], 0)
		elif len(pos) == 3:
			self.pos = pos

		if player == 1:
			self.color = (210,180,140)
		elif player == -1:
			self.color = (25,25,25)

		self.linecolor = (0,128,0)
		self.im = pygame.image.load('grasshopper.png').convert()
		self.im_size = self.im.get_rect().size

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

	def __init__(self, state = None):
		#screen is a pygame screen object
		#bounds is the coordinates on the screen that the
		#board will be displayed
		self.turn = 1
		if state == None:
			self.state = {}
		else:
			self.state = state
		#State will be an dictionary
		#The keys are a tuple of position
		#The values are the objects themselves
		self.player = 1
		self.remaining_pieces = {}
		self.remaining_pieces[1] = {'queen':1,
									'spider':2,
									'beetle':2,
									'grasshopper':3,
									'ant':3}
		self.remaining_pieces[-1] = {'queen':1,
									'spider':2,
									'beetle':2,
									'grasshopper':3,
									'ant':3}

	def valid_placements(self):

		if self.turn == 1:
			return [(0,0,0)]
		if self.turn == 2:
			return adjacent_tiles((0,0,0))


		valid_tiles = []
		#find all the tiles you are allowed to place next to
		#get all the locations for the coordinates whose top tile is that players
		#only look at the tiles on the bottom layer
		player_tiles = [x for x in self.state
						 if (self.state[top_tile(x,self.state)].player == self.player) and
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
						if self.state[tippy_top].player != self.player:
							valid = False
							break
				#if its valid add it to the list
				if valid:
					valid_tiles.append(tile)

		return valid_tiles

	def vacant_tiles(self):
		if self.turn == 1:
			return [(0,0,0)]

		vacancies = []
		for tile in self.state:
			if tile[2] == 0:
				for adj_tile in adjacent_tiles(tile):
					if (not adj_tile in self.state) and (not adj_tile in vacancies):
						vacancies.append(adj_tile)

		return vacancies

	def possible_moves(self):
		moves = {}
		for piece in [x for x in self.state.values() if x.player == self.player]:
			piece_moves = piece.valid_moves(self.state)
			if len(piece_moves) != 0:
				moves[piece.pos] = piece_moves.copy()
				#print('Move '+piece.bug+' '+str(piece_moves))

		places = self.valid_placements()
		if len(places) != 0:
			for piece in self.remaining_pieces[self.player]:
				if self.remaining_pieces[self.player][piece] != 0:
					moves[piece] = places.copy()
					#print('Place '+str(piece)+' '+str(places))
		#print(len(moves))
		return moves

	def add_piece(self, piece_type, pos):
		self.remaining_pieces[self.player][piece_type] -= 1

		if piece_type.lower() == 'queen':
			game_piece = Queen(self.player, pos)
		elif piece_type.lower() == 'ant':
			game_piece = Ant(self.player, pos)
		elif piece_type.lower() == 'spider':
			game_piece = Spider(self.player, pos)
		elif piece_type.lower() == 'beetle':
			game_piece = Beetle(self.player, pos)
		elif piece_type.lower() == 'grasshopper':
			game_piece = Grasshopper(self.player, pos)
		else:
			print('Unknown piece: '+str(piece_type))
			return False

		if len(pos) == 3:
			if pos[2] != 0:
				self.state[(pos[0], pos[1], pos[2]-1)].under_beetle = True

		self.state[game_piece.pos] = game_piece
		self.turn +=1
		self.player = -self.player

	def move_piece(self, start_pos, end_pos):
		if start_pos in self.state:

			self.state[start_pos].pos = end_pos #update the piece objects position
			self.state[end_pos] = self.state.pop(start_pos) #delete old position and add new position
			#deal with beetle logic. Free up the tile it moved from, and lock down the tile it moved to
			if end_pos[2] != 0:
				self.state[(end_pos[0], end_pos[1], end_pos[2]-1)].under_beetle = True
			if start_pos[2] != 0:
				self.state[(start_pos[0], start_pos[1], start_pos[2]-1)].under_beetle = False

		self.turn +=1
		self.player = -self.player


	def move(action):
		#action = ('mov', (x,y,z), (x,y,z))
		#action = ('add', 'beetle', (x,y,z))
		if action[0] == 'add':
			bug = action[1]
			pos = action[2]
			self.add_piece(bug, pos)
		elif action[0] == 'mov':
			pos1 = action[1]
			pos2 = action[2]
			self.move_piece(pos1,pos2)

		return self.state


	def is_game_over(self):
		if len(self.possible_moves()) == 0:
			return True, 0

		winners = []
		for piece in self.state.values():
			if piece.bug == 'queen':
				alive = False
				for tile in adjacent_tiles(piece.pos):
					if tile not in self.state:
						alive = True
						break
				if not alive:
					winners.append(piece.player)

		if len(winners) == 2:
			return True, 0
		elif len(winners) == 0:
			return False, 0
		elif winners[0] == 1:
			return True, 1
		else:
			return True, -1



class Gui():

	def __init__(self, screen, board_bounds = (0,0,1080,720), menu_bounds = (0,0,160,720)):
		self.board_bounds = board_bounds
		self.screen = screen
		self.board_width = board_bounds[2] - board_bounds[0]
		self.board_height = board_bounds[3] - board_bounds[1]
		self.board_xoffset = board_bounds[0]
		self.board_yoffset = board_bounds[1]
		self.camerapos = [0,0]
		self.hex_rad = (board_bounds[3] - board_bounds[1])/22

		self.hex_to_pix = array([[2*self.hex_rad, 2*self.hex_rad*cos(pi/3)],
				   				 [0, 		-2*self.hex_rad*sin(pi/3)]])
		self.pix_to_hex = inv(self.hex_to_pix)
		self.hex_points = [(self.hex_rad*cos(x), self.hex_rad*sin(x)) for x in linspace(0,2*pi, 7)+pi/6]

		pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
		self.font = pygame.font.SysFont('Arial', 30)

		self.mode = None
		#modes:
		#add - The next click will add a tile
		#sel - next click will select a tile to move
		#mov - the next click will move the selected piece
		#None - Clicking does nothing
		self.selected_piece = None
		self.adding_type = None

	def cart_to_hex(self, cart_pos):
		x, y = cart_pos
		#the board screen will be a subsection of the entire screen
		#get the pixel distance from the center of teh subscreen to the mouse
		x -= self.board_width/2 + self.board_xoffset
		y -= self.board_height/2 + self.board_yoffset
		#add the position of the camera to the pixelpos to account
		#for the translated view
		x += self.camerapos[0]
		y += self.camerapos[1]
		temp = rint(self.pix_to_hex@array([x,y]))
		return (int(temp[0]), int(temp[1]), 0)

	def hex_to_cart(self, hex_pos):
		pix_pos = self.hex_to_pix@array([hex_pos[0], hex_pos[1]])
		x, y = pix_pos
		x -= self.camerapos[0]
		y -= self.camerapos[1]
		x += self.board_width/2 + self.board_xoffset
		y += self.board_height/2 + self.board_yoffset
		return (x, y)

	def draw_outline(self, hex_pos, color):
		center = self.hex_to_cart(hex_pos)
		vertical_offset = hex_pos[2]*7
		pointlist = [(x*1.1 + center[0] + vertical_offset, y*1.1 + center[1] - vertical_offset) for x, y in self.hex_points]
		pygame.draw.polygon(self.screen, color, pointlist, 4)

	def draw_piece(self, tile):

		center = self.hex_to_cart(tile.pos)
		vertical_offset = tile.pos[2]*7
		pointlist = [(x + center[0] + vertical_offset, y + center[1] - vertical_offset) for x, y in self.hex_points]
		im_pos = (center[0]-tile.im_size[0]/2 + vertical_offset,
				  center[1]-tile.im_size[1]/2 - vertical_offset)

		pygame.draw.polygon(self.screen, tile.color, pointlist, 0)
		pygame.draw.polygon(self.screen, tile.linecolor, pointlist, 4)
		self.screen.blit(tile.im, im_pos)

	def draw_board(self, board, mousepos):

		green_tiles = []
		if self.mode == 'add':
			green_tiles = board.valid_placements()
		if self.mode == 'sel':
			green_tiles = [x for x in board.state if (not board.state[x].under_beetle) and (board.state[x].player == board.player)]
		if self.mode == 'mov':
			green_tiles = self.selected_piece.valid_moves(board.state)

		grey_tiles = board.vacant_tiles()
		for grey in grey_tiles:
			self.draw_outline(grey, (80,80,80))

		hex_pos = self.cart_to_hex(mousepos)
		if hex_pos in board.state:
			top = top_tile(hex_pos, board.state)
			hex_pos = (hex_pos[0], hex_pos[1], top[2])
			if (self.selected_piece != None) and (self.selected_piece.bug == 'beetle'):
				hex_pos = (hex_pos[0], hex_pos[1], top[2]+1)

		if hex_pos in green_tiles:
			outline_color =  (0,255,0)
		else:
			outline_color = (255,0,0)

		#draw the tiles from bottom to top
		level = 0
		bottom_tiles = [tile for tile in board.state.values() if tile.pos[2] == level]
		if board.turn == 1:
			self.draw_outline(hex_pos, outline_color)

		while (len(bottom_tiles) != 0):

			if hex_pos[2] == level:
				self.draw_outline(hex_pos, outline_color)

			for tile in bottom_tiles:
				self.draw_piece(tile)
			level += 1
			bottom_tiles = [tile for tile in board.state.values() if tile.pos[2] == level]
		if hex_pos[2] >= level:
			self.draw_outline(hex_pos, outline_color)



		textsurface = self.font.render('Player: '+str(board.player), False, (0, 0, 0))
		self.screen.blit(textsurface,(960,0))
		textsurface = self.font.render('Mode: '+str(self.mode), False, (0, 0, 0))
		self.screen.blit(textsurface,(760,0))
		Qs = board.remaining_pieces[board.player]['queen']
		As = board.remaining_pieces[board.player]['ant']
		Ss = board.remaining_pieces[board.player]['spider']
		Bs = board.remaining_pieces[board.player]['beetle']
		Gs = board.remaining_pieces[board.player]['grasshopper']
		bottom_text = '[Q]ueens: '+str(Qs)+'  [A]nts: '+str(As)+'  [S]piders: '+str(Ss)+'  [B]eetles: '+str(Bs)+'  [G]rasshoppers: '+str(Gs)+'  [M]ove'
		textsurface = self.font.render(bottom_text, False, (0, 0, 0))
		self.screen.blit(textsurface,(0,680))

		is_won, loser = board.is_game_over()
		if is_won:
			if loser == 0:
				textsurface = self.font.render('DRAW', False, (255, 0, 0))
				self.screen.blit(textsurface,(450,340))
			elif loser == 1:
				textsurface = self.font.render('BLACK WINS', False, (255, 0, 0))
				self.screen.blit(textsurface,(450,340))
			elif loser == -1:
				textsurface = self.font.render('WHITE WINS', False, (255, 0, 0))
				self.screen.blit(textsurface,(450,340))