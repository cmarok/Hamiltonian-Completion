import random
import time
import networkx as nx
import ast
from mpi4py import MPI

#init stuff
filename = sys.argv[1] +'_graph_' + sys.argv[2] + '.txt'
G = nx.Graph()
visited = set()
original_node = 1
done = False
busy_threads = 0
#end of init stuff

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

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
    if rank < nx.number_of_nodes(G):
        starting_node = rank
        timeStart = time.time()
        starting_node = rank + 1
        if check_neighbours(starting_node, None):
            print "Graph is hamiltonian! (process", rank, ")"
        else:
            print "Graph is not hamiltonian (process", rank, ")"
        timeEnd = time.time() - timeStart
        print timeEnd
        comm.Abort()

build_graph()

main()


