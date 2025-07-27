""" Some simple unit tests for my AVL Tree. These were all GPT'd. We should really just use PyTest. """

from avl_tree import *

# Helper functions for testing
def is_balanced(tree):
    """Check if the tree satisfies AVL balance property"""
    if not tree:
        return True
    
    left_height = height(tree.l)
    right_height = height(tree.r)
    balance_factor = left_height - right_height
    
    return abs(balance_factor) <= 1 and is_balanced(tree.l) and is_balanced(tree.r)

def is_bst(tree, min_val=float('-inf'), max_val=float('inf')):
    """Check if the tree satisfies BST property"""
    if not tree:
        return True
    
    if tree.k <= min_val or tree.k >= max_val:
        return False
    
    return is_bst(tree.l, min_val, tree.k) and is_bst(tree.r, tree.k, max_val)

def get_keys_inorder(tree):
    """Get keys in inorder traversal"""
    return [k for k, v in to_list(tree)]


# Test suite
def test_empty_tree():
    """Test operations on empty tree"""
    tree = empty()
    assert tree is None
    assert find(10, tree) is None
    removed, tree = remove(10, tree)
    assert removed is None
    assert tree is None
    assert to_list(tree) == []
    print("✓ Empty tree tests passed")

def test_single_node():
    """Test single node operations"""
    tree = empty()
    tree = add(10, "ten", tree)
    assert find(10, tree) == "ten"
    assert find(5, tree) is None
    assert to_list(tree) == [(10, "ten")]
    assert height(tree) == 1
    assert is_balanced(tree)
    assert is_bst(tree)
    
    removed, tree = remove(10, tree)
    assert removed == "ten"
    assert tree is None
    print("✓ Single node tests passed")

def test_basic_insertions():
    """Test basic insertions and lookups"""
    tree = empty()
    
    # Insert multiple elements
    elements = [(5, "five"), (3, "three"), (7, "seven"), (2, "two"), 
                (4, "four"), (6, "six"), (8, "eight")]
    
    for k, v in elements:
        tree = add(k, v, tree)
    
    # Verify all elements are findable
    for k, v in elements:
        assert find(k, tree) == v
    
    # Verify non-existent elements
    assert find(1, tree) is None
    assert find(9, tree) is None
    
    # Verify order
    keys = get_keys_inorder(tree)
    assert keys == [2, 3, 4, 5, 6, 7, 8]
    
    # Verify balance and BST properties
    assert is_balanced(tree)
    assert is_bst(tree)
    print("✓ Basic insertion tests passed")

def test_duplicate_keys():
    """Test updating values for duplicate keys"""
    tree = empty()
    tree = add(10, "first", tree)
    tree = add(10, "second", tree)
    tree = add(10, "third", tree)
    
    assert find(10, tree) == "third"
    assert to_list(tree) == [(10, "third")]
    print("✓ Duplicate key tests passed")

def test_left_rotation():
    """Test left rotation (RR case)"""
    tree = empty()
    tree = add(1, "1", tree)
    tree = add(2, "2", tree)
    tree = add(3, "3", tree)  # This should trigger left rotation
    
    # After rotation, 2 should be root
    assert tree.k == 2
    assert tree.l.k == 1
    assert tree.r.k == 3
    assert is_balanced(tree)
    assert is_bst(tree)
    print("✓ Left rotation tests passed")

def test_right_rotation():
    """Test right rotation (LL case)"""
    tree = empty()
    tree = add(3, "3", tree)
    tree = add(2, "2", tree)
    tree = add(1, "1", tree)  # This should trigger right rotation
    
    # After rotation, 2 should be root
    assert tree.k == 2
    assert tree.l.k == 1
    assert tree.r.k == 3
    assert is_balanced(tree)
    assert is_bst(tree)
    print("✓ Right rotation tests passed")

def test_left_right_rotation():
    """Test left-right rotation (LR case)"""
    tree = empty()
    tree = add(3, "3", tree)
    tree = add(1, "1", tree)
    tree = add(2, "2", tree)  # This should trigger LR rotation
    
    # After rotation, 2 should be root
    assert tree.k == 2
    assert tree.l.k == 1
    assert tree.r.k == 3
    assert is_balanced(tree)
    assert is_bst(tree)
    print("✓ Left-right rotation tests passed")

