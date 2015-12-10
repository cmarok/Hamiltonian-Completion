import sys
import random
import string


def write():
     print('Creating new text file')

     name = str(sys.argv[1]) + '_graph_' + str(sys.argv[2]) +'.txt'  # Name of text file coerced with +.txt
     try:
          file = open(name,'w')   # Trying to create a new file or open one
          numNodes = int(sys.argv[1])
          numEdges = int(sys.argv[2])
          
          lineOne = ''
          for i in range(1, numNodes+1):
               lineOne += str(i) + ' ' 
          lineOne += '\n'
          file.write(lineOne)
          
          #make connections
          possible = []
          for i in range(1, numNodes+1):
               for j in range(1, numNodes+1):
                    if j > i:
                         possible.append([i,j])

          edges = random.sample(possible, numEdges)
          outString = '('
          for edge in edges:
               outString += str(edge) + ', '
          finalString = outString
          
          finalString = finalString[:-2]
          finalString += ')'
          file.write(finalString)
          
          file.close()

     except:
          print('Something went wrong! Can\'t tell what?')
          sys.exit(0) # quit Python

write()
	

	
