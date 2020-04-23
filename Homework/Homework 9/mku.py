'''
DSA Homework 9

Wildcard Matching Pattern Implementation
'''

def match_wildcard(s1, s2):
    '''
    Given two strings s1 and s2, returns if s2 can be made
    to look like s1 given a number of substitutions where
    there are * in s2.

    This algorithm uses a DP, bottom up approach.

    Returns T/F whether s2 can be turned into s1.

    m[i,j] returns whether the substring s2[0:j] can be turned into s1[0:i].
    This indexing allows room for the empty string base cases.
    '''

    x = len(s1)
    y = len(s2)
    m = [[0 for m in range(y+1)] for n in range(x+1)]
    # Base cases initialization
    # Empty string is equal to empty string
    m[0][0] = True
    for i in range(1, x+1, 1):
        # Empty s2 and nonempty s1 always returns False
        m[i][0] = False
    for j in range(1,y+1, 1):
        if s2[j-1] == "*":
            # If there are only * in s2, return True
            sub_val = m[0][j-1]
            m[0][j] = sub_val
        else:
            m[0][j] = False
    # Implement general value function
    for i in range (1, x+1):
        for j in range(1, y+1):
            # Accounts for all three scenarios of * presence in s2
            if s2[j-1] == "*":
                m[i][j] = m[i][j-1] or m[i-1][j] or m[i-1][j-1]
            # If the characters match, check if their substrings match
            elif s1[i-1] == s2[j-1]:
                m[i][j] = m[i-1][j-1]
            else:
                m[i][j] = False

    return m[x][y]

def test_wildcard():
    '''
    Tests the match_wildcard() function for the following cases:
    1. s1 == s2
    2. s1 is an empty string, s2 is nonempty
    3. s2 is an empty string, s1 is nonempty
    4. s2 can be recreated to be s1
    5. s2 cannot be recreated to be s1
    6. s2 has an * at the beginning and end
    '''
    s1 = ["bubbletea", "", "milkshake","xiaolongbao", "sushi", "steak", "iedcba"]
    s2 = ["bubbletea", "soup","", "x*l*bao*", "s*is", "**e**", "kji*cba"]
    output = [True, False, False, True, False, True, False]
    for i in range(len(s1)):
        assert match_wildcard(s1[i], s2[i]) == output[i]
