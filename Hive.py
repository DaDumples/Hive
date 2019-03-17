import pygame
import sys
from numpy import *

win_size = (1080,720)

class Hex():

	def __init__(self, x, y, screen, im_file = None, color = (180,180,180), linewidth = 0):
		self.x = x
		self.y = y
		self.z = -(x+y) #for whenever you want to use a three axis coordinate system
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

	def __init__(self, player, x, y, screen):
		if player == 1:
			color = (210,180,140)
			linewidth = 0
		elif player == -1:
			color = (25,25,25)
			linewidth = 0
		self.player = player
		Hex.__init__(self, x, y, screen, 'bee.png',color, linewidth)

	def can_move(self, pieces):
		pass

	def valid_moves(self, pieces):
		pass




# class Board():

# 	def __init__(self, screen):
# 		self.screen = screen
# 		self.player = 1
# 		self.turn = 1
# 		self.pieces = {}
# 		self.piece_selected = None
# 		self.mode = 'add'

# 	def draw(self,mousepos):
# 		if turn == 1:
# 			Empty_hex(0, 0, mousepos, screen).draw()
# 		else:
# 			for piece in self.pieces:
# 				piece.draw()

# 	def add(self, player, piece_type, xpos, ypos):






pygame.init()
screen = pygame.display.set_mode(win_size)

test = Queen(1,0,0,screen)
test2 = Hex(1,0,screen)
test3 = Queen(-1,1,1,screen)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()


	screen.fill((250,250,250))
	test.draw()
	test2.draw()
	test3.draw()
	pygame.display.flip()