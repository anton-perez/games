import sys
sys.path.append('algorithms')
from ttt_neural_net import *
sys.path.append('games')
from tic_tac_toe import *
sys.path.append('players')
from random_player import *
from ttt_minimax_player import *
from ttt_input_player import *
from ttt_np_player import *
from ttt_nn_player import *

net = TTTNeuralNetwork()
net.initialize()
players = [NeuralNetPlayer(net), NearPerfectPlayer()]
game = TicTacToe(players)
game.run_to_completion()
winner = game.winner