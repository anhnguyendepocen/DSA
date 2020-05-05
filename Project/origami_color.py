"""
Final Project script for Data Structures and Algorithms.

Author: Megan Ku
"""
import random
import networkx as nx
from graphs import I

# This code is meant for polyhedra that are tricolored.
# Any change in that will result in a need to change the rest of the code
COLORS = ("yellow", "green", "blue")

def color_graph_greedy(G):
    """
    Returns a greedy coloring solution for a given graph, with the added parameter
    that the distribution of colors should be as equal as possible.
    G = graph to be colored
    returns a hashmap of the number node and its color, a hashmap of the color distribution totals, and the node number of any violations.
    """

    visited = {}
    # set color count to zero
    color_count = {}
    # dict to check color of neighbors
    color_neighbors = {}
    for color in COLORS:
        color_count[color] = 0
        color_neighbors[color] = False
    node_color = {}
    # mark all nodes as unvisited
    for node in G.nodes():
        visited[node] = False
        node_color[node] = None

    violations = []
    # Start at a random node
    start_node = random.randrange(0,len(G.nodes()))

    # Create BFS queue
    search = [start_node]

    # Search loop
    while search != []:
        # dequeue current node
        curr_node = search.pop(0)
        # Avoid repeats by checking if the node has been visited
        if not visited[curr_node]:
            # mark node as visited
            visited[curr_node] = True
            for neighbor in G.neighbors(curr_node):
                # Check neighbors - if they've been visited, take note of their color
                # Otherwise, add them to the queue.
                if visited[neighbor]:
                    color_neighbors[node_color[neighbor]] = True
                else:
                    search.append(neighbor)

            smallest_color = None
            smallest_count = 100000000

            # Make curr_node the color of the least-used valid color
            for color in color_neighbors:
                if not color_neighbors[color]:
                    if color_count[color] < smallest_count:
                        smallest_color = color
                        smallest_count = color_count[color]
            # If no color is valid, we have a color violation. Set this node to the first color.
            if smallest_color == None:
                node_color[curr_node] = COLORS[0]
                violations.append(curr_node)
            else:
                node_color[curr_node] = smallest_color

            # Update tallies of colors
            color_count[node_color[curr_node]] += 1
            # Reset neighbor colors
            for color in COLORS:
                color_neighbors[color] = False

    return node_color, color_count, violations

def colors_equal(color_count):
    return (color_count[COLORS[0]] == color_count[COLORS[1]] == color_count[COLORS[2]])

def color_local_search(G, node_color, color_count, violations):
    """
    Local search algorithm to improve solutions given by greedy algorithm.
    """
    # Change this number to affect how many times the improvement process happens
    # If this doesn't exist the code can get stuck in an infinite loop
    upper_limit = 100

    num_runs = 0
    while violations != []:
        num_runs += 1
        # Arbitrary iteration break
        if num_runs > upper_limit and colors_equal(color_count) or num_runs > 2*upper_limit:
            break

        # Reset neighboring colors
        color_neighbors = {COLORS[0]:[], COLORS[1]:[], COLORS[2]:[]}

        # If solution fits constraints, stop
        node = violations.pop()
        curr_color = node_color[node]

        # Count the number of different colored neighbors
        for neighbor in G.neighbors(node):
            color_neighbors[node_color[neighbor]].append(neighbor)

        # Change the current node color to the one that gives the least new number of violations
        if curr_color == COLORS[0]:
            if len(color_neighbors[COLORS[1]]) <= len(color_neighbors[COLORS[2]]):
                best_color = COLORS[1]
            else:
                best_color = COLORS[2]
        elif curr_color == COLORS[1]:
            if len(color_neighbors[COLORS[0]]) <= len(color_neighbors[COLORS[2]]):
                best_color = COLORS[0]
            else:
                best_color = COLORS[2]
        else:
            if len(color_neighbors[COLORS[0]]) <= len(color_neighbors[COLORS[1]]):
                best_color = COLORS[0]
            else:
                best_color = COLORS[1]

        # Update node counts and colors
        node_color[node] = best_color
        violations += color_neighbors[best_color]
        color_count[curr_color] -= 1
        color_count[best_color] += 1

    return node_color, color_count, violations


def color_combined_search(G):
    # Number of times greedy algorithm is run
    num_greedy = len(G.nodes()) // len(COLORS)
    # Initialize violations list to keep track of largest existing list of violations
    violations = G.nodes()
    best_node_color = {}
    best_color_count = {}

    # Runs greedy search several times and finds best one
    for run in range(num_greedy):
        node_color_run, color_count_run, violations_run = color_graph_greedy(G)
        if len(violations) >= len(violations_run):
            best_node_color = node_color_run
            best_color_count = color_count_run
            violations = violations_run
        # If the greedy algorithm finds a solution, return it
        if colors_equal(best_color_count) and violations == []:
            print("Greedy find")
            return node_color_run, color_count_run, violations_run


    # Perform local search on best greedy output
    return color_local_search(G, best_node_color, best_color_count, violations)


def test_color_algs(G):

    pass


if __name__ == "__main__":

    # node_color, color_count, violations = color_graph_greedy(I)
    # node_color, color_count, violations = color_local_search(I, node_color, color_count, violations)
    node_color, color_count, violations = color_combined_search(I)
    print(node_color, color_count, violations)
