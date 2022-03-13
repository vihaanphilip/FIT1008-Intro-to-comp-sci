""" AVL Tree implemented on top of the standard BST. """

__author__ = 'Alexey Ignatiev'
__docformat__ = 'reStructuredText'

from bst import BinarySearchTree
from typing import TypeVar, Generic
from node import AVLTreeNode

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """ Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        BinarySearchTree.__init__(self)

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current.height if current is 
            not None. Otherwise, return 0.
            :complexity: O(1)
        """

        # if current is None, then return 0
        if current is None:
            return 0
        
        # Otherwise, return current.height
        return current.height


    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.
            :complexity: O(1)
        """

        if current is None:
            return 0
        
        return self.get_height(current.right) - self.get_height(current.left)

    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert
            it. After insertion, performs sub-tree rotation whenever it becomes
            unbalanced.
        """

        if current is None:  # base case: at the leaf
            current = AVLTreeNode(key, item)
            self.length += 1
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
            if current.height < current.left.height+1:
                current.height = current.left.height+1
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
            if current.height < current.right.height+1:
                current.height = current.right.height+1
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')

        current = self.rebalance(current)

        return current

    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete. After deletion,
            performs sub-tree rotation whenever it becomes unbalanced.
        """

        if current is None:  # key not found
            return current

        elif key < current.key:
            current.left  = self.delete_aux(current.left, key)

        elif key > current.key:
            current.right = self.delete_aux(current.right, key)

        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key  = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

            self.rebalance(current)

        return current

    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            :complexity: O(1)
        """

        right_child = current.right
        current.right = right_child.left
        right_child.left = current

        current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1
        right_child.height = max(self.get_height(right_child.left), self.get_height(right_child.right)) + 1
        

        #self.root = right_child

        return right_child

    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :complexity: O(1)
        """

        left_child = current.left
        current.left = left_child.right
        left_child.right = current

        current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1
        left_child.height = max(self.get_height(left_child.left), self.get_height(left_child.right)) + 1

        return left_child

    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """ Compute the balance of the current node.
            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
        """

        if self.get_balance(current) >= 2:
            child = current.right

            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            
            return self.left_rotate(current)
        
        if self.get_balance(current) <= -2:
            child = current.left

            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            
            return self.right_rotate(current) 

        return current

if __name__ == '__main__':
    
    tree = AVLTree()
    tree[20] = 1
    tree[14] = 1
    tree[23] = 1
    tree[24] = 1
    tree[25] = 1
    tree[16] = 1
    tree[1] = 1
    tree[2] = 1
    tree[3] = 1
    tree[4] = 1
    tree[5] = 1
    tree[6] = 1

    tree.draw()

    print(tree.get_height(tree.root))

    del tree[4]
    #print(tree.get_successor(tree.root.left))

    tree.draw()

    #print(tree.get_balance(tree.root.left))

    #tree.root.right.right = tree.rebalance(tree.root.right.right)

    #print(tree.get_height(tree.root.right.right))

    #tree.draw()
    
    """
    tree1 = AVLTree()
    tree1.root = AVLTreeNode(10)
    tree1.root.left = AVLTreeNode(20)
    tree1.root.left.left = AVLTreeNode(80)
    tree1.root.left.right = AVLTreeNode(40)
    tree1.root.right = AVLTreeNode(35)
    print("TREE 1:")
    tree1.draw()
    print(tree1.get_height(tree1.root))
    """
    """
    # Helper methods, to construct trees directly.
    def make_leaf(key):
        node = AVLTreeNode(key)
        node.height = 1
        return node

    def make_node(key, left, right):
        node = AVLTreeNode(key)
        node.left = left
        node.right = right
        node.height = 1 + max(left.height, right.height)
        return node

    def make_tree(root):
        tree = AVLTree()
        tree.root = root
        return tree
    
    tree2 = make_tree( 
                make_node(8, make_node(120, make_node(60, make_node(30, make_leaf(9), make_leaf(44)), make_leaf(11)),
                        make_node(180,
                            make_leaf(147),
                            make_leaf(190)
                            )
                        ),
                    make_leaf(200)
                    )
                )

    tree2.draw()
    """

    #print(tree2.get_height(tree2.root.right))
    #print(tree2.root.left)
    #tree2.right_rotate(tree2.root)
    #tree2.draw()


    #print(tree2.get_balance(tree2.root))
    #tree2.root = tree2.rebalance(tree2.root)
    #tree2.draw()
    #print(tree2.get_balance(tree2.root))

    #tree2.root = tree2.rebalance(tree2.root)
    #tree2.draw()
    #print(tree2.get_balance(tree2.root))
    