import numpy as np
import time

def read_tsp(filename):
    '''
    Reads a TSPLIB instance given by filename and returns the corresponding
    distance matrix C. Assumes that the edge weights are given in lower
    diagonal row form.
    '''
    f = open(filename,'r')

    n, C = 0, None
    i, j = -1, 0

    for line in f:
        words = line.split()
        if words[0] == 'DIMENSION:':
            n = int(words[1])
            C = np.zeros(shape=(n,n))
        elif words[0] == 'EDGE_WEIGHT_SECTION':
            i = 0 # Start indexing of edges
        elif i >= 0:
            for k in range(len(words)):
                if words[k] == 'EOF':
                    break
                elif words[k] == '0':
                    i += 1 # Continue to next row of the matrix
                    j = 0
                else:
                    C[i,j] = int(words[k])
                    C[j,i] = int(words[k])
                    j += 1
    return C


def greedy_traveling_salesman(C):
    '''
    Greedy traveling salesman solution that checks the closest node to the
    current node in the path.
    Returns distance of constructed path.
    '''
    # Initialize distance variable and hash map to keep track of visited cities
    dist = 0
    visited = {}
    path = []

    # Initialize all cities as unvisited
    for i in range(len(C)+1):
        visited[i+1] = False

    start = 1
    curr_loc = start
    path.append(start)
    visited[curr_loc] = True
    # Counter to keep track of cities traveled
    total_cities_traveled = 1

    while total_cities_traveled < len(C):
        min_dist = 1000000000
        for city in range(1, len(C)+1):
            if not visited[city]:
                curr_commute = C[curr_loc-1][city-1]
                if curr_commute < min_dist:
                    min_dist = curr_commute
                    closest_city = city

        dist += min_dist
        visited[closest_city] = True
        path.append(closest_city)
        curr_loc = closest_city
        total_cities_traveled += 1

    dist += C[curr_loc-1][start-1]
    return dist, path

def search_traveling_salesman(dist, path, C):
    '''
    A local search algorithm for the traveling salesman problem.
    '''
    idx = 0
    moving_node = path[idx]

    # Calculate the "value" of that node's existence in that location
    # Add the cost of each edge connected to those nodes and subtract the
    # cost of those nodes being directly connected
    if idx == 0:
        left_node = len(path)
        right_node = path[idx+1]
    elif idx == len(path)-1:
        left_node = path[idx-1]
        right_node = path[0]
    else:
        left_node = path[idx-1]
        right_node = path[idx+1]

    dist -= (C[moving_node-1][left_node-1] + C[moving_node-1][right_node-1])
    dist += C[left_node-1][right_node-1]

    path.remove(moving_node)
    cheap_cost = 100000000

    # Check each possible insertion for lowest cost
    for i in range(1, len(path)+1):
        if i == len(path):
            j = path[0]
        else:
            j = path[i+1]
        insert_cost = C[moving_node-1][i-1] + C[moving_node-1][j-1]
        insert_cost -= C[i-1][j-1]
        if insert_cost < cheap_cost:
            cheap_cost = insert_cost
            best_node = i

    # insert at cheapest location
    dist += cheap_cost
    path.insert(i-1, moving_node)
    return dist, path

#
C = read_tsp('gr17.tsp')
dist, path = greedy_traveling_salesman(C)
print(path) #optimal = 2085
dist2, path2 = search_traveling_salesman(dist, path, C)
print(path2)
print(dist, dist2)
# C = read_tsp('gr21.tsp')
# print(greedy_traveling_salesman(C)) #optimal = 2707
# C = read_tsp('gr24.tsp')
# print(greedy_traveling_salesman(C)) #optimal = 1272
# C = read_tsp('gr48.tsp')
# print(greedy_traveling_salesman(C)) #optimal = 5046
