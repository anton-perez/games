import sys
sys.path.append('games')
from tic_tac_toe import *
sys.path.append('players')
from random_player import *
from ttt_minimax_player import *
from ttt_input_player import *

players = [MinimaxPlayer(), InputPlayer()]
game = TicTacToe(players)
game.run_to_completion()
winner = game.winner