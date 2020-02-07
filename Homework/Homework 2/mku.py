'''
Megan Ku
DSA Homework 2 (Code)

Question 1 (strictly ascending lists)
'''

import pytest
import timeit
import random

class Node():
    def __init__(self, val=None, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next


class DLL():
    def __init__(self):
        '''
        Constructor for an empty list.
        '''

        self.head = None
        self.tail = None


    def length(self):
        '''
        Returns the number of nodes in the list.
        '''

        length = 0
        curr_node = self.head

        # Traverse DLL to count elements in list
        while curr_node != None:
            length += 1
            curr_node = curr_node.next

        return length

    def push(self, val):
        '''
        Adds a node with val equal to val to the front of the list
        val = value for node
        '''
        #initialize new node with given value
        node = Node(val=val)

        #if DLL isn't empty, assign the new 'next' and 'prev'
        if not self.head:
            self.tail = node
        else:
            self.head.prev = node
            node.next = self.head

        #make this node the new head
        self.head = node

    def insert(self, val, given_node):
        '''
        Initializes and inserts node into DLL after given_node.
        val = value for node
        given_node = node
        '''
        node = Node(val=val, prev=given_node)
        if given_node.next == None:
            self.tail = node
        else:
            next_node = given_node.next
            node.next = next_node
            next_node.prev = node
        given_node.next = node

    def delete(self, node):
        '''
        Deletes a given node from a DLL.

        '''
        if node == self.head:
            self.head = self.head.next
            self.head.prev = None
        else:
            node.prev.next = node.next
        if node == self.tail:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            node.next.prev = node.prev

    def index(self, number):
        '''
        Returns the node at a given index in the DLL.

        curr_node: Node object
        '''
        curr_node = self.head
        for i in range(number):
            curr_node = curr_node.next
        return curr_node

    def multiply_all_pairs(self):
        '''
        Returns the sum of the products of all unique pair combinations in the DLL.

        sum = sum of all the products of unique pairs.
        '''
        sum = 0
        x = self.head
        y = self.head
            #traverse through list, adding combinations to sum
        while x:
            while y:
                if x is not y:
                    sum += x.val*y.val
                y = y.next
            x = x.next
            y = self.head

        sum /= 2

        return sum

    def multiply_all_pairs_linear(self):
        '''
        A linear approach to multiplying all pairs given understanding of
        algebra. Returns the same sum as multiply_all_pairs().

        For a given list [a, b, c,...n], the sum of all combinations is equal to
        1/2((a + b + c + .. + n)^2 - (a^2 + b^2 + c^2))

        A = (a + b + c + .. + n)^2
        B = (a^2 + b^2 + c^2)

        sum = 1/2(A - B)
        '''
        A = 0
        B = 0
        curr_node = self.head
        if curr_node == None:
            return 0
        for i in range(self.length()):
            A += curr_node.val
            B += curr_node.val**2
            curr_node = curr_node.next

        sum = 1/2*(A**2-B)
        return sum


'''
--------------------------------------------------------------------------------
TEST FUNCTIONS
run pytest mku.py in command line to run test functions
'''

def test_multiply():
    '''
    Tests both multiply_all_pairs() and multiply_all_pairs_linear() for several cases:
    1. Empty DLL
    2. DLL with one node
    3. DLL with more than one node

    '''

    # Check case if DLL is empty (should return 0)
    my_DLL = DLL()
    assert my_DLL.multiply_all_pairs() == 0
    assert my_DLL.multiply_all_pairs() == my_DLL.multiply_all_pairs_linear()

    # Check case if DLL has length of 1 (should return 0)
    my_DLL.push(1)
    assert my_DLL.multiply_all_pairs() == 0
    assert my_DLL.multiply_all_pairs() == my_DLL.multiply_all_pairs_linear()

    my_DLL.push(2)
    my_DLL.push(3)
    my_DLL.push(4)

    #check if function actually solves for the sum of all product pairs
    assert my_DLL.multiply_all_pairs() == 35
    assert my_DLL.multiply_all_pairs() == my_DLL.multiply_all_pairs_linear()

def test_length():
    '''
    Check if correct length is returned for following cases:
    1. Empty DLL
    2. DLL with more than one node
    '''

    # Check length of empty DLL (should return 0)
    my_DLL = DLL()
    assert my_DLL.length() == 0

    # Check length of DLL (should return 4)
    my_DLL.push(1)
    my_DLL.push(2)
    my_DLL.push(3)
    my_DLL.push(4)
    assert my_DLL.length() == 4

def test_push():
    '''
    tests push() method for following cases:
    1. adding to empty DLL
    2. adding to DLL that already contains nodes

    '''
    # Check if pushed to empty DLL
    my_DLL = DLL()
    my_DLL.push(1)
    assert my_DLL.head.val == 1
    assert my_DLL.length() == 1

    #check if pushed to non-empty DLL
    my_DLL.push(2)
    my_DLL.push(3)
    my_DLL.push(4)
    assert my_DLL.length() == 4
    assert my_DLL.head.val == 4

def test_insert():
    '''
    tests insert() method for following cases:
    1. Inserting after the first node
    2. Inserting at the end
    '''

    my_DLL = DLL()
    my_DLL.push(1)
    my_DLL.push(2)
    # Check if node gets inserted correctly
    firstNode = my_DLL.head
    my_DLL.insert(3, firstNode)
    assert my_DLL.head.next.val == 3

    # Check if node gets inserted correctly at end
    lastNode = my_DLL.tail
    my_DLL.insert(4, lastNode)
    assert my_DLL.tail.val == 4


def test_delete():
    '''
    Tests delete() method for following cases:
    1. deleting head
    2. deleting tail
    3. deleting in the middle
    '''
    my_DLL = DLL()
    my_DLL.push(1)
    my_DLL.push(2)
    my_DLL.push(3)
    my_DLL.push(4)
    my_DLL.push(5)
    my_DLL.push(6)

    # Check that first value was deleted
    my_DLL.delete(my_DLL.head)
    assert my_DLL.head.val == 5

    #Check that last value was deleted
    my_DLL.delete(my_DLL.tail)
    assert my_DLL.tail.val == 2

    #Check if middle value was deleted
    my_DLL.delete(my_DLL.index(1))
    assert my_DLL.index(1).val == 3

def test_index():
    '''
    Tests index() method for following cases:
    1. indexing at 0
    2. indexing at the end of the DLL
    3. indexing in the middle of the list

    '''
    my_DLL = DLL()
    my_DLL.push(1)
    my_DLL.push(2)
    my_DLL.push(3)
    my_DLL.push(4)
    my_DLL.push(5)
    my_DLL.push(6)

    # Check value at index of 0 (should be 6)
    assert my_DLL.index(0).val == 6

    # Check value in middle of list
    assert my_DLL.index(3).val == 3

    # Check value at end of list (should be 1)
    assert my_DLL.index(my_DLL.length()-1).val == 1
