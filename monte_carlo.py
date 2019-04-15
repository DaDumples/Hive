from numpy import *
import random as pyrandom
from Hive_funcs import *
import copy

class Node():

	def __init__(self, Ntot, board, state_hash, move, N = 0, Q = 0, parents = [] ):
		self.N = N
		self.Ntot = Ntot
		self.Q = Q
		self.potential = 0
		self.board = board
		self.state_hash = state_hash
		self.parents = parents
		self.move = move


	def update_NQ(self, Q):
		self.N += 1
		self.Q += Q
		self.potential = self.Q + sqrt(2*log(self.Ntot)/self.N)

	def __str__(self):
		return str(self.move) + ' ' + str(self.board.turn) + ' ' + str(self.board.player) + ' ' + str(self.parents)


class Monte_Carlo():
	def __init__(self, board):
		self.nodes = {}
		self.hash_table = {}
		self.num_sims = 0

		random.seed(10799759)
		bugs = ['queen', 'ant', 'spider', 'grasshopper', 'beetle']
		positions = board.positions
		pieces = []
		for bug in bugs:
			for player in [-1, 1]:
				pieces.append((bug, player))

		for position in positions:
			self.hash_table[position] = {}
			for piece in pieces:
				self.hash_table[position][piece] = pyrandom.getrandbits(64)



	def hash_state(self, state):
		H = 0
		for pos in state:
			piece = (state[pos].bug, state[pos].player)
			H = H^self.hash_table[pos][piece]

		return H

	def hash_move(self, move, state, player):
		h1 = self.hash_state(state)
		if move[0] == 'pass':
			return h1
		elif move[0] == 'mov':
			#hash out the old location
			h2 = h1 ^ self.hash_table[move[1]][(state[move[1]].bug, player)]
			#hash in the new location, same piece name and player
			h2 = h1 ^ self.hash_table[move[2]][(state[move[1]].bug, player)]
		else:
			#hash in the added piece
			h2 = h1 ^ self.hash_table[move[2]][(move[1], player)]

		return h2


	def simulate(state):
		return pyrandom.choice([1,-1]) #needs to be implemented

	def get_move(self, input_board):

		root_state = input_board.state #Need to add this to Board
		root_hash = self.hash_state(root_state)
		player_evaluated = input_board.player
		
		#keep relevant nodes from the last run
		nodes = {}

		#create the first few child nodes
		for move in input_board.possible_moves():
			temp = copy.copy(input_board)
			temp.move(move)
			print(input_board.state)
			print('')

			move_hash = self.hash_state(temp.state)
			if not move_hash in nodes:
				nodes[move_hash] = Node(0, temp, move_hash, move)
		#start exploring the nodes, only explore 500
		player_factor = input_board.player # 1 or -1
		num_moves = 500
		count = 0
		while count < num_moves:
			count += 1

			#find the node with the higest potential
			max_potential = list(nodes.keys())[0]
			for node in nodes:
				if nodes[node].potential*player_factor >= nodes[max_potential].potential*player_factor:
					max_potential = node

			print(nodes[max_potential])
			print(' ')

			#get a list of moves from this node
			node_board = nodes[max_potential].board
			node_turn = node_board.turn
			node_player = node_board.player
			temp_board = node_board.copy_board()
			moves = temp_board.possible_moves()
			print(moves)
			print(temp_board.player)
			#make sure non of the moves are already known
			print(' ')
			for move in moves:
				move_hash = self.hash_move(move, node_board.state, node_player)
				if move_hash in nodes:
					moves.pop(move)

			#pick a random move
			move = pyrandom.choice(moves)
			#play it
			new_state = temp_board.move(move)
			move_hash = self.hash_state(new_state)


			score = self.simulate(temp_board)

			#create a new node for the move
			parents = nodes[max_potential].parents + [max_potential]
			nodes[move_hash] = Node(self.num_moves, temp_board, move_hash, move, N = 1, Q = score, parents = parents )

			#update all parent nodes
			for parent in nodes[max_potential].parents:
				nodes[parent].update_NQ(score)

			#update all nodes
			for node in nodes.values():
				node.Ntot += 1

			#update the sim count
			self.num_sims += 1

		#chose the best node explored
		#ISSUE: Since we are using the same tree for p1 and p2, Ntot is increased by both players, meaning p2 might make the best move for p1
		#probably want to make separate trees for each player
		best_choice = list(nodes.keys())[0]
		for node in nodes:
			if nodes[node].Ntot > nodes[best_choice].Ntot:
				best_choice = node

		return nodes[best_choice].move

