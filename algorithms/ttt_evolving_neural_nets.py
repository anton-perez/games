import sys, pickle, copy
import random
import matplotlib.pyplot as plt
sys.path.append('algorithms')
from ttt_neural_net import *
sys.path.append('games')
from tic_tac_toe import *
sys.path.append('players')
from ttt_input_player import *
from ttt_np_player import *
from ttt_nn_player import *

class TTTEvolvingNeuralNets:
  def __init__(self, num_players, num_games=32):
    self.num_players = num_players
    self.num_games = num_games
    self.players = []
    self.gen_num = 0
    self.prev_gen_payoffs = []

  def init_generation(self):
    for i in range(self.num_players):
      net = TTTNeuralNetwork()
      net.initialize()
      self.players.append(NeuralNetPlayer(net))
    self.gen_num += 1

  def first_evaluation(self):
    for player in self.players:
      players = [player, NearPerfectPlayer()]
      for _ in range(self.num_games):
        game = TicTacToe(players)
        game.run_to_completion()
        if game.winner == 1:
          player.payoff_score += 1
        elif game.winner == 2:
          player.payoff_score -= 10

  def second_evaluation(self):
    for i,player in enumerate(self.players):
      other_player_idx = [idx for idx in range(len(self.players)) if idx!=i]
      for _ in range(10):
        rand_idx = random.choice(other_player_idx)
        rand_player = self.players[rand_idx]
        if player.payoff_score > rand_player.payoff_score:
          player.eval_score += 1
        other_player_idx.remove(rand_idx)

  def get_top_players(self):
    self.first_evaluation()
    self.second_evaluation()
    self.players.sort(key=lambda p: p.eval_score, reverse=True)
    self.prev_gen_payoffs = [p.payoff_score for p in self.players]
    return self.players[:int(self.num_players/2)]

  def reset_scores(self, players):
    for player in players:
      player.payoff_score = 0
      player.eval_score = 0
  
  def generate_generation(self):
    top_players = self.get_top_players()
    new_players = []
    for player in top_players:
      new_net = player.neural_net.replicate()
      new_players.append(NeuralNetPlayer(new_net))
    new_generation = top_players + new_players
    self.reset_scores(new_generation)
    self.players = new_generation
    self.gen_num += 1

  def evolve_n_gens(self, n):
    for _ in range(n):
      self.genearate_generation()
    
  def get_net_info(self, player):
    return {'net_obj': player.neural_net, 'net_info':player.neural_net.__dict__}
    
  def gen_copy(self):
    return [copy.deepcopy(player.neural_net) for player in self.players] 


total_gen_num = 100
trials = 20
gens = [i for i in range(total_gen_num)]
max_payoffs = [0 for _ in range(total_gen_num)]


file = open('nn_players.pickle', 'wb')
for i in range(trials): # make 20
  enn = TTTEvolvingNeuralNets(50)
  enn.init_generation()
  print(f'trial {i+1}')
  print('initialized first gen')
  for gen_id in range(total_gen_num): # make 100 or 50
    enn.generate_generation()
    max_payoff = max(enn.prev_gen_payoffs)
    print(f'trial {i+1} gen {enn.gen_num-1} max payoff: {max_payoff}')
    max_payoffs[gen_id] += max_payoff/trials
  enn.get_top_players() # should score newest gen
  pickle.dump(enn.gen_copy(), file)
file.close()
print('finished trials, making plot')

# final gen players stored iteratively, load iteratively
# with open/read, while true, get that gen players, stop if eof error

plt.style.use('bmh')
plt.plot(gens, max_payoffs)
plt.xlabel('Number of Generations')
plt.ylabel('Avg Max Payoff')
plt.savefig('evolving_fogel_nn_players.png')
print('finished plotting')
    

  

  
    
    