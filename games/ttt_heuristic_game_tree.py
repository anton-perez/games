class Node:
  def __init__(self, state, player):
    self.state = state
    self.player = player
    self.winner = None
    self.children = []
    self.score = None
  
  def print_state(self):
    for i in range(len(self.state)):
      row = self.state[i]
      row_string = ''
      for space in row:
        if space == None:
          row_string += '_|'
        else:
          row_string += space + '|'
      print(row_string[:-1])
    print('\n')


class HeuristicGameTree:
  def __init__(self, player, first, search_depth):
    self.root = Node([[None for _ in range(3)] for _ in range(3)], first)
    self.player = player
    self.first = first
    self.search_depth = search_depth
    self.node_num = 1
    self.leaf_node_num = 0
    self.state_dict = {'000000000':self.root}
    self.build_part_of_tree(self.root)

  def get_open_spaces(self, state):
    open_spaces = [(i,j) for i in range(3) for j in range(3) if state[i][j] == None]
    return open_spaces

  def get_opposite_symbol(self, symbol):
    if symbol == '1':
      return '2'
    elif symbol == '2':
      return '1'

  def state_to_string(self, state):
    state_list = state[0]+state[1]+state[2]
    str_list = ['0' if i == None else i for i in state_list]
    return ''.join(str_list)
  
  def check_for_winner(self, state):
    rows = state.copy()
    cols = [[state[i][j] for i in range(3)] for j in range(3)]
    diags = [[state[i][i] for i in range(3)],
             [state[i][2-i] for i in range(3)]]

    board_full = True
    for line in (rows + cols + diags):
      if None in line:
        board_full = False

      for symbol in ['1','2']:
        if line == [symbol for _ in range(3)]:
          return symbol
    
    if board_full:
      return 'Tie'
    return None
  
  def get_node(self, state):
    current_nodes = [self.root]
    while True:
      for node in current_nodes:
        if node.state == state:
          return node
        else:
          current_nodes += node.children
          current_nodes.remove(node)

  def build_part_of_tree(self, start_node):
    current_layer = [start_node]
    for i in range(self.search_depth):
      next_layer = []
      for node in current_layer:
        if node.winner == None:
          for space in self.get_open_spaces(node.state):
            new_state = [[node.state[i][j] for j in range(3)] for i in range(3)]
            new_state[space[0]][space[1]] = node.player
            new_string = self.state_to_string(new_state)
            if new_string in self.state_dict.keys():
              existing_node = self.state_dict[new_string]
              node.children.append(existing_node)
            else:
              new_node = Node(new_state, self.get_opposite_symbol(node.player))
              new_node.winner = self.check_for_winner(new_state)
              node.children.append(new_node)
              next_layer.append(new_node)

              self.state_dict[new_string] = new_node
              self.node_num += 1
              if new_node.winner != None:
                self.leaf_node_num += 1
                break

      current_layer = next_layer

      

  def heuristic_function(self, state, player):
    rows = state.copy()
    cols = [[state[i][j] for i in range(3)] for j in range(3)]
    diags = [[state[i][i] for i in range(3)],
             [state[i][2-i] for i in range(3)]]
    
    score = 0
    opponent = self.get_opposite_symbol(player)
    for line in (rows + cols + diags):
      if None in line:
        if line.count(player) == 2:
          score += 1
        elif line.count(opponent) == 2:
          score -= 1

    return score/8
    

  def set_scores(self, node, player):
    if node.children != []:
      for child in node.children:
        self.set_scores(child, player)

      scores = [child.score for child in node.children]
      if node.player == str(self.player):
        node.score = max(scores)
      else:
        node.score = min(scores)
    else: 
      if node.winner == None:
        node.score = self.heuristic_function(node.state, player)
      elif node.winner == player:
        node.score = 1
      elif node.winner == 'Tie':
        node.score = 0
      else:
        node.score = -1
