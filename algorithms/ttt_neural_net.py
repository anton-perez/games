import math, numpy, copy, random
# import matplotlib.pyplot as plt

class Node:
  def __init__(self, index, activation_function, bias=False):
    self.index = index
    self.prev_layer = [] #from
    self.next_layer = [] #to
    self.act_f = activation_function
    self.input = None
    self.output = None
    self.bias = bias

class TTTNeuralNetwork:
  def __init__(self):
    self.H = random.randint(1,10)
    self.input_layer = []
    self.output_layer = []
    self.hidden_layer = []
    self.weights = {}
    self.nodes = []
    self.counter = 1

  def lin_func(self, x):
    return x
    
  def sig_func(self, x):
    return 1/(1+(math.e)**-x)
  
  def build_layers(self):
    act_f = self.lin_func
    for _ in range(9):
      self.input_layer.append(Node(self.counter, act_f))
      self.counter += 1
    self.input_layer.append(Node(self.counter, act_f, True))
    self.counter += 1

    act_f = self.sig_func
    for _ in range(self.H):
      self.hidden_layer.append(Node(self.counter, act_f))
      self.counter += 1
    self.hidden_layer.append(Node(self.counter, act_f, True))
    self.counter += 1

    for _ in range(9):
      self.output_layer.append(Node(self.counter, act_f))
      self.counter += 1

  def generate_weights(self):
    #(start_index, end_index)
    for input_node in self.input_layer:
      for hidden_node in self.hidden_layer:
        if not hidden_node.bias:
          edge =  (input_node.index, hidden_node.index)
          self.weights[edge] = random.uniform(-5, 5)
    
    for hidden_node in self.hidden_layer:
      for output_node in self.output_layer:
        if not output_node.bias:
          edge = (hidden_node.index, output_node.index)
          self.weights[edge] = random.uniform(-5, 5)
          
  def clear_connections(self):
    for node in self.input_layer + self.hidden_layer + self.output_layer:
      node.prev_layer = []
      node.next_layer = []
    
  def connect_layers(self):
    self.clear_connections()
    for edge in self.weights:
      start_node = self.get_node(edge[0])
      end_node = self.get_node(edge[1])
      if start_node.bias:
        start_node.output = 1
      if end_node not in start_node.next_layer:
        start_node.next_layer.append(end_node)
      if start_node not in end_node.prev_layer:
        end_node.prev_layer.append(start_node)
      

  def get_node(self, node_index):
    for node in self.input_layer + self.hidden_layer + self.output_layer:
      if node.index == node_index:
        return node
  
  def initialize(self):
    self.build_layers()
    self.generate_weights()
    self.connect_layers()

  def clear_network(self):
    all_nodes = self.input_layer + self.hidden_layer + self.output_layer
    for node in all_nodes:
      if not node.bias:
        node.input = None
        node.output = None
      
  def forward_propagate(self, input_vals):
    self.clear_network()
    for i, input_val in enumerate(input_vals):
      self.input_layer[i].input = input_val
      self.input_layer[i].output = self.input_layer[i].act_f(input_val)

    for hidden_node in self.hidden_layer:
      if not hidden_node.bias:
        if hidden_node.input == None:
          hidden_node.input = 0
          end_index = hidden_node.index
          for prev_node in self.input_layer:
            start_index = prev_node.index
            hidden_node.input += self.weights[(start_index, end_index)]*prev_node.output
        hidden_node.output = hidden_node.act_f(hidden_node.input)
        # if hidden_node.output == None:
        #   print(hidden_node.index)

    for output_node in self.output_layer:
      if not output_node.bias:
        if output_node.input == None:
          output_node.input = 0
          end_index = output_node.index
          for prev_node in self.hidden_layer:
            start_index = prev_node.index
            output_node.input += self.weights[(start_index, end_index)]*prev_node.output
        output_node.output = output_node.act_f(output_node.input)  
        
    return [node.output for node in self.output_layer]
  
  def add_node(self):
    self.H += 1
    act_f = self.sig_func
    new_node = Node(self.counter, act_f)
    self.counter += 1
    for input_node in self.input_layer:
      input_node.next_layer.append(new_node)
      new_node.prev_layer.append(input_node)
      edge = (input_node.index, new_node.index)
      self.weights[edge] = 0

    for output_node in self.output_layer:
      output_node.prev_layer.append(new_node)
      new_node.next_layer.append(output_node)
      edge = (new_node.index, output_node.index)
      self.weights[edge] = 0
    
    self.hidden_layer.append(new_node)
    
  def delete_node(self):
    self.H -= 1
    removed_node = random.choice([node for node in self.hidden_layer if not node.bias])
    for input_node in self.input_layer:
      if removed_node in input_node.next_layer:
        input_node.next_layer.remove(removed_node)
      edge = (input_node.index, removed_node.index)
      if edge in self.weights.keys():
        del self.weights[edge]

    for output_node in self.output_layer:
      if removed_node in output_node.prev_layer:
        output_node.prev_layer.remove(removed_node)
      edge = (removed_node.index, output_node.index)
      if edge in self.weights.keys():
        del self.weights[edge]

    self.hidden_layer.remove(removed_node)

  def copy(self):
    copied_net = TTTNeuralNetwork()
    copied_net.H = self.H
    copied_net.input_layer = copy.deepcopy(self.input_layer)
    copied_net.hidden_layer = copy.deepcopy(self.hidden_layer)
    copied_net.output_layer = copy.deepcopy(self.output_layer)
    copied_net.weights = {edge:self.weights[edge] for edge in self.weights}
    copied_net.connect_layers()
    copied_net.counter = int(self.counter)
    return copied_net
    
  
  def replicate(self):
    new_net = self.copy()
    for key in new_net.weights:
      new_net.weights[key] += numpy.random.normal(0,0.05)
  
    mod_bool = random.choice([True, False])
    if mod_bool:
      add_bool = random.choice([True, False])
      if add_bool:
        if self.H < 10:
          new_net.add_node()
      else: 
        if self.H > 1:
          new_net.delete_node()

    return new_net

# net = TTTNeuralNetwork()
# net.initialize()
# print([n.index for n in net.output_layer])
# print([n.index for n in net.hidden_layer])
# print([n.index for n in net.input_layer])
# print(net.forward_propagate([0,0,0,0,0,0,0,0,0]))
# print(len(net.weights))
# new_net = net.replicate()
# print([n.index for n in new_net.output_layer])
# print([n.index for n in new_net.hidden_layer])
# print([n.index for n in new_net.input_layer])
# print(new_net.forward_propagate([0,0,0,0,0,0,0,0,0]))
# # print(len(new_net.weights))
# print(net.weights)
    
    
    
    

  