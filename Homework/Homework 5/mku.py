'''
Megan Ku
DSA Homework 5 (Code)

Implementing Min Heaps
'''

import pytest
from hypothesis import given
import hypothesis.strategies as st

class Heap:
    def __init__(self, oglist=[]):
        ''' Initialize heap from a (possibly empty) list. '''
        self.heap = oglist

    def length(self):
        ''' Return length of the heap. '''

        return len(self.heap)

    def insert(self, value):
        ''' Insert value into the heap. '''

        self.heap.append(value)

        child_idx = self.length() - 1

        while child_idx > 0:
            if child_idx % 2 == 1:
                parent_idx = int((child_idx - 1)/2)
            else:
                parent_idx = int((child_idx - 2)/2)

            parent = self.heap[parent_idx]

            if value < parent:
                self.heap[parent_idx] = value
                self.heap[child_idx] = parent
                child_idx = parent_idx

            else:
                break


    def delete_min(self):
        ''' Remove the min (root) from heap. '''

        # Store min value that is getting removed
        past_min = self.heap[0]

        # Set first value to last value in list to preserve complete tree
        self.heap[0] = self.heap[self.length() - 1]

        # Remove last element
        self.heap.pop(self.length() - 1)

        # If list is empty, terminate
        if self.heap == []:
            return past_min

        # Otherwise, percolate downward until sorted again
        curr_idx = 0
        curr = self.heap[0]

        while curr_idx < self.length() - 1:

            child1_idx = curr_idx*2 + 1
            child2_idx = child1_idx + 1

            # Checks edge cases of child1 or child2 not existing
            if child1_idx > self.length() - 1:
                break
            elif child2_idx > self.length() - 1:
                child1 = self.heap[child1_idx]
                child2 = None
            else:
                child1 = self.heap[child1_idx]
                child2 = self.heap[child2_idx]

            #swaps parent value with smaller child if children are smaller than parent
            if child2:
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
        meep = self
        final_list = []
        for i in range(self.length()):
            final_list.append(meep.delete_min())
        return final_list


@given(st.lists(st.integers()))
def test_heap_insert_and_delete_min(l):

    h = Heap()
    print(h.heap)
    assert h.length() == 0

    for i in range(len(l)):
        h.insert(l[i])
        assert h.length() == i + 1


    for j in range(len(l)):
        assert h.delete_min() == min(l)
        l.remove(min(l))
        assert h.length() == len(l)


#@given(st.lists(st.integers()))
# def test_heap_delete_min():
#     l = [16, -2230046943609019054, 1709591971, 9658, 9904, -1776378205]
#     h = Heap(l)
#     print("Initial Heap:", h.heap)
#     for j in range(len(l)):
#         h.delete_min()
#         print(h.heap)
#         #assert h.delete_min() == min(l)
#         #l.remove(min(l))
#         # assert h.length() == len(l)
#         # print(h.heap)
#     assert h.length() == 0
