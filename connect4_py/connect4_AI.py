import numpy as np
import random
import pygame
import sys
import math

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

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

def evaluate_window(window, piece):
	score = 0

	#get opponet's piece (1->2, 2->1)
	opp_piece = piece % 2
	opp_piece += 1

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2
	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score


def score_position(board, piece):
	score = 0

	#Score Center Column:
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	##Score Horizontal:
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range (COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	##Score Vertical:
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	##Score Diagonal-Up:
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	##Score Diagonal-Down:
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):

	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)

	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 10000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000)
			else: #game is over, no more moves
				return (None, 0)
		else: #depth is 0
			return (None, score_position(board, AI_PIECE))

	if maximizingPlayer:
		value = -math.inf
		best_column = random.choice(valid_locations)
		for col in valid_locations:
			row = next_open_row(board, col)
			board_copy = board.copy()
			drop_piece(board_copy, row, col, AI_PIECE)
			new_score = minimax(board_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				best_column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return best_column, value

	else: #minimizingPlayer
		value = math.inf
		best_column = random.choice(valid_locations)
		for col in valid_locations:
			row = next_open_row(board, col)
			board_copy = board.copy()
			drop_piece(board_copy, row, col, PLAYER_PIECE)
			new_score = minimax(board_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				best_column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return best_column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if check_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(baord, piece):
	
	valid_locations = get_valid_locations(board)
	best_score = 0
	best_col = random.choice(valid_locations)

	for col in valid_locations:
		row = next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col


def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
			
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE:
				pygame.draw.circle(screen, GREEN, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()
	

board = create_board()
print_board(board)
game_over = False
turn = 0
#turn = random.randint(PLAYER, AI)

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
			if turn == PLAYER:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#get player 1 input
			if turn == PLAYER:
				#col = int(input("Player 1 Choose Move (0-6):"))
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if check_valid_location(board, col):
					row = next_open_row(board, col)
					drop_piece(board, row, col, PLAYER_PIECE)
					
					if winning_move(board, PLAYER_PIECE): 
						print("Player 1 Wins!")
						label = myfont.render("Player 1 Wins!", PLAYER_PIECE, RED)
						screen.blit(label, (40, 10))
						game_over = True

					turn += 1
					turn = turn % 2

					print_board(board)
					draw_board(board)

	#get player 2 input
	if turn == AI and not game_over:

		#col = pick_best_move(board, AI_PIECE)
		col, minimax_score = minimax(board, 4, -math.inf, math.inf, True) #DEPTH = 4, CAN INCREASE FOR DIFFICULTY!

		if check_valid_location(board, col):
			pygame.time.wait(500)
			row = next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)

			if winning_move(board, AI_PIECE): 
				print("Player 2 Wins!")
				label = myfont.render("Player 2 Wins!", PLAYER_PIECE, GREEN)
				screen.blit(label, (40, 10))
				game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)




