import sys
sys.path.append('games')
from connect_four import *
sys.path.append('players')
from random_player import *
from c4_input_player import *
from c4_heuristic_player import *
from c4_lastminute_player import *

players = [HeuristicPlayer(), InputPlayer()]
game = ConnectFour(players)
game.run_to_completion()
winner = game.winner

num_wins = {1: 0, 2: 0, 'Tie':0}

print('First 50')
for _ in range(50):
  players = [HeuristicPlayer(), LastMinutePlayer()]
  game = ConnectFour(players)
  game.run_to_completion()
  winner = game.winner
  print(winner)
  num_wins[winner] += 1

print(num_wins)

num_wins = {1: 0, 2: 0, 'Tie':0}

print('Next 50')
for _ in range(50):
  players = [LastMinutePlayer(), HeuristicPlayer()]
  game = ConnectFour(players)
  game.run_to_completion()
  winner = game.winner
  print(winner)
  num_wins[winner] += 1
  
print(num_wins)


players = [HeuristicPlayer(), RandomPlayer()]
game = ConnectFour(players)
game.run_to_completion()
winner = game.winner