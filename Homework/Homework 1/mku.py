'''
Megan Ku
DSA Homework 1 (Code)

Question 3 (strictly ascending lists)
'''

import pytest


def longest_asc(x):
    '''
    Returns the longest sequence of strictly increasing integers.
    x: list of integers
    longest_list: list of the longest sequence of increasing integers found in x

    If there are multiple sub-lists that are the longest, longest_asc() returns the first sequence encountered.
    '''

    # initialize empty lists
    longest_list = []
    curr_list = []

    #iterate through each int in list
    for index, item in enumerate(x):
        curr_list.append(item)

        #check if last list number or if next number is less than current
        if (index == len(x)-1) or (x[index + 1] <= item):
            if len(curr_list) > len(longest_list):
                #if current sequence is longer, replace value of longest_list
                longest_list = curr_list
            curr_list = []
    return longest_list


def test_function():
    '''
    Tests the function longest_asc() for four input cases:
    1. Empty list (should return empty list)
    2. Strictly descending list (should return first value)
    3. Strictly ascending list (should return whole list)
    4. Lists with multiple longest ascending lists (should return first of the multiple)

    '''
    assert longest_asc([]) == []
    assert longest_asc([5, 4, 3, 2, 1]) == [5]
    assert longest_asc([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert longest_asc([1, 2, 3, 1, 4, 3, 5, 6]) == [1, 2, 3]


if __name__ == "__main__":

    x  = [1, 2, 0, 4, 8, 9, 3]

    print(longest_asc(x))
