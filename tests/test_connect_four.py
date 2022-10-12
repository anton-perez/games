import sys
sys.path.append('games')
from connect_four import *
sys.path.append('players')
from random_player import *
from c4_input_player import *

players = [InputPlayer(), RandomPlayer()]
game = ConnectFour(players)
game.run_to_completion()
winner = game.winner