import random
import time
import networkx as nx
import ast
import sys

filename = sys.argv[1] +'_graph_' + sys.argv[2] + '.txt'
G = nx.Graph()
visited = set()
original_node = None

def build_graph():
    with open(filename, 'r') as f:
        nodes_line = f.readline()
        edges_line = f.readline()
        nodes = [int(n) for n in nodes_line.split()]
        edges = ast.literal_eval(edges_line)
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

def check_neighbours(node, current_path=None):
    global visited
    neighbours = list(nx.all_neighbors(G, node))
    
    if current_path == None:
        current_path = []
    
    # print "Current path is", current_path
    visited.add(node)
    current_path.append(node) 
    

    for n in neighbours:
        if n not in visited:
            if (check_neighbours(n, current_path)):
                return True

    if len(current_path) == nx.number_of_nodes(G) and original_node in neighbours:
        return True

    current_path.remove(node)
    visited.remove(node)
    return False

def main():
    build_graph()
    print "What are we doing"

timeStart = time.time()
build_graph()
original_node = random.randint(1, nx.number_of_nodes(G))
print original_node
print check_neighbours(original_node)
timeEnd = time.time() - timeStart
print timeEnd
with open("results.txt", 'a') as myfile:
	myfile.write(filename + ' ' + str(timeEnd) + '\n')
