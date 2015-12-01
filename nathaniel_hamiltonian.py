import networkx as nx
import ast

G = nx.Graph()
visited = set()
original_node = None

def build_graph():
    with open('graph.txt', 'r') as f:
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
    
    visited.add(node)
    current_path.append(node) 
    
    for n in neighbours:
        if n not in visited:
            if (check_neighbours(n, current_path)):
                return True
        
        # else:
            # if len(current_path) == nx.number_of_nodes(G) and original_node in neighbours:
                # return True

    if len(current_path) == nx.number_of_nodes(G) and original_node in neighbours:
        return True

    visited.remove(node)
    return False

def main():
    build_graph()
    print "What are we doing"

build_graph()
original_node = 1
print check_neighbours(original_node)
