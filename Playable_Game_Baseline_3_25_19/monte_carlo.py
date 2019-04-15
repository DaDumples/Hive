from numpy import *
import random
from Hive_funcs import *

class Node():

	def __init__(self, N = 0, Q = 0, Ntot, state, move, state_hash, move, parents = [] ):
		self.N = N
		self.Ntot = Ntot
		self.Q = Q
		self.potential = self.update(Q)
		self.state = state
		self.state_hash = state_hash
		self.parents = parents


	def update(self, Q):
		self.N += 1
		self.Ntot += 1
		self.Q = Q
		self.potential = self.Q + sqrt(2*log(self.Ntot)/self.N)


class Monte_Carlo():
	def __init__(self):
		self.nodes = {}
		self.hash_table = {}
		self.num_sims = 0

		random.seed(a = 10799759)
		bugs = ['queen', 'ant', 'spider', 'grasshopper', 'beetle']
		positions = [] #Need to fill this our
		pieces = []
		for bug in bugs:
			for player in [-1, 1]:
				pieces.append((bug, player))

		for piece in pieces:
			self.hash_table[piece] = {}
			for position in positions:
				self.hash_table[piece][position] = random.getrandbits(64)

	def hash_state(self, state):
		pass

	def simulate(state):
		pass

	def get_move(self, board):

		root_state = board.state #Need to add this to Board
		root_hash = self.hash_state(root_state)
		
		#keep relevant nodes from the last run
		new_nodes = {}
		for node in self.nodes:
			if root_hash in self.nodes[node].parents:
				new_nodes[node] = self.nodes[node]
		self.nodes = new_nodes

		for move in board.possible_moves():
			temp_board = Board(board.state)
			move_state = temp_board.move(move)
			move_hash = self.hash_state(move_state)
			if not move_hash in self.nodes:
				new_nodes[move_hash] = Node(N = 0, Q = 0, 0, state, move, move_hash, move, parents = [])

		num_moves = 500
		count = 0
		while cound < num_moves:
			count += 1
			self.num_sims += 1

			max_potential = self.nodes.keys()[0]
			for node in self.nodes:
				if self.nodes[node].potential > self.nodes[max_potential].potential:
					max_potential = node

			state = self.nodes[max_potential].state
			temp_board = Board(state)
			moves = board.possible_moves()
			for move in moves:
				move_hash = #the hash of the state after the move
				if move_hash in self.nodes:
					moves.pop(move)

			move = random.choice(moves)
			new_state = temp_board.move(move)
			move_hash = self.hash_state(new_state)

			if player1:
				score = simulate(new_state)
			else:
				score = -simulate(new_state)

			parents = self.nodes[max_potential].parents + [max_potential]
			self.nodes[move_hash] = Node(N = 1, Q = score, self.num_moves, new_state, move, move_hash, move, parents = parents )

			for parent in self.nodes[max_potential].parents:
				self.nodes[parent].update(score)

		best_choice = self.nodes.keys()[0]
		for node in self.nodes:
			if self.nodes[node].Ntot > self.nodes[best_choice].Ntot:
				best_choice = node

		return self.nodes[best_choice].move

