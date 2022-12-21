class NeuralNetPlayer():
  def __init__(self, neural_net):
    self.symbol = None
    self.number = None
    self.first = None
    self.payoff_score = 0
    self.eval_score = 0
    self.neural_net = neural_net

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

  def index_to_coords(self, index):
    return (int((index-index%3)/3), int(index%3))

  def coords_to_index(self, coords):
    return 3*coords[0]+coords[1]

  def state_to_input(self, state):
    state_list = state[0]+state[1]+state[2]
    input_list = [1 if i == self.symbol else -1 if i == self.opposite_symbol() else 0 for i in state_list]
    return input_list
  
  def choose_move(self, state, choices):  
    input = self.state_to_input(state)
    output = self.neural_net.forward_propagate(input)
    if None in output or output == []:
      print(input)
      print(output)
    valid_idxs = [self.coords_to_index(choice) for choice in choices] 
    # if None in valid_idxs or valid_idxs == []:
    #   print(valid_idxs)   
    max_output = max([output[i] for i in valid_idxs])
    max_idx = output.index(max_output)
    return self.index_to_coords(max_idx)
    
  