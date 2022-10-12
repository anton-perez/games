class InputPlayer():
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

  def index_to_coords(self, index):
    return (int((index-index%3)/3), int(index%3))
  
  def print_board(self, state):
    for i in range(len(state)):
      row = state[i]
      row_string = ''
      for space in row:
        if space == None:
          row_string += '_|'
        else:
          row_string += space + '|'
      print(row_string[:-1])
    print('\n')

  def is_move_valid(self, move, choices):
    if move == 'before input' or move not in [i for i in range(9)]:
      return False
    return self.index_to_coords(move) in choices

  def choose_move(self, state, choices):  
    self.print_board(state)
    move = 'before input'
    while not self.is_move_valid(move, choices):
      if move == 'before input':
        move = input("\nYour move: ")
      else:
        print("that move is not valid")
        move = input("Your move: ")
  
      move = int(move)
    return self.index_to_coords(move)

  
