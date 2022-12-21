import math
import random
from random import shuffle, sample
import matplotlib.pyplot as plt
import sys
sys.path.append('games')
from tic_tac_toe import *
sys.path.append('players')
from strat_player import *


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

def get_lines(state):
    board = [list(state[i:i+3]) for i in range(0, 9, 3)]
    rows = [[board[i][j] for j in range(3)] for i in range(3)]
    cols = [[rows[i][j] for i in range(3)] for j in range(3)]
    diags = [[rows[i][i] for i in range(3)],
             [rows[i][2-i] for i in range(3)]]

    return rows + cols + diags



def possible_state(state_str):
  num_ones = len([i for i in range(9) if state_str[i] == '1'])
  num_twos = len([i for i in range(9) if state_str[i] == '2'])
  lines = get_lines(state_str)
  if (['1','1','1'] in lines) or (['2','2','2'] in lines):
    return False
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



class GeneticAlgorithm():
  def __init__(self, population_size, mutation_rate):
    self.strats = [generate_random_strat() for _ in range(population_size)]
    self.population = population_size
    self.mutation_rate = mutation_rate
    # self.players = [StratPlayer(strat) for strat in initial_strats]
    # self.top_strats = []
    # self.scores = [0 for _ in range(len(initial_strats))]
    # self.generations = [initial_strats.copy()]

  def run_games(self, strats):
    scores = [0 for _ in range(len(strats))]
    players = [StratPlayer(strat) for strat in strats]
    for i in range(len(strats)):
      for j in range(len(strats)):
        if i != j:
          game_players = [players[i], players[j]]
          game =  TicTacToe(game_players)
          game.run_to_completion()
          if game.winner == 1:
            scores[i] += 1
            scores[j] -= 1
          elif game.winner == 2:
            scores[i] -= 1
            scores[j] += 1

    return scores

  def run_brackets(self, strats):
    num_rounds = int(math.log(len(strats), 2))
    ranks = [num_rounds for _ in range(len(strats))]
    current_players = [(StratPlayer(strat), i) for i, strat in enumerate(strats)]
    for round in range(num_rounds):
      shuffle(current_players)
      brackets = [current_players[i:i+2] for i in range(0,len(current_players),2)]
      winning_players = []
      for bracket in brackets:
        bracket_players, idxs = list(zip(*bracket))
        game =  TicTacToe(bracket_players)
        game.run_to_completion()
        if game.winner == 1:
          ranks[idxs[0]] -= 1
          winning_players.append((bracket_players[0], idxs[0]))
        elif game.winner == 2:
          ranks[idxs[1]] -= 1
          winning_players.append((bracket_players[1], idxs[1]))
        elif game.winner == 'Tie':
          rand_idx = math.floor(2 * random())
          ranks[idxs[rand_idx]] -= 1
          winning_players.append((bracket_players[rand_idx], idxs[rand_idx]))
          
      current_players = winning_players
    
    return ranks
    

  def breed_strats(self, parent_strats):
    child_strat = {}
    for state in parent_strats[0]:
      r = random()
      if r < (1+self.mutation_rate)/2 and r > (1-self.mutation_rate)/2:
        possible_moves = [i for i in range(9) if state[i] == '0']
        random_idx = math.floor(len(possible_moves) * random())
        child_strat[state] = possible_moves[random_idx]
      else:
        child_strat[state] = parent_strats[round(r)][state]
    return child_strat
  
  def generate_new_generation(self, init_strats, fitness_score = 'Round Robin',selection_method = 'Hard Cut Off'):
    if fitness_score == 'Round Robin':
      if selection_method == 'Hard Cut Off':
        scores = self.run_games(init_strats)
        top_idxs = sorted(zip(scores, [i for i in range(len(scores))]), reverse=True)[:math.floor(self.population/4)]
        

      elif selection_method == 'Stochastic':
        scores = self.run_games(init_strats)
        scored_idxs = list(zip(scores, [i for i in range(len(scores))]))
        top_idxs = []
        for _ in range(math.floor(self.population/4)):
          shuffle(scored_idxs)
          top_idx = max(scored_idxs[:math.floor(self.population/8)],key=lambda item:item[0])
          top_idxs.append(top_idx)
          scored_idxs.remove(top_idx)
          
        # subsets = [scored_idxs[i:i+math.floor(self.population/8)] for i in range(0, len(scored_idxs), math.floor(self.population/8))]
        # top_idxs = [max(subset,key=lambda item:item[0]) for subset in subsets[:math.floor(self.population/4)]]

      elif selection_method == 'Tournament':
        idxed_strats = list(zip(init_strats, [i for i in range(len(init_strats))]))
        top_idxs = []
        for _ in range(math.floor(self.population/4)):
          shuffle(idxed_strats)
          subset_idxed_strats = idxed_strats[:math.floor(self.population/8)]
          subset_strats, subset_idxs = tuple(zip(*subset_idxed_strats))
          scores = self.run_games(subset_strats)
          scored_idxs = list(zip(scores, subset_idxs))
          top_idx = max(scored_idxs[:math.floor(self.population/8)],key=lambda item:item[0])
          top_idxs.append(top_idx)
          idxed_strats.remove((init_strats[top_idx[1]], top_idx[1]))


    elif fitness_score == 'Bracket':
      if selection_method == 'Hard Cut Off':
        ranks = self.run_brackets(init_strats)
        top_idxs = sorted(zip(ranks, [i for i in range(len(ranks))]), reverse=False)[:math.floor(self.population/4)]
        
      elif selection_method == 'Stochastic':
        ranks = self.run_brackets(init_strats)
        ranked_idxs = list(zip(ranks, [i for i in range(len(ranks))]))
        top_idxs = []
        for _ in range(math.floor(self.population/4)):
          shuffle(ranked_idxs)
          top_idx = min(ranked_idxs[:math.floor(self.population/8)],key=lambda item:item[0])
          top_idxs.append(top_idx)
          ranked_idxs.remove(top_idx)

      elif selection_method == 'Tournament':
        idxed_strats = list(zip(init_strats, [i for i in range(len(init_strats))]))
        top_idxs = []
        for _ in range(math.floor(self.population/4)):
          shuffle(idxed_strats)
          subset_idxed_strats = idxed_strats[:math.floor(self.population/8)]
          subset_strats, subset_idxs = tuple(zip(*subset_idxed_strats))
          ranks = self.run_brackets(subset_strats)
          ranked_idxs = list(zip(ranks, subset_idxs))
          top_idx = min(ranked_idxs[:math.floor(self.population/8)],key=lambda item:item[0])
          top_idxs.append(top_idx)
          idxed_strats.remove((init_strats[top_idx[1]], top_idx[1]))

    print(top_idxs)
    top_strats = [init_strats[i] for s,i in top_idxs]
    new_strats = top_strats.copy()

    while len(new_strats) < self.population:
      parents = sample(top_strats, 2)
      child_strat = self.breed_strats(parents)
      new_strats.append(child_strat)
    #       new_strats.append(child_strat)
    # for i in range(len(top_strats)):
    #   for j in range(len(top_strats)):
    #     if i!=j:
    #       child_strat = self.breed_strats([top_strats[i],top_strats[j]])
    #       new_strats.append(child_strat)

    return new_strats

  def run_generations(self, num_generations, fitness_score = 'Round Robin',selection_method = 'Hard Cut Off'):
    current_gen = self.strats
    for i in range(num_generations):
      current_gen = self.generate_new_generation(current_gen)
      print('generated generation:',i+1)

    return current_gen

  def run_games_between_gens(self, gen1, gen2):
    gen1_scores = [0 for _ in range(len(gen1))]
    gen2_scores = [0 for _ in range(len(gen2))]
    gen1_players = [StratPlayer(strat) for strat in gen1]
    gen2_players = [StratPlayer(strat) for strat in gen2]
    for i in range(len(gen1)):
      for j in range(len(gen2)):
        players = [gen1_players[i], gen2_players[j]]
        game =  TicTacToe(players)
        game.run_to_completion()
        if game.winner == 1:
          gen1_scores[i] += 1
          gen2_scores[j] -= 1
        elif game.winner == 2:
          gen1_scores[i] -= 1
          gen2_scores[j] += 1

        players = [gen2_players[j], gen1_players[i]]
        game =  TicTacToe(players)
        game.run_to_completion()
        if game.winner == 1:
          gen1_scores[i] -= 1
          gen2_scores[j] += 1
        elif game.winner == 2:
          gen1_scores[i] += 1
          gen2_scores[j] -= 1

    return {"gen1":sum(gen1_scores)/len(gen1_scores), "gen2":sum(gen2_scores)/len(gen2_scores)}

  def get_rows_cols_diags(self, state):
    board = [list(state[i:i+3]) for i in range(0, 9, 3)]
    rows = [[(board[i][j],3*i+j) for j in range(3)] for i in range(3)]
    cols = [[rows[i][j] for i in range(3)] for j in range(3)]
    diags = [[rows[i][i] for i in range(3)],
             [rows[i][2-i] for i in range(3)]]

    return rows + cols + diags
  
  def get_win_captures(self, strat):
    captured_win = 0
    can_win = 0
    for state in strat:
      lines = self.get_rows_cols_diags(state)
      if not (['1','1','1'] in lines or ['2','2','2'] in lines):
        for line in lines:
          line_unzip =  list(zip(*line))
          if line_unzip[0].count('1') == 2 and '0' in line_unzip[0]:
            can_win += 1
            open_space = line_unzip[1][line_unzip[0].index('0')]
            if strat[state] == open_space:
              captured_win += 1
      
    return captured_win / can_win

  def get_loss_preventions(self, strat):
    loss_prevented = 0
    can_prevent = 0
    for state in strat:
      lines = self.get_rows_cols_diags(state)
      if not (['1','1','1'] in lines or ['2','2','2'] in lines):
        for line in lines:
          line_unzip =  list(zip(*line))
          if line_unzip[0].count('2') == 2 and '0' in line_unzip[0]:
            can_prevent += 1
            open_space = line_unzip[1][line_unzip[0].index('0')]
            if strat[state] == open_space:
              loss_prevented += 1
      
    return loss_prevented / can_prevent
  
  def generate_plots(self, num_generations):
    values = {'Round Robin':{'Hard Cut Off':{}, 'Stochastic':{}, 'Tournament':{}},
              'Bracket':{'Hard Cut Off':{}, 'Stochastic':{}, 'Tournament':{}}}

    for fitness_score in values:
      for selection_method in values[fitness_score]:
        print(fitness_score, selection_method)
        values[fitness_score][selection_method]['init_gen_scores'] = []
        values[fitness_score][selection_method]['prev_gen_scores'] = []
        values[fitness_score][selection_method]['win_cap_freq'] = []
        values[fitness_score][selection_method]['loss_prev_freq'] = []
        init_gen = self.strats.copy()
        prev_gen = self.strats.copy()
        
        current_gen = self.strats
        for i in range(num_generations):
          current_gen = self.generate_new_generation(current_gen, fitness_score = fitness_score, selection_method = selection_method)
          print('generated generation:',i+1)
          if i > 0:
            top_strats = current_gen[:math.floor(self.population/4)]
            init_gen_score = self.run_games_between_gens(top_strats, init_gen)['gen1']
            values[fitness_score][selection_method]['init_gen_scores'].append(init_gen_score)
            prev_gen_score = self.run_games_between_gens(top_strats, prev_gen)['gen1']
            values[fitness_score][selection_method]['prev_gen_scores'] .append(prev_gen_score)
            prev_gen = current_gen.copy()
    
            top_win_caps = [self.get_win_captures(strat) for strat in top_strats]
            values[fitness_score][selection_method]['win_cap_freq'].append(sum(top_win_caps)/len(top_win_caps))
    
            top_loss_prevs = [self.get_loss_preventions(strat) for strat in top_strats]
            values[fitness_score][selection_method]['loss_prev_freq'].append(sum(top_loss_prevs)/len(top_loss_prevs))
        
    
    plt.clf()
    plt.title("Genetic Algorithm Initial Generation Comparison")
    for fitness_score in values:
      for selection_method in values[fitness_score]:
        plt.plot([i+1 for i in range(num_generations-1)], values[fitness_score][selection_method]['init_gen_scores'], label = fitness_score + ' ' + selection_method)
    plt.xlabel('Number of Generations')
    plt.ylabel('Average Total Score')
    plt.legend()
    plt.savefig('init_gen_comparison.png')

    plt.clf()
    plt.title("Genetic Algorithm Previous Generation Comparison")
    for fitness_score in values:
      for selection_method in values[fitness_score]:
        plt.plot([i+1 for i in range(num_generations-1)], values[fitness_score][selection_method]['prev_gen_scores'], label = fitness_score + ' ' + selection_method)
    plt.xlabel('Number of Generations')
    plt.ylabel('Average Total Score')
    plt.legend()
    plt.savefig('prev_gen_comparison.png')

    plt.clf()
    plt.title("Genetic Algorithm Win Capture Frequency")
    for fitness_score in values:
      for selection_method in values[fitness_score]:
        plt.plot([i+1 for i in range(num_generations-1)], values[fitness_score][selection_method]['win_cap_freq'], label = fitness_score + ' ' + selection_method)
    plt.xlabel('Number of Generations')
    plt.ylabel('Average Win Capture Frequency')
    plt.legend()
    plt.savefig('win_cap_freq.png')

    plt.clf()
    plt.title("Genetic Algorithm Loss Prevention Frequency")
    for fitness_score in values:
      for selection_method in values[fitness_score]:
        plt.plot([i+1 for i in range(num_generations-1)], values[fitness_score][selection_method]['loss_prev_freq'], label = fitness_score + ' ' + selection_method)
    plt.xlabel('Number of Generations')
    plt.ylabel('Average Loss Prevention Frequency')
    plt.legend()
    plt.savefig('loss_prev_freq.png')
    

  
  
          