import sys
sys.path.append('trees')
from game_tree import *

tree = GameTree('1')

print('Building game tree...')
#tree.build_tree(tree.root)
tree.set_scores(tree.root, '1')
print('FINISHED')

print(tree.node_num)
print(tree.leaf_node_num)
print(tree.root.score)

node = tree.get_node([[None,None,None], [None,None,None],[None,None,None]])
print(node.score)
node.print_state()

node = tree.get_node([['1','2',None], ['2','1',None],[None,None,None]])
print(node.score)
node.print_state()
# for child in tree.root.children:
#   print(child.score)
#   child.print_state()

