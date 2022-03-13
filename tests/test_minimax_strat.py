import sys
sys.path.append('games')
from tic_tac_toe import *
sys.path.append('players')
from random_player import *
from minimax_player import *


num_wins = {1: 0, 2: 0, 'Tie':0}

for _ in range(3):
  players = [RandomPlayer(), MinimaxPlayer()]
  game = TicTacToe(players)
  game.run_to_completion()
  winner = game.winner
  print(winner)

  num_wins[winner] += 1
print(num_wins)