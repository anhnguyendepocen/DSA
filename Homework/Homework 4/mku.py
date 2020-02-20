'''
Megan Ku
DSA Homework 4 (Code)

Questions 3-5: Implementing the Happy Meals
'''

import pytest
from sys import maxsize
import numpy as np


def happiest_meal(happy_meal, start, end):
    '''
    Uses divide-and-conquer method to find largest sub-list sum.

    happy_meal: list of happiness values
    start: starting index of happy_meal
    end: ending index of happy_meal

    Returns (sum, start, end) where
    sum: maximum sum
    start: starting index of max sub-list
    end: ending index of max sub-list

    '''

    # base case
    if start == end:
        return (happy_meal[start], start, end)

    else:
        # define midpoint to split problem in half
        mid = (start + end) // 2

        # find maximum sums for each of the three cases: all in left half, all in right half, or crossing the midpoint
        (happiest_left, l_start, l_end) = happiest_meal(happy_meal, start, mid)
        (happiest_right, r_start, r_end) = happiest_meal(happy_meal, mid+1, end)
        (happiest_cross, m_start, m_end) = happiest_crossing_meal(happy_meal, start, mid, end)

        # return the max of the three above cases
        if happiest_left > happiest_right and happiest_left > happiest_cross:
            return (happiest_left, l_start, l_end)

        elif happiest_right > happiest_left and happiest_right > happiest_cross:
            return (happiest_right, r_start, r_end)

        else:
            return (happiest_cross, m_start, m_end)


def happiest_crossing_meal(happy_meal, start, mid, end):
    '''
    Finds largest crossing sum.

    happy_meal: list of happiness values
    start: starting index of happy_meal
    end: ending index of happy_meal

    Returns (sum, start, end) where
    sum: maximum sum
    start: starting index of max sub-list
    end: ending index of max sub-list

    '''

    #set original mex_sum to smallest possible number
    l_max_sum = -maxsize - 1
    r_max_sum = -maxsize - 1

    #set index to points at midpoint
    l_index = mid
    r_index = mid + 1

    l_sum = 0

    #sum from the middle leftward, saving max running total
    for i in range(mid, start - 1, -1):
        l_sum += happy_meal[i]
        if l_sum > l_max_sum:
            l_max_sum = l_sum
            l_index = i

    r_sum = 0

    #sum from the middle rightward, saving max running total
    for i in range(mid+1, end+1, 1):
        r_sum += happy_meal[i]
        if r_sum > r_max_sum:
            r_max_sum = r_sum
            r_index = i

    #sum of two max sums is greatest crossing sum
    return (l_max_sum + r_max_sum, l_index, r_index)


def test_happiest_meal():
    '''
    Test function checks the following cases:
    1. list of all positive values (should return whole list)
    2. list of all negative values (should return greatest value)
    3. list with both positive and negative values (typical case)
    4. list with one element (base case)
    '''

    pos_list = [1, 2, 2, 2, 8, 45]
    assert happiest_meal(pos_list, 0, 5) == (60, 0, 5)

    neg_list = [-34, -42, -16, -5]
    assert happiest_meal(neg_list, 0, 3) == (-5, 3, 3)

    mix_list = [3, -2, 1, 5, -6]
    assert happiest_meal(mix_list, 0, 4) == (7, 0, 3)

    smol_list = [3]
    assert happiest_meal(smol_list, 0, 0) == (3, 0, 0)

def mean_happy_uniform():
    '''
    Creates pseudorandom lists and runs find_happiest_meal.
    Returns mean of max sums and lengths of sublists.
    '''
    max_happy = np.zeros(100)
    sublist_len = np.zeros(100)

    for i in range(100):

        # Generates random list
        rand_happy = np.random.randint(-10, high=10, size=100)
        (val, l, r) = happiest_meal(rand_happy, 0, len(rand_happy) - 1)

        # Stores max value and length
        max_happy[i] = val
        sublist_len[i] = (r-l) + 1
    return np.mean(max_happy), np.mean(sublist_len)

def mean_happy_prob():
    '''
    Creates lists with 0.7 probability of mean=6 and stdev=1 and 0.3 probability of mean=-7 and stdev=0.5
    and runs find_happiest_meal.
    Returns mean of max and lengths of sublists.
    '''
    max_happy = np.zeros(100)
    sublist_len = np.zeros(100)

    for i in range(100):

        food_list = np.zeros(100)
        rand = np.random.sample(100)

        #Generates list with "probability"
        for j in range(len(food_list)):

            if rand[j] > 0.3:
                food_list[j] = np.random.normal(loc=6, scale=1)
            else:
                food_list[j] = np.random.normal(loc=-7, scale=0.5)

        # Finds largest subarray sum
        (val, l, r) = happiest_meal(food_list, 0, len(food_list) - 1)

        #Stores max values and lengths
        max_happy[i] = val
        sublist_len[i] = (r-l) + 1

    # Return the mean
    return np.mean(max_happy), np.mean(sublist_len)

if __name__ == "__main__":

    # Print output for Question 3
    # On average, the max sum is about 50 and the length is around 26.
    print(mean_happy_uniform())

    #Print output for Question 4
    # On average, the max sum is about 220, and the length is around 90.
    print(mean_happy_prob())
