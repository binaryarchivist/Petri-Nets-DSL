from tree import Node

# Ex 1 [2, 3] 2 [4], 3 [5, 6], 4 [7], 5 [7], 6 [8]

root = Node(1)
n2 = Node(2)
n3 = Node(3)

root.add_subnode(n2)
root.add_subnode(n3)

n4 = Node(4)
n5 = Node(5)
n6 = Node(6)

n2.add_subnode(n4)
n3.add_subnode(n5)
n3.add_subnode(n6)

n7 = Node(7)
n8 = Node(8)

n4.add_subnode(n7)
n5.add_subnode(n7)
n6.add_subnode(n8)

print(root.find_paths_to_last_nodes())

root.draw_tree()