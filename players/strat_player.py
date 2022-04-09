from random import random
import math

def decimal_to_terniary(n):
  if n == 0:
    return '0'
  trit_str = ''
  num_of_trits = math.floor(math.log(n,3)) + 1
  remaining = n
  for place in range(num_of_trits, 0, -1):    
    if remaining >= 3**(place-1):
      trit = 0
      while remaining > 3**(place-1):
        remaining -= 3**(place-1)
        trit += 1
      trit_str += str(trit)
    else:
      trit_str += '0'

  return trit_str

def possible_state(state_str):
  num_ones = len([i for i in range(9) if state_str[i] == '1'])
  num_twos = len([i for i in range(9) if state_str[i] == '2'])
  return True if abs(num_ones - num_twos) < 2 and num_ones + num_twos != 9 else False

def generate_random_strat():
  strat = {}
  for i in range(3**9):
    trit_str = decimal_to_terniary(i)
    state_str = ''.join(['0' for _ in range(9-len(trit_str))]) + trit_str
    if possible_state(state_str):
      possible_moves = [i for i in range(9) if state_str[i] == '0']
      random_idx = math.floor(len(possible_moves) * random())
      strat[state_str] = possible_moves[random_idx]
  return strat


class StratPlayer:
  def __init__(self, strat):
    self.symbol = None
    self.number = None
    self.first = None
    self.strat = strat
  
  def set_player_symbol(self, n):
    self.symbol = n
  
  def set_player_number(self, n):
    self.number = n
  
  def set_first(self, first):
    self.first = first

  def state_to_string(self, state):
    #make so strat always plays as 1
    #1 is player, 2 is opponent
    state_list = state[0]+state[1]+state[2]
    if self.number == 1:
      str_list = ['0' if i == None else i for i in state_list]
    elif self.number == 2:
      #changes 1s to 2s and 2s to 1s
      str_list = ['0' if i == None else str(3-int(i)) for i in state_list]
    return ''.join(str_list)

  def string_to_state(self, string):
    return [list(string[i:i+3]) for i in range(0, 9, 3)]

  def index_to_coords(self, index):
    return (int((index-index%3)/3), int(index%3))

  def coords_to_index(self, coords):
    return 3*coords[0]+coords[1]
    
  def choose_move(self, state, choices):
    state_string = self.state_to_string(state)
    strat_idx = self.strat[state_string]
    return self.index_to_coords(strat_idx)