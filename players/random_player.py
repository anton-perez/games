from random import random
import math

class RandomPlayer:
  def __init__(self):
    self.symbol = None
    self.number = None
    self.first = None
  
  def set_player_symbol(self, n):
    self.symbol = n
  
  def set_player_number(self, n):
    self.number = n
  
  def set_first(self, first):
    self.first = first
  
  def choose_move(self, state, choices):
    random_idx = math.floor(len(choices) * random())
    return choices[random_idx]
