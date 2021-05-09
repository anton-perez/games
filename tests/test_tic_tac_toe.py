import sys
sys.path.append('games')
from tic_tac_toe import *
sys.path.append('players')
from random_player import *

players = [RandomPlayer(), RandomPlayer()]
game = TicTacToe(players)

game.print_board()

game.complete_round()
game.print_board()

game.run_to_completion()
game.print_board()
print(game.round)
print(game.winner)

num_wins = {1: 0, 2: 0, 'Tie':0}

for _ in range(1000):
  players = [RandomPlayer(), RandomPlayer()]
  game = TicTacToe(players)
  game.run_to_completion()
  winner = game.winner

  num_wins[winner] += 1
print(num_wins)