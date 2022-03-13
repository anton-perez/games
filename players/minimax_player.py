import random
import math
import sys
sys.path.append('games')
from game_tree import *

class MinimaxPlayer:
  def __init__(self):
    self.symbol = None
    self.number = None
    self.first = None
    self.game_tree = None
  
  def set_player_symbol(self, n):
    self.symbol = n
  
  def set_player_number(self, n):
    self.number = n

  def set_first(self, first):
    self.first = first
    self.game_tree = GameTree(self.first)
    self.game_tree.set_scores(self.game_tree.root, self.symbol)

  def choose_move(self, state, choices):
    state_node = self.game_tree.get_node(state)
    scores = [child.score for child in state_node.children]
    max_score = max(scores)
    max_indices = [i for i, x in enumerate(scores) if x == max_score]
    random_index = random.choice(max_indices)
    chosen_state = state_node.children[random_index].state
    for choice in choices:
      choice_state = [[state[i][j] for j in range(3)] for i in range(3)]
      choice_state[choice[0]][choice[1]] = self.symbol
      if choice_state == chosen_state:
        return choice
  