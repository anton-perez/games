import math, random
import sys
sys.path.append('games')
from tic_tac_toe import *
sys.path.append('algorithms')
from genetic_algorithm import *
sys.path.append('players')
from strat_player import *
from ttt_input_player import *

initial_strats = [generate_random_strat() for _ in range(25)]

ga = GeneticAlgorithm(initial_strats)
ga.run_generations(50)
#print(ga.strats[0])

players = [InputPlayer(), ga.players[0]]
game = TicTacToe(players)
game.run_to_completion()