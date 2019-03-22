import pygame
import sys
from numpy import *
from Hive_funcs import *

win_size = (1080,720)

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode(win_size)
	board = Board()
	gui = Gui(screen)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			is_won, loser = board.is_game_over()
			if is_won:
				continue

			if event.type == pygame.KEYDOWN:
				if pygame.key.get_pressed()[pygame.K_m]:
					if (gui.mode == None) and (board.remaining_pieces[board.player]['queen'] == 0):
							gui.mode = 'sel'
				if pygame.key.get_pressed()[pygame.K_q]:
					if (gui.mode == None) and (board.remaining_pieces[board.player]['queen'] != 0):
						gui.mode = 'add'
						gui.adding_type = 'queen'

				if ((board.turn == 7) or (board.turn == 8)) and (board.remaining_pieces[board.player]['queen'] != 0):
					#if its your fourth move and you havent placed your queen, you have to place your queen
					continue

				if pygame.key.get_pressed()[pygame.K_a]:
					if (gui.mode == None) and (board.remaining_pieces[board.player]['ant'] != 0):
						gui.mode = 'add'
						gui.adding_type = 'ant'
				if pygame.key.get_pressed()[pygame.K_s]:
					if (gui.mode == None) and (board.remaining_pieces[board.player]['spider'] != 0):
						gui.mode = 'add'
						gui.adding_type = 'spider'
				if pygame.key.get_pressed()[pygame.K_b]:
					if (gui.mode == None) and (board.remaining_pieces[board.player]['beetle'] != 0):
						gui.mode = 'add'
						gui.adding_type = 'beetle'
				if pygame.key.get_pressed()[pygame.K_g]:
					if (gui.mode == None) and (board.remaining_pieces[board.player]['grasshopper'] != 0):
						gui.mode = 'add'
						gui.adding_type = 'grasshopper'
				if pygame.key.get_pressed()[pygame.K_ESCAPE]:
					gui.mode = None
					gui.adding_type = None
					gui.selected_piece = None

			if pygame.mouse.get_pressed()[0]:
				pos = gui.cart_to_hex(pygame.mouse.get_pos())
				if gui.mode == 'sel':
					if (pos in board.state):
						if (pos == top_tile(pos, board.state)):
							if (board.state[pos].player == board.player):
								gui.selected_piece = board.state[pos]
								gui.mode = 'mov'
						else:
							pos = top_tile(pos, board.state)
							if (board.state[pos].player == board.player):
								gui.selected_piece = board.state[pos]
								gui.mode = 'mov'

				elif gui.mode == 'mov':
					if (gui.selected_piece.bug == 'beetle') and (pos in board.state):
						top = top_tile(pos, board.state)
						pos = (top[0], top[1], top[2]+1)
					if pos in gui.selected_piece.valid_moves(board.state):
						board.move(gui.selected_piece.pos, pos)
						gui.mode = None
						gui.selected_piece = None

				elif gui.mode == 'add':
					if pos in board.valid_placements():
						board.add(gui.adding_type,pos)
						gui.mode = None
						gui.adding_type = None
				else:
					pass



		screen.fill((150,150,150))
		gui.draw_board(board, pygame.mouse.get_pos())
		pygame.display.flip()
