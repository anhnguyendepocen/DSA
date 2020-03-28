'''
Megan Ku
DSA Homework 7 (Code)

Questions 2-3: So many graphs
'''

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def find_num_components(G):
    """
    Finds the number of components in a given graph with
    vertices V and edges E.

    Returns the number of components in a graph (int).
    """
    visited = {}
    components = 0

    #Initialize hashmap to keep track of visited nodes
    for v in G.nodes():
        visited[v] = False

    for node in visited:
        #Every time we have to initialize a new DFS, we have identified
        #that there is a new component
        if not visited[node]:
            components += 1
            visited[node] = True
            visited_stack = [node]

            # While all nodes in this component haven't been visited
            while visited_stack != []:
                curr_node = visited_stack.pop()
                #DFS
                for neighbor in G.neighbors(curr_node):
                    if visited[neighbor] == False:
                        visited[neighbor] = True
                        visited_stack.append(neighbor)
    return components

def test_find_num_components():
    """
    Tests find_num_components for the following cases:
    1. One component
    2. Multiple components
    3. Zero edges (num of components = num nodes)
    """

    G = nx.Graph()
    G.add_node(1)
    G.add_node(2)
    G.add_edge(1,2)
    assert find_num_components(G) == 1

    G.add_node(3)
    G.add_node(4)
    G.add_edge(3,4)
    assert find_num_components(G) == 2

    G.remove_edge(3,4)
    G.remove_edge(1,2)
    assert find_num_components(G) == 4

#-------------------------------------------------------------------------------

def rand_bi_graphs(n, p):
    '''
    Generates 10 graphs and checks if they're fully connected.
    n = number of nodes
    p = probability
    '''
    for i in range(10):
        G = make_graph(n, p)
        num = find_num_components(G)
        #Check if connected
        if num > 1:
            return False
    return True

def make_graph(n, p):
    '''
    Builds a graph with n nodes and with probability p that there is an edge
    between two nodes.
    '''
    G = nx.Graph()
    #Adds n nodes
    for j in range(n):
        G.add_node(j)
    node_list = list(G.nodes())
    #Adds edges if probability is satisfied
    for n in range(len(node_list)):
        for m in range(n+1, len(node_list)):
            s = np.random.sample()
            if s <= p:
                G.add_edge(node_list[n], node_list[m])
    return G

def find_p():
    '''
    Finds lowest probability that graph is fully connected.
    '''
    prob = []
    for m in range(5,51):
        p_0 = 0
        connected = False
        while not connected:
            # Increase the probability until all graphs are connected
            p_0 += 0.01
            connected = rand_bi_graphs(m, p_0)
        prob.append(p_0)

    # Plots results
    plt.plot(range(5,51), prob, '.')
    plt.xlabel("Input Size (n)")
    plt.ylabel("Probability for Connected Graph")
    plt.title("Minimum Probability of Edge Connection for Connected Graph")
    fig = plt.gcf()
    fig.savefig("connect.png")
    plt.show()

    return prob

n = find_p()
print(n)