def test_right_left_rotation():
    """Test right-left rotation (RL case)"""
    tree = empty()
    tree = add(1, "1", tree)
    tree = add(3, "3", tree)
    tree = add(2, "2", tree)  # This should trigger RL rotation
    
    # After rotation, 2 should be root
    assert tree.k == 2
    assert tree.l.k == 1
    assert tree.r.k == 3
    assert is_balanced(tree)
    assert is_bst(tree)
    print("✓ Right-left rotation tests passed")

def test_complex_insertions():
    """Test complex insertion sequence"""
    tree = empty()
    
    # Insert sequence that triggers multiple rotations
    sequence = [10, 20, 30, 40, 50, 25]
    for k in sequence:
        tree = add(k, str(k), tree)
        assert is_balanced(tree)
        assert is_bst(tree)
    
    # Verify final structure
    keys = get_keys_inorder(tree)
    assert keys == [10, 20, 25, 30, 40, 50]
    
    # Verify all values
    for k in sequence:
        assert find(k, tree) == str(k)
    print("✓ Complex insertion tests passed")

def test_removals():
    """Test removal operations"""
    tree = empty()
    
    # Build a tree
    for i in range(1, 8):
        tree = add(i, str(i), tree)
    
    # Remove leaf node
    removed, tree = remove(1, tree)
    assert removed == "1"
    assert find(1, tree) is None
    assert is_balanced(tree)
    assert is_bst(tree)
    
    # Remove node with one child
    removed, tree = remove(2, tree)
    assert removed == "2"
    assert find(2, tree) is None
    assert is_balanced(tree)
    assert is_bst(tree)
    
    # Remove node with two children
    removed, tree = remove(4, tree)
    assert removed == "4"
    assert find(4, tree) is None
    assert is_balanced(tree)
    assert is_bst(tree)
    
    # Verify remaining elements
    remaining = get_keys_inorder(tree)
    assert remaining == [3, 5, 6, 7]
    print("✓ Removal tests passed")

def test_remove_root():
    """Test removing root node"""
    tree = empty()
    tree = add(2, "two", tree)
    tree = add(1, "one", tree)
    tree = add(3, "three", tree)
    
    removed, tree = remove(2, tree)
    assert removed == "two"
    assert find(2, tree) is None
    assert is_balanced(tree)
    assert is_bst(tree)
    assert get_keys_inorder(tree) == [1, 3]
    print("✓ Remove root tests passed")

def test_remove_nonexistent():
    """Test removing non-existent keys"""
    tree = empty()
    tree = add(10, "ten", tree)
    
    removed, tree = remove(20, tree)
    assert removed is None
    assert find(10, tree) == "ten"
    print("✓ Remove non-existent tests passed")

def test_large_tree():
    """Test with larger tree"""
    tree = empty()
    n = 100
    
    # Insert n elements
    for i in range(n):
        tree = add(i, f"value_{i}", tree)
    
    # Verify all elements
    for i in range(n):
        assert find(i, tree) == f"value_{i}"
    
    # Verify balance
    assert is_balanced(tree)
    assert is_bst(tree)
    
    # Verify order
    keys = get_keys_inorder(tree)
    assert keys == list(range(n))
    
    # Remove half the elements
    for i in range(0, n, 2):
        removed, tree = remove(i, tree)
        assert removed == f"value_{i}"
    
    # Verify remaining elements
    for i in range(1, n, 2):
        assert find(i, tree) == f"value_{i}"
    
    assert is_balanced(tree)
    assert is_bst(tree)
    print("✓ Large tree tests passed")

def test_height_calculation():
    """Test height calculation"""
    tree = empty()
    assert height(tree) == 0
    
    tree = add(1, "1", tree)
    assert height(tree) == 1
    
    tree = add(2, "2", tree)
    assert height(tree) == 2
    
    tree = add(3, "3", tree)  # Triggers rotation
    assert height(tree) == 2  # Height should be 2 after rotation
    print("✓ Height calculation tests passed")

# Run all tests
if __name__ == "__main__":
    print("Running AVL Tree Tests...\n")
    
    test_empty_tree()
    test_single_node()
    test_basic_insertions()
    test_duplicate_keys()
    test_left_rotation()
    test_right_rotation()
    test_left_right_rotation()
    test_right_left_rotation()
    test_complex_insertions()
    test_removals()
    test_remove_root()
    test_remove_nonexistent()
    test_large_tree()
    test_height_calculation()
    
    print("\n✅ All tests passed!")