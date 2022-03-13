import math, random
import sys
sys.path.append('games')
from tic_tac_toe import *
sys.path.append('players')
from strat_player import *

strat1 = generate_random_strat()
strat2 = generate_random_strat()

# for i, (j,k) in enumerate(strat1.items()):
#   if i < 200 and i > 100:
#     print(i,j,k)

players = [StratPlayer(strat1), StratPlayer(strat2)]
game = TicTacToe(players)

game.print_board()

game.complete_round()
game.print_board()

game.run_to_completion()
game.print_board()
print(game.round)
print(game.winner)


