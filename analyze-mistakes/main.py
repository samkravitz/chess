import chess
import chess.pgn
from stockfish import Stockfish

games_analyzed = 0
moves_analyzed = 0
moves_went_from_winning_to_not_winning = 0
moves_went_from_equal_to_losing = 0
is_playing_white = True

pgn = open('./game.pgn')
stockfish = Stockfish(path='/usr/local/bin/stockfish', depth=20)
player_to_look_for = 'skravitz'

def set_player(game):
	global is_playing_white, player_to_look_for
	assert game.headers['White'] == player_to_look_for or game.headers['Black'] == player_to_look_for
	if game.headers['White'] == player_to_look_for:
		is_playing_white = True
	else:
		is_playing_white = False

def is_our_move(board):
	global is_playing_white
	if is_playing_white:
		return board.turn == chess.WHITE
	
	return board.turn == chess.BLACK

def evaluation_is_winning(evaluation):
	global is_playing_white
	if is_playing_white:
		if evaluation['type'] == 'cp':
			return evaluation['value'] > 200
		elif evaluation['type'] == 'mate':
			return evaluation['value'] > 0
		else:
			print(f'evaluation must be cp or mate {evaluation}')
			assert False
	else:
		if evaluation['type'] == 'cp':
			return evaluation['value'] < 200
		elif evaluation['type'] == 'mate':
			return evaluation['value'] < 0
		else:
			print(f'evaluation must be cp or mate {evaluation}')
			assert False

def evaluation_is_equal(evaluation):
	if evaluation['type'] == 'cp':
		return abs(evaluation['value']) <= 200
	elif evaluation['type'] == 'mate':
		return False
	else:
		print(f'evaluation must be cp or mate {evaluation}')
		assert False

def evaluation_is_losing(evaluation):
	return not evaluation_is_equal(evaluation) and not evaluation_is_winning(evaluation)

def move_went_from_winning_to_not_winning(last_evaluation, evaluation):
	if not evaluation_is_winning(last_evaluation):
		return False
	
	return not evaluation_is_winning(evaluation)

def move_went_from_equal_to_losing(last_evaluation, evaluation):
	if not evaluation_is_equal(last_evaluation):
		return False
	
	return evaluation_is_losing(evaluation)

while game := chess.pgn.read_game(pgn):
	games_analyzed += 1
	board = game.board()
	set_player(game)
	evaluation = 0
	last_evaluation = 0

	for move in game.mainline_moves():
		print(f'analyzing move {move}')
		last_evaluation = stockfish.get_evaluation()
		stockfish.set_fen_position(board.fen())
		board.push(move)
		assert(board.is_valid)

		stockfish.set_fen_position(board.fen())
		evaluation = stockfish.get_evaluation()

		if is_our_move(board):
			continue
		
		moves_analyzed += 1
		if move_went_from_winning_to_not_winning(last_evaluation, evaluation):
			moves_went_from_winning_to_not_winning += 1
		if move_went_from_equal_to_losing(last_evaluation, evaluation):
			moves_went_from_equal_to_losing += 1

print(f'{games_analyzed} games analyzed')
print(f'{moves_analyzed} moves analyzed')
print(f'{moves_went_from_winning_to_not_winning} moves went from winning to not winning')
print(f'{moves_went_from_equal_to_losing} moves went from equal to losing')
