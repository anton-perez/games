import random
import math
import sys
sys.path.append('games')
from c4_heuristic_game_tree import *

class HeuristicPlayer:
  def __init__(self, search_depth = 4):
    self.symbol = None
    self.number = None
    self.first = None
    self.search_depth = search_depth
    self.game_tree = None
  
  def set_player_symbol(self, n):
    self.symbol = n
  
  def set_player_number(self, n):
    self.number = n
  # def set_first(self, first):
    self.first = '1'
    self.game_tree = HeuristicGameTree(self.number, self.first, self.search_depth)
    self.game_tree.set_scores(self.game_tree.root, self.symbol)

  def transpose(self, state):
    return [[state[i][j] for i in range(len(state))] for j in range(len(state[0]))]
  
  def choose_move(self, state, choices):
    state_string = self.game_tree.state_to_string(state)
    if state_string not in self.game_tree.state_dict.keys():
      self.game_tree.state_dict[state_string] = Node(state, self.symbol)
    state_node = self.game_tree.state_dict[state_string]
    if state_node.children == []:
      self.game_tree.build_part_of_tree(state_node)
      self.game_tree.set_scores(state_node, self.symbol)
    scores = [child.score for child in state_node.children]
    max_score = max(scores)
    max_indices = [i for i, x in enumerate(scores) if x == max_score]
    #random_index = random.choice(max_indices)
    chosen_state = state_node.children[max_indices[0]].state
    for choice in choices:
      choice_state = [[state[i][j] for j in range(6)] for i in range(7)]
      i = 0
      while i+1 < 6 and choice_state[choice][i+1]==None:
        i+=1
      choice_state[choice][i] = self.symbol
      if choice_state == chosen_state:
        return choice