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
  
  def print_board(self, state):
    transpose_state = [[state[i][j] for i in range(7)] for j in range(6)]
    for i in range(len(transpose_state)):
      row = transpose_state[i]
      row_string = ''
      for space in row:
        if space == None:
          row_string += '_|'
        else:
          row_string += space + '|'
      print(row_string[:-1])
    print('\n')

  def is_move_valid(self, move, choices):
    if move == 'before input' or move not in [i for i in range(7)]:
      return False
    return move in choices

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
    return move

  
