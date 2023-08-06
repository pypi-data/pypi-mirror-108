"""
class:

TreeNode(val=0, left=None, right=None)

method:

TreeNode <- fromArray(ls: [list, str])
list     <- toArray(root: TreeNode)
str      <- toStr(root: TreeNode)
None     <- draw(root: [TreeNode, str])
"""

from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import math


"""
Definition for a binary tree node.
"""
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    

"""
fromArrayToTree(ls: list) -> TreeNode
"""
def fromArray(ls):
    if len(ls) == 0: return None
    if isinstance(ls, str):
        ls = ls.strip("[]")
        ls = ls.split(',')
        ls = [None if v == "null" else int(v) for v in ls]
    
    root = TreeNode(ls[0])
    queue = deque([root])
    i = 1
    while i < len(ls)-1:
        node = queue.popleft()
        if ls[i]:
            node.left = TreeNode(ls[i])
            queue.append(node.left)
        if ls[i+1]:
            node.right = TreeNode(ls[i+1])
            queue.append(node.right)
        i += 2
        
    if i == len(ls)-1:
        node = queue.popleft()
        node.left = TreeNode(ls[i]) if ls[i] else None
    return root


def toArray(root):
    result = []
    queue = deque([root])
    while len(queue) > 0:
        node = queue.popleft()
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    while len(result) > 0 and result[-1] == None:
        result.pop()
    return result


def toStr(root):
    result = []
    queue = deque([root])
    while len(queue) > 0:
        node = queue.popleft()
        if node:
            result.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append("null")
    while len(result) > 0 and result[-1] == "null":
        result.pop()
    return "[" + ",".join(result) + "]"


    
"""
Draw tree graph
drawTree(root: TreeNode) -> None
"""
def draw(root):
    if root == None:
        return
    if isinstance(root, str):
        root = fromArray(root)
    def create_graph(G, node, pos={}, x=0, y=0, layer=1):
        G.add_node(id(node), desc=node.val)
        pos[id(node)] = (x, y)
        
        mlayer = 0
        if node.left:
            G.add_edge(id(node), id(node.left))
            l_x, l_y = x - 1 / 2 ** layer, y - 1
            l_layer = layer + 1
            _, _, mlayer = create_graph(G, node.left, x=l_x, y=l_y, pos=pos, layer=l_layer)
        if node.right:
            G.add_edge(id(node), id(node.right))
            r_x, r_y = x + 1 / 2 ** layer, y - 1
            r_layer = layer + 1
            _, _, mlayer = create_graph(G, node.right, x=r_x, y=r_y, pos=pos, layer=r_layer)
        
        mlayer = max(mlayer, layer)
        return (G, pos, mlayer)
    
    graph = nx.DiGraph()
    graph, pos, height = create_graph(graph, root)
    # print('width={}, height={}'.format(height*math.log(height), height))
    fig, ax = plt.subplots(figsize=(height*math.log(height, 2)+1, height))
    
    nx.draw(graph, pos, ax=ax, node_color='#d8f7fa', node_size=300)
    node_labels = nx.get_node_attributes(graph, 'desc')
    nx.draw_networkx_labels(graph, pos, labels=node_labels)
    plt.show() 