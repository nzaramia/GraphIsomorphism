import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QApplication, QPushButton
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore

import random
import time

#NEXT TODO:
#Setup the UI
#Generate isomorphisms
#Calculate the average degrees of the vertices
#Test with a large number of vertices, generating and checking for isomorphisms.

class vertexDesc:
   def __init__(self, vertexId):
      self.vertexId = vertexId
      self.vertexNeighbors = []

class edgeDesc:
   def __init__(self, vertexIdStart, vertexIdEnd):
      self.vertexIdStart = vertexIdStart
      self.vertexIdEnd = vertexIdEnd

   

class MainWindow(QWidget):
   def __init__(self):
       super().__init__()
       self.setupUI()

   def setupUI(self):
      self.resize(1200, 650)
      self.move(80, 20)
      self.setWindowTitle('Graph Generator')
                   
      self.show()
      
      #TODO the degree given by the user cannot be greater than #nodes-1
      #Alse, minimum degree should be 1

      numNodes = 10
      Degree = 3
      fileName = "NZ-1"
      self.generateGraph(fileName, numNodes, Degree)
      
   def generateGraph(self, fileName, numNodes, requestedDegree):

      # build the graph
      # List of (node index, adjacency list) 
      # Add the node indices in the list
      # Pick two nodes randomly from the list.
      # Connect them
      # If their degree >= average degree, remove it and put it in a processed list.
      # If there are nodes left at the end, connect them to a random node in the processed list.
      
      #Seed random and write it to a file.
      seed = time.time()
      #seed = 1644977001.0896435
      random.seed(seed)
      f = open("seed.txt", "w")
      f.write(str(seed))
      f.close()
      
      vertList = []
      
      #Add the vertices
      for v in range(numNodes):
         print("v ", v)
         vertList.append(vertexDesc(v))

      #Add the edges by adding nodes to the lists in vertDesc objects in the vertlist list
      
      generatedGraph = []
      graphEdgeList = []
      
      maxNeighborFindTries = 0
      numVertices = len(vertList)
      
      while numVertices>0:
         
         maxNeighborFindTries = 2*numVertices
                  
         #if there are more vertices left in the list than the degree of this vertex + 1 and we haven't reached the degree
         while (len(vertList[0].vertexNeighbors) < requestedDegree):

            numTries = 0

            #get a random vertex index
            #add an edge between this and other vertex if no edge exists between them.  
            #if yes, choose another until we find one.            
            while numTries<maxNeighborFindTries and numVertices>1:
               numTries += 1
               vertexIndex = random.randint(1, len(vertList)-1)
               if not vertList[vertexIndex].vertexId in vertList[0].vertexNeighbors:
                  vertList[0].vertexNeighbors.append(vertList[vertexIndex].vertexId)
                  vertList[vertexIndex].vertexNeighbors.append(vertList[0].vertexId)

                  graphEdgeList.append(edgeDesc(vertList[0].vertexId, vertList[vertexIndex].vertexId))

                  #REMOVE THE NEIGHBOR FROM THE LIST IF REACHED DEGREE AND PUT IN GRAPH.
                  if len(vertList[vertexIndex].vertexNeighbors) == requestedDegree:
                     generatedGraph.append(vertList[vertexIndex])
                     vertList.pop(vertexIndex)
                     numVertices -= 1
                  break

            if numTries==maxNeighborFindTries or numVertices<=1:
               break

         #Remove vertex 0 from the list:
         #if not reached the max degree and degree is max relative to remaining list length then
         #randomly choose if connected to some random vertex in the graph.
         if len(vertList[0].vertexNeighbors) < requestedDegree and len(generatedGraph)>0:
            if random.randint(0, 1) == 0:
               #select random vertex in the other graph then add this!!!!
               graphVertexIndex = random.randint(0, len(generatedGraph)-1)
               vertList[0].vertexNeighbors.append(generatedGraph[graphVertexIndex].vertexId)
               generatedGraph[graphVertexIndex].vertexNeighbors.append(vertList[0].vertexId)

               graphEdgeList.append(edgeDesc(vertList[0].vertexId, generatedGraph[graphVertexIndex].vertexId))

         generatedGraph.append(vertList[0])      
         vertList.pop(0)
         numVertices -= 1
                                         
      #write the graph into a file
      graphfile  = open(fileName, "w") 
      
      graphfile.write("p edge " + str(numNodes) + " " + str(len(graphEdgeList)) + "\n")

      for e in graphEdgeList:
         graphfile.write("e " + str(e.vertexIdStart+1) + ' ' + str(e.vertexIdEnd+1) + "\n")
      
      graphfile.close()


def main():

    app = QApplication(sys.argv)
    
    ex = MainWindow()
    #w.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()