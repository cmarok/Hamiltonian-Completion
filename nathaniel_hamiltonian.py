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
    # Convert neighbours to a list so that it 
    # is statically evaluated instead of lazily,
    # this way the original_node won't be thrown away.
    # Downside is that if you're dealing with large
    # graphs, you need to actually allocate this much
    # memory instead of being able to just look at
    # one value at a time.
    
    if current_path == None:
        current_path = []
    
    visited.add(node)
    current_path.append(node) 
    
    for n in neighbours:
        if n not in visited:
            return check_neighbours(n, current_path)
        
        else:
            if len(current_path) == nx.number_of_nodes(G) and original_node in neighbours:
            # Here's your problem. The "original_node in neighbours".
            # neighbours is a generator, meaning it is lazily evaluated, and throws
            # away its value as soon as you look at it to save memory.
            # So, depending on which order you check your neighbours in,
            # it's entirely possible that the original_node WON'T be in
            # neighbours anymore.
                return True
    
    return False

def main():
    print "What are we doing"

build_graph()
original_node = 1
print check_neighbours(original_node)
