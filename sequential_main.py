import networkx as nx
import ast

G = nx.Graph()
visited = set()
original_node = None

def build_graph():
	f = open('graph.txt', 'r')
	nodes_line = f.readline()
	edges_line = f.readline()
	nodes = [int(n) for n in nodes_line.split()]
	edges = ast.literal_eval(edges_line)
	G.add_nodes_from(nodes)
	G.add_edges_from(edges)

def check_neighbours(node, current_path):
	neighbours = nx.all_neighbors(G, node)
	visited.add(node)
	current_path.append(node)
	for n in neighbours:
		# print (original_node in neighbours)
		if n not in visited:
			print current_path
			print "Returning...something"
			return check_neighbours(n, current_path)
		elif (len(current_path) == nx.number_of_nodes(G)) and (original_node in neighbours):
			print "Returning true!"
			return True
	return False



def main():
	print "What are we doing"

build_graph()
print G.nodes()
print G.edges()
original_node = 4
print check_neighbours(original_node, [])
