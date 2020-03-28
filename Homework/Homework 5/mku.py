'''
Megan Ku
DSA Homework 5 (Code)

Implementing Min Heaps
'''

import pytest
from hypothesis import given
import hypothesis.strategies as st

class Heap:
    def __init__(self, oglist=None):

        ''' Initialize heap from a (possibly empty) list. '''

        # Handle empty list case
        if oglist is None or oglist == []:
            self.heap = []
        else:
            # Build heap structure
            self.heap = oglist
            back_counter = len(self.heap)//2

            # Move backwards starting at last internal node to sort the values
            while back_counter >= 0:
                curr_idx = back_counter
                curr = self.heap[curr_idx]

                while curr_idx < len(self) - 1:
                    child1_idx = curr_idx*2 + 1
                    child2_idx = child1_idx + 1

                    # Checks edge cases of child1 or child2 not existing
                    if child1_idx > len(self) - 1:
                        break

                    elif child2_idx > len(self) - 1:
                        child1 = self.heap[child1_idx]
                        child2 = None

                    else:
                        child1 = self.heap[child1_idx]
                        child2 = self.heap[child2_idx]

                    #swaps parent value with smaller child if children are smaller than parent
                    if child2 != None:
                        if curr > child1 or curr > child2:
                            if child1 <= child2:
                                self.heap[curr_idx] = child1
                                self.heap[child1_idx] = curr
                                curr_idx = child1_idx

                            else:
                                self.heap[curr_idx] = child2
                                self.heap[child2_idx] = curr
                                curr_idx = child2_idx

                        else:
                            # Break as soon as no more swapping needs to occur
                            break
                    else:
                        if curr > child1:
                            self.heap[curr_idx] = child1
                            self.heap[child1_idx] = curr
                            curr_idx = child1_idx

                        else:
                            break

                # Move backwards through internal nodes
                back_counter = back_counter - 1



    def insert(self, value):
        ''' Insert value into the heap. '''

        # Insert value to end of heap to preserve structure
        self.heap.append(value)

        child_idx = len(self) - 1

        # Percolate downward to maintain sorted tree
        while child_idx > 0:
            if child_idx % 2 == 1:
                parent_idx = int((child_idx - 1)/2)

            else:
                parent_idx = int((child_idx - 2)/2)

            parent = self.heap[parent_idx]

            # Swap child and parent to keep order
            if value < parent:
                self.heap[parent_idx] = value
                self.heap[child_idx] = parent
                child_idx = parent_idx

            else:
                break

    def __len__(self):
        return len(self.heap)

    def delete_min(self):
        ''' Remove the min (root) from heap. '''

        # Store min value that is getting removed
        past_min = self.heap[0]

        last_value = self.heap[len(self) - 1]
        # Set first value to last value in list to preserve complete tree
        self.heap[0] = last_value

        # Remove last element
        self.heap.pop(len(self) - 1)

        # If list is empty, terminate
        if self.heap == []:
            return past_min

        # Otherwise, percolate downward until sorted again
        curr_idx = 0
        curr = self.heap[0]

        while curr_idx < len(self) - 1:
            child1_idx = curr_idx*2 + 1
            child2_idx = child1_idx + 1

            # Checks edge cases of child1 or child2 not existing
            if child1_idx > len(self) - 1:
                break

            elif child2_idx > len(self) - 1:
                child1 = self.heap[child1_idx]
                child2 = None

            else:
                child1 = self.heap[child1_idx]
                child2 = self.heap[child2_idx]

            #swaps parent value with smaller child if children are smaller than parent
            if child2 != None:

                if curr > child1 or curr > child2:

                    if child1 <= child2:
                        self.heap[curr_idx] = child1
                        self.heap[child1_idx] = curr
                        curr_idx = child1_idx

                    else:
                        self.heap[curr_idx] = child2
                        self.heap[child2_idx] = curr
                        curr_idx = child2_idx

                else:
                    # Break as soon as no more swapping needs to occur
                    break
            else:

                if curr > child1:
                    self.heap[curr_idx] = child1
                    self.heap[child1_idx] = curr
                    curr_idx = child1_idx

                else:
                    break

        return past_min

    def find_min(self):
        ''' Return min value in the heap. '''

        return self.heap[0]

    def sorted_list(self):
        ''' Return a sorted list of all heap elements. '''
        # Calls delete_min() to constantly return smallest value
        meep = self
        if len(self) == 0 or len(self) == 1:
            return self.heap

        final_list = []

        for i in range(len(self)):
            final_list.append(meep.delete_min())

        return final_list


@given(st.lists(st.integers()))
def test_heap_insert_and_delete_min(l):
    '''
    Tests insert and delete_min on an empty heap.
    '''
    h = Heap()

    assert len(h) == 0

    for i in range(len(l)):
        h.insert(l[i])
        # Check that length matches
        assert len(h) == i + 1

    for j in range(len(l)):

        # Check that the value removed was actually the minimum
        assert h.delete_min() == min(l)
        l.remove(min(l))
        # Check that item has been deleted
        assert len(h) == len(l)


@given(st.lists(st.integers()))
def test_heap_delete_min(l):
    '''
    Tests delete_min on heap with list as parameter.
    '''
    h = Heap(l)
    size = len(l)

    for j in range(size):
        min_list = min(l)
        # Check that value removed was actually the minimum
        assert h.delete_min() == min_list
        # Check that item has been deleted
        assert len(h) == len(l)

@given(st.lists(st.integers()))
def test_sort(l):
    '''
    Tests sorted_list function against built-in python sort() function
    '''
    h = Heap(l)
    l2 = l.copy()
    l2.sort()

    if l == []:
        # Checks empty case
        assert h.sorted_list() == []
    else:
        # Checks non-empty case
        assert h.sorted_list() == l2
