import math, random
import sys
sys.path.append('games')
from tic_tac_toe import *
sys.path.append('players')
from strat_player import *

class GeneticAlgorithm():
  def __init__(self, initial_strats):
    self.strats = initial_strats.copy()
    self.players = [StratPlayer(strat) for strat in initial_strats]
    self.scores = [0 for _ in range(len(initial_strats))]

  def run_games(self):
    for i in range(len(self.strats)):
      for j in range(len(self.strats)):
        if i != j:
          players = [self.players[i], self.players[j]]
          game =  TicTacToe(players)
          game.run_to_completion()
          if game.winner == 1:
            self.scores[i] += 1
            self.scores[j] -= 1
          elif game.winner == 2:
            self.scores[i] -= 1
            self.scores[j] += 1


  def breed_strats(self, parent_strats):
    child_strat = {}
    for state in parent_strats[0]:
      child_strat[state] = parent_strats[round(random())][state]
    return child_strat
      
  def generate_new_generation(self):
    self.run_games()
    top_idxs = sorted(zip(self.scores, [i for i in range(len(self.scores))]), reverse=True)[:5]
    top_strats = [self.strats[i] for s,i in top_idxs]
    new_strats = top_strats.copy()
    for i in range(len(top_strats)):
      for j in range(len(top_strats)):
        if i!=j:
          child_strat = self.breed_strats([top_strats[i],top_strats[j]])
          new_strats.append(child_strat)

    self.strats = new_strats
    self.players = [StratPlayer(strat) for strat in new_strats]
    self.scores = [0 for _ in range(len(new_strats))]

  def run_generations(self, num_generations):
    for i in range(num_generations):
      self.generate_new_generation()
      print('generated generation:',i)

  
    
    
    
    
          