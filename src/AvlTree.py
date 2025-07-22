""" AVL Tree implementation with the sole goal of making create() as few lines as possible. """

class Comparison:
    Eq = 0
    Gt = 1
    Lt = 2

def cmp(a, b):
    if a - b < 0:
        return Comparison.Lt
    elif a - b > 0:
        return Comparison.Gt
    else:
        return Comparison.Eq

class Node:
    def __init__(self, l, k, v, r, h):
        self.l = l
        self.k = k
        self.v = v
        self.r = r
        self.h = h

def empty():
    return None

def height(tree):
    return tree.h if tree else 0

# 2 crazy one liners, hopefully 1 crazier one liner soon
def create(node):
    aux = [lambda n: Node(n.l, n.k, n.v, n.r, 1 + max(height(n.l), height(n.r))), lambda n, r: aux[0](Node(aux[0](Node(n.l, n.k, n.v, r.l, n.h)), r.k, r.v, r.r, r.h)), lambda n, l: aux[0](Node(l.l, l.k, l.v, aux[0](Node(l.r, n.k, n.v, n.r, n.h)), l.h))]
    return aux[1](node, node.r) if node.r and node.r.r and node.r.r.h > height(node.l) else (aux[1](node, aux[2](node.r, node.r.l)) if node.r and node.r.l and node.r.l.h > height(node.l) else (aux[2](node, aux[1](node.l, node.l.r))) if node.l and node.l.r and node.l.r.h > height(node.r) else (aux[2](node, node.l) if node.l and node.l.l and node.l.l.h > height(node.r) else (aux[0](node))))

def add(k, v, tree):
    if not tree:
        return Node(None, k, v, None, 1)
    
    comparison = cmp(k, tree.k)
    if comparison == Comparison.Eq:
        return create(Node(tree.l, tree.k, v, tree.r, tree.h))
    elif comparison == Comparison.Lt:
        return create(Node(add(k, v, tree.l), tree.k, tree.v, tree.r, tree.h))
    else:
        return create(Node(tree.l, tree.k, tree.v, add(k, v, tree.r), tree.h))

def find(k, tree):
    if not tree:
        return None
    
    comparison = cmp(k, tree.k)
    if comparison == Comparison.Eq:
        return tree.v
    elif comparison == Comparison.Lt:
        return find(k, tree.l)
    else:
        return find(k, tree.r)

def remove(k, tree):
    def pop_successor(n):
        if not n.l:
            return (n.k, n.v), n.r
        successor, new_l = pop_successor(n.l)
        return successor, create(Node(new_l, n.k, n.v, n.r, n.h))
    
    if not tree:
        return None, None
    
    comparison = cmp(k, tree.k)
    if comparison == Comparison.Eq:
        if not tree.r:
            return tree.v, tree.l
        (new_k, new_v), new_r = pop_successor(tree.r)
        return tree.v, create(Node(tree.l, new_k, new_v, new_r, tree.h))
    elif comparison == Comparison.Lt:
        removed_val, new_l = remove(k, tree.l)
        return removed_val, create(Node(new_l, tree.k, tree.v, tree.r, tree.h))
    else:
        removed_val, new_r = remove(k, tree.r)
        return removed_val, create(Node(tree.l, tree.k, tree.v, new_r, tree.h))

def to_list(tree):
    def aux(acc, t):
        if not t:
            return acc
        return aux([(t.k, t.v)] + aux(acc, t.r), t.l)
    return aux([], tree)
