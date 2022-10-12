import math, random
from random import shuffle
import sys
sys.path.append('games')
from tic_tac_toe import *
from genetic_algorithm import *
sys.path.append('players')
from strat_player import *

# initial_strats = [generate_random_strat() for _ in range(25)]

ga = GeneticAlgorithm(32, 0.001)
# print(ga.strats[0])
final_strats = ga.run_generations(10)
#print(final_strats[0])
# ga.generate_plots(30)