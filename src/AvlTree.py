""" AVL Tree implementation with the sole goal of making create() as few lines as possible. """

from enum import Enum

class Comparison(Enum):
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

# the craziest one liner
def create(node):
    return (
        # walrus operator goated
        (make := lambda n:    Node(n.l, n.k, n.v, n.r, 1 + max(height(n.l), height(n.r)))) and
        (rotl := lambda n, r: Node(make(Node(n.l, n.k, n.v, r.l, 0)), r.k, r.v, r.r, 0)) and
        (rotr := lambda n, l: Node(l.l, l.k, l.v, make(Node(l.r, n.k, n.v, n.r, 0)), 0)) and
        # rename because node.l and node.r is verbose
        ((l := node.l) or True) and # or True to handle node = None case
        ((r := node.r) or True) and
        # poor mans match statement
        make(
            rotl(node, r)            if r and r.r and r.r and r.r.h > height(l) else(
            rotl(node, rotr(r, r.l)) if r and r.l and r.l and r.l.h > height(l) else(
            rotr(node, rotl(l, l.r)) if l and l.r and l.r and l.r.h > height(r) else(
            rotr(node, l)            if l and l.l and l.l and l.l.h > height(r) else(
            node
            ))))
        )
    )

def add(k, v, tree):
    if not tree:
        return Node(None, k, v, None, 1)
    
    comparison = cmp(k, tree.k)
    match comparison:
        case Comparison.Eq:
            return create(Node(tree.l, tree.k, v, tree.r, tree.h))
        case Comparison.Lt:
            return create(Node(add(k, v, tree.l), tree.k, tree.v, tree.r, tree.h))
        case Comparison.Gt:
            return create(Node(tree.l, tree.k, tree.v, add(k, v, tree.r), tree.h))
        case _:
            raise Exception("Should be unreachable")

def find(k, tree):
    if not tree:
        return None
    
    comparison = cmp(k, tree.k)
    match comparison:
        case Comparison.Eq:
            return tree.v
        case Comparison.Lt:
            return find(k, tree.l)
        case Comparison.Gt:
            return find(k, tree.r)
        case _:
            raise Exception("Should be unreachable")

def remove(k, tree):
    def pop_successor(n):
        if not n.l:
            return (n.k, n.v), n.r
        successor, new_l = pop_successor(n.l)
        return successor, create(Node(new_l, n.k, n.v, n.r, n.h))
    
    if not tree:
        return None, None
    
    comparison = cmp(k, tree.k)
    match comparison:
        case Comparison.Eq:
            if not tree.r:
                return tree.v, tree.l
            (new_k, new_v), new_r = pop_successor(tree.r)
            return tree.v, create(Node(tree.l, new_k, new_v, new_r, tree.h))
        case comparison.Lt:
            removed_val, new_l = remove(k, tree.l)
            return removed_val, create(Node(new_l, tree.k, tree.v, tree.r, tree.h))
        case comparison.Gt:
            removed_val, new_r = remove(k, tree.r)
            return removed_val, create(Node(tree.l, tree.k, tree.v, new_r, tree.h))
        case _:
            raise Exception("Should be unreachable")

def to_list(tree):
    def aux(acc, t):
        if not t:
            return acc
        return aux([(t.k, t.v)] + aux(acc, t.r), t.l)
    return aux([], tree)
