import numpy as np
import pygame as pygame
import sys
import math

ROW_COUNT = 6
COLUMN_COUNT = 7
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

class Move:
	def __init__(self, row, col, piece):
	    self.row = row
	    self.col = col
	    self.piece = piece

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece, move):
	board[row][col] = piece
	update_move(move, row, col, piece)

def check_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	#O(n) solution, check all winning spaces
	#Horizontal locations
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True 

	#Vertical locations
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True 

	#Diagonal-up locations
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True 

	#Diagonal-down locations
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True 

def update_move(move, row, col, piece):
	move.row = row
	move.col = col
	move.piece = piece

def fast_winning_move(board, piece, move):
	#O(1) solution: Only consider most recent move, check if piece is first, second, third, fourth in possible winning combination
	#Horizontal cases:
	for i in range(4):
		if i <= move.col and move.col < COLUMN_COUNT-3+i:
			if board[move.row][move.col-i] == piece and board[move.row][move.col+1-i]  == piece and board[move.row][move.col+2-i]  == piece and board[move.row][move.col+3-i]  == piece:
				return True

	#Vertical cases:
	for i in range(4):
		if i <= move.row and move.row < ROW_COUNT-3+i:
			if board[move.row-i][move.col] == piece and board[move.row+1-i][move.col]  == piece and board[move.row+2-i][move.col]  == piece and board[move.row+3-i][move.col]  == piece:
				return True

	#Diagonal-Up cases:
	for i in range(4):
		if i <= move.col and move.col < COLUMN_COUNT-3+i and i <= move.row and move.row < ROW_COUNT-3+i:
			if board[move.row-i][move.col-i] == piece and board[move.row+1-i][move.col+1-i]  == piece and board[move.row+2-i][move.col+2-i]  == piece and board[move.row+3-i][move.col+3-i]  == piece:
				return True

	#Diagonal-Down cases:
	for i in range(4):
		if i <= move.col and move.col < COLUMN_COUNT-3+i and 3-i <= move.row and move.row < ROW_COUNT-i:
			if board[move.row+i][move.col-i] == piece and board[move.row-1+i][move.col+1-i]  == piece and board[move.row-2+i][move.col+2-i]  == piece and board[move.row-3+i][move.col+3-i]  == piece:
				return True


def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
			
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2:
				pygame.draw.circle(screen, GREEN, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()
	

board = create_board()
print_board(board)
game_over = False
turn = 0

recent_move = Move(0,0,0) #recent move for O(1) win checking

pygame.init() 

SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			else:
				pygame.draw.circle(screen, GREEN, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

			
		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#get player 1 input
			if turn == 0:
				#col = int(input("Player 1 Choose Move (0-6):"))
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if check_valid_location(board, col):
					row = next_open_row(board, col)
					drop_piece(board, row, col, 1, recent_move)
					
					#if winning_move(board, 1): #OLDER VERSION
					if fast_winning_move(board, 1, recent_move):
						print("Player 1 Wins!")
						label = myfont.render("Player 1 Wins!", 1, RED)
						screen.blit(label, (40, 10))
						game_over = True

			#get player 2 input
			else:
				#col = int(input("Player 2 Choose Move (0-6):"))
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if check_valid_location(board, col):
					row = next_open_row(board, col)
					drop_piece(board, row, col, 2, recent_move)

					#if winning_move(board, 2): #OLDER VERSION
					if fast_winning_move(board, 2, recent_move):
						print("Player 2 Wins!")
						label = myfont.render("Player 2 Wins!", 1, GREEN)
						screen.blit(label, (40, 10))
						game_over = True

			print_board(board)
			draw_board(board)
			turn += 1
			turn = turn % 2

			if game_over:
				pygame.time.wait(3000)




