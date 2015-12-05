import random
import time
import networkx as nx
import ast
from mpi4py import MPI

#init stuff
filename = 'hamExample.txt'
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
    global busy_threads
    global done
    neighbours = list(nx.all_neighbors(G, node))
    
    if current_path == None:
        current_path = []
    
    visited.add(node)
    current_path.append(node) 

    #to count how many neighbours have been passed off to other processes.
    #this is used so that the root node can keep exploring the graph itself
    #and continue passing off branches to other processes until it runs out
    #of processes
    neighbour_iterator = 0

    print "Root sees visited as", visited
    print "Root sees current path as", current_path

    for n in neighbours:
        if n not in visited:
            if (busy_threads < size - 1) and neighbour_iterator < len(neighbours):
                busy_threads += 1
                # print "Sending job to thread", busy_threads
                comm.send(current_path, dest=busy_threads, tag=2)
                comm.send(n, dest=busy_threads, tag=3)
                neighbour_iterator += 1
            elif (check_neighbours(n, current_path)): #if there's no more branches or threads to distribute...do it yourself
                done = True
                comm.barrier()
                comm.bcast(done, root=rank)
                return True

    if len(current_path) == nx.number_of_nodes(G) and original_node in neighbours:
        comm.barrier()
        comm.bcast(done, root=rank)
        return True

    current_path.remove(node)
    visited.remove(node) #backtracking
    comm.barrier()
    if done:
        Finalize()
    return False

def child_explore(node, current_path):
    global done

    neighbours = list(nx.all_neighbors(G, node))
    print "Child starting node", node
    
    current_path.append(node)
    for node in current_path:
        visited.add(node) #this will include the current node since it just got appended

    print "Child", rank, "is seeing visited as", visited
    print "Child", rank, "is seeing current path as", current_path
    for n in neighbours:
        if n not in visited:
            if (child_explore(n, current_path)):
                done = True
                comm.barrier()
                comm.bcast(done, root=rank)
                return True
    if len(current_path) == nx.number_of_nodes(G) and original_node in neighbours:
        comm.barrier()
        comm.bcast(done, root=rank)
        return True

    current_path.remove(node)
    visited.remove(node) #backtracking
    comm.barrier()
    if done:
        Finalize()
    return False

def main():
    if rank == 0:
        build_graph()
        for i in range(1, comm.Get_size()):
            comm.send(G.nodes(), dest=i, tag=0)
            comm.send(G.edges(), dest=i, tag=1)
        if check_neighbours(original_node):
            print "Root returns true!"
            return True
    else:
        G.add_nodes_from(comm.recv(source=0, tag=0))
        G.add_edges_from(comm.recv(source=0, tag=1))
        current_path = comm.recv(source=0, tag=2) #blocking wait
        starting_node = comm.recv(source=0, tag=3) #blocking wait
        if child_explore(starting_node, current_path):
            print "Child", rank, "returns true!"
            return True

timeStart = time.time()
main()
timeEnd = time.time() - timeStart
print timeEnd
comm.Abort()

# build_graph()
# original_node = 1
# print check_neighbours(original_node)
# with open("results.txt", 'a') as myfile:
# 	myfile.write(filename + ' ' + str(timeEnd) + '\n')
