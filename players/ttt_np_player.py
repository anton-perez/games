import math, random

class NearPerfectPlayer():
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

  def opposite_symbol(self):
    if self.symbol == '1':
      return '2'
    if self.symbol == '2':
      return '1'
    
  def get_lines_with_coords(self, state):
    rows = [[(state[i][j], (i,j)) for j in range(3)] for i in range(3)]
    cols = [[(state[j][i], (j,i)) for j in range(3)] for i in range(3)]
    diags = [[(state[i][i], (i,i)) for i in range(3)],
            [(state[i][2-i], (i,2-i)) for i in range(3)]]

    return rows + cols + diags
  # def is_move_valid(self, move, choices):
  #   if move == 'before input' or move not in [i for i in range(9)]:
  #     return False
  #   return self.index_to_coords(move) in choices

  def choose_move(self, state, choices):  
    random_int = random.randint(1,10)
    if random_int == 1:
      return random.choice(choices)
    else:
      lines = self.get_lines_with_coords(state)
      for line_coords in lines:
        line = [l[0] for l in line_coords]
        coords = [l[1] for l in line_coords]
        if line.count(self.symbol) == 2 and None in line:
          idx = line.index(None)
          return coords[idx]
      for line_coords in lines:
        line = [l[0] for l in line_coords]
        coords = [l[1] for l in line_coords]
        if line.count(self.opposite_symbol()) == 2 and None in line:
          idx = line.index(None)
          return coords[idx]
      for line_coords in lines:
        line = [l[0] for l in line_coords]
        coords = [l[1] for l in line_coords]
        if line.count(None) == 2 and self.opposite_symbol() in line:
          idx = line.index(self.opposite_symbol())
          none_idxs = [i for i in range(3) if i != idx]
          return coords[random.choice(none_idxs)]
      return random.choice(choices)
      
        
  