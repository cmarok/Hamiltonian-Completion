import networkx as nx
import ast

G = nx.Graph()


def build_graph():
	f = open('graph.txt', 'r')
	nodes_line = f.readline()
	edges_line = f.readline()
	nodes = [int(n) for n in nodes_line.split()]
	edges = ast.literal_eval(edges_line)
	G.add_nodes_from(nodes)
	G.add_edges_from(edges)

def main():
	print "What are we doing"

build_graph()
print G.nodes()
print G.edges()