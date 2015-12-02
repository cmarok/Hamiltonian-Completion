import time
import networkx as nx
import ast
G = nx.Graph()

def build_graph():
    f = open('10_graph_18.txt', 'r')
    nodes_line = f.readline()
    edges_line = f.readline()
    nodes = [int(n) for n in nodes_line.split()]
    edges = ast.literal_eval(edges_line)
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

def find_all_paths(G, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return[]
    paths = []
    for node in nx.all_neighbors(G, [start]):
        if node not in path:
            newpaths = find_all_paths(G, node, end, path)
            for newpath in newpaths:
                if(len(newpath) == nx.number_of_nodes(G):
                   paths.append(newpath)
    return paths
build_graph()
find_all_paths(G, 
