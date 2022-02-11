import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QApplication, QPushButton
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore

import random

#NEXT TODO:
#Setup the UI
#TODO: random will have to be seeded so I could reproduce issues.
#Generate isomorphisms

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
      Degree = 9
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
      
      vertList = []
      
      #Add the vertices
      for v in range(numNodes):
         print("v ", v)
         vertList.append(vertexDesc(v))

      #Add the edges by adding nodes to the lists in vertDesc objects in the vertlist list
      
      generatedGraph = []
      graphEdgeList = []
      
      
      while len(vertList)>0:
                  
         #if there are more vertices left in the list than the degree of this vertex + 1 and we haven't reached the degree
         while (len(vertList[0].vertexNeighbors) < requestedDegree):
            #get a random vertex index
            #add an edge between this and other vertex if no edge exists between them.  
            #if yes, choose another until we find one.            
            while True:
               vertexIndex = random.randint(1, len(vertList)-1)
               if not vertList[vertexIndex].vertexId in vertList[0].vertexNeighbors:
                  vertList[0].vertexNeighbors.append(vertList[vertexIndex].vertexId)
                  vertList[vertexIndex].vertexNeighbors.append(vertList[0].vertexId)

                  graphEdgeList.append(edgeDesc(vertList[0].vertexId, vertList[vertexIndex].vertexId))

                  #REMOVE THE NEIGHBOR FROM THE LIST IF REACHED DEGREE AND PUT IN GRAPH.
                  if len(vertList[vertexIndex].vertexNeighbors) == requestedDegree:
                     generatedGraph.append(vertList[vertexIndex])
                     vertList.pop(vertexIndex)
                  break

         #Remove vertex 0 from the list:
         #if not reached the max degree and degree is max relative to remaining list length then
         #randomly choose if connected to some random vertex in the graph.
         if len(vertList[0].vertexNeighbors) < requestedDegree:
            if random.randint(0, 1) == 0:
               #select random vertex in the other graph then add this!!!!
               graphVertexIndex = random.randint(0, len(generatedGraph)-1)
               vertList[0].vertexNeighbors.append(generatedGraph[graphVertexIndex].vertexId)
               generatedGraph[graphVertexIndex].vertexNeighbors.append(vertList[0].vertexId)

               graphEdgeList.append(edgeDesc(vertList[0].vertexId, generatedGraph[graphVertexIndex].vertexId))

         generatedGraph.append(vertList[0])      
         vertList.pop(0)
                                         
      #write the graph into a file
      graphfile  = open(fileName, "w") 
      
      graphfile.write("p edge " + str(numNodes) + " " + str(len(graphEdgeList)) + "\n")

      for e in graphEdgeList:
         graphfile.write("e " + str(e.vertexIdStart) + ' ' + str(e.vertexIdEnd) + "\n")
      
      graphfile.close()


def main():

    app = QApplication(sys.argv)
    
    ex = MainWindow()
    #w.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()