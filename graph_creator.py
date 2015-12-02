import sys
import random
import string


def makeEdges(currentEdge, totalNodes):
	numEdges = random.randint(currentEdge + 1, totalNodes)
	edges = random.sample(range(currentEdge + 1, totalNodes), numEdges)
	outString = ''
	for edge in edges:
		outString += '[' + str(currentEdge) + ',' + str(edge) + '], '
	return outString
		

def write():
    	print('Creating new text file') 

    	name = raw_input('Enter name of text file: ')+'.txt'  # Name of text file coerced with +.txt

    	try:
        	file = open(name,'w')   # Trying to create a new file or open one
		numNodes = raw_input('Enter number of nodes to create: ')
		finalString = '('
		for i in xrange(1, numNodes):
			finalString += makeEdges(i, numNodes)
		
		finalString = finalString[:-2]
		finalString += ')'
		print '%s' % finalString
	        file.close()

	except:
        	print('Something went wrong! Can\'t tell what?')
	        sys.exit(0) # quit Python

write()
	

	
