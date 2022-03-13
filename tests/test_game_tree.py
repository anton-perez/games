import sys
sys.path.append('games')
from game_tree import *

tree = GameTree('X')

print('Building game tree...')
#tree.build_tree(tree.root)
tree.set_scores(tree.root, 'X')
print('FINISHED')

print(tree.node_num)
print(tree.leaf_node_num)
print(tree.root.score)

node = tree.get_node([[None,None,None], [None,None,None],[None,None,None]])
print(node.score)
node.print_state()

node = tree.get_node([['X','O',None], ['O','X',None],[None,None,None]])
print(node.score)
node.print_state()
# for child in tree.root.children:
#   print(child.score)
#   child.print_state()

