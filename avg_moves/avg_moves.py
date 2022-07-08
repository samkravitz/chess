#! /usr/bin/python3

# this program counts the average number of moves per game given a pgn file

import sys
import chess.pgn

pgn_filename = sys.argv[1] if len(sys.argv) > 1 else 'skravitz-rapid.pgn'

pgn = open(pgn_filename)

num_games_won = 0
num_games_lost = 0
num_games_drawn = 0

total_won_moves = 0
total_lost_moves = 0
total_drawn_moves = 0

while game := chess.pgn.read_game(pgn):
	is_white = game.headers['White'] == 'skravitz'

	nmoves = 0
	for move in game.mainline_moves():
		nmoves += 1
	# divide by 2 because a move ie '1.e4 e5' is interpreted as 2 moves
	nmoves /= 2

	# game drawn
	if game.headers['Result'] == '1/2-1/2':
		num_games_drawn += 1
		total_drawn_moves += nmoves
	
	# won game as white
	elif is_white and game.headers['Result'] == '1-0':
		num_games_won += 1
		total_won_moves += nmoves
	
	# lost game as white
	elif is_white and game.headers['Result'] == '0-1':
		num_games_lost += 1
		total_lost_moves += nmoves
	
	# lost game as black
	elif not is_white and game.headers['Result'] == '1-0':
		num_games_lost += 1
		total_lost_moves += nmoves
	
	# won game as black
	elif not is_white and game.headers['Result'] == '0-1':
		num_games_won += 1
		total_won_moves += nmoves
	else:
		print('should never get here')
	

print(f'sample size: {num_games_won + num_games_drawn + num_games_lost} games')

print(f'{num_games_won} games won')
print(f'{num_games_drawn} games lost')
print(f'{num_games_lost} games drawn')

print(f'avg moves in won games: {total_won_moves / num_games_won:.1f}')
print(f'avg moves in drawn games: {total_drawn_moves / num_games_drawn:.1f}')
print(f'avg moves in lost games: {total_lost_moves / num_games_lost:.1f}')
