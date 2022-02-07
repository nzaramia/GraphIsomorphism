import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QApplication, QPushButton
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore

import random

#TODO: random will have to be seeded so I could reproduce issues.

class vertexDesc:
   def __init__(self, vertexId):
      self.vertexId = vertexId
      self.vertexNeighbors = []
   

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
      Degree = 4
      fileName = "NZ-1"
      self.generateGraph(fileName, numNodes, Degree)
      
   def generateGraph(self, fileName, numNodes, requestedDegree):

      #TODO: build the graph
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

      #START HERE: Add the edges by adding nodes to the lists in vertDesc objects in the vertlist list
      
      generatedGraph = []
      edgeCanBeAdded = true
      
      
      while edgeCanBeAdded and len(vertList)>0:
         
         numVertices = len(vertList)
         edgeCanBeAdded = False
         #if there are more vertices left in the list than the degree of this vertex + 1 and we haven't reached the degree
         while (len(vertList[0].vertexNeighbors)+1 < numVertices) and (len(vertList[0].vertexNeighbors) < requestedDegree):
            edgeCanBeAdded = True
            #get a random vertex index
            #add an edge between this and other vertex if no edge exists between them.  
            #if yes, choose another until we find one.            
            while True:
               vertexIndex = random.randint(1, len(vertList)-1)
               if not vertList[vertexIndex].vertexId in vertList[0].vertexNeighbors:
                  vertList[0].append(vertList[vertexIndex].vertexId)
                  #NEXT: REMOVE THE NEIGHBOR FROM THE LIST IF REACHED DEGREE AND PUT IN GRAPH.
                  break

         #NEXT: Remove vertex 0 from the list.  
         #if not reached the max degree and degree is max relative to remaining list length then
         #randomly choose if connected to some random vertex in the graph.
         #THEN put the vertex in the graph.
         
         #if nothing changed then
         if not edgeCanBeAdded:
            #for each remaining vertex
               #if degree is 0, connect to a random vertex in other list
               #otherwise, randomly choose to connect to a random vertex in the other tree
         
      
      #TODO: take the processed list 
      graphfile  = open(fileName, "w") 
      
      graphfile.write("p edge " + str(numNodes) + " " + "???\n")  #TODO I don't know the number of edges yet.

      #for e in range()   #need number of edges here
      graphfile.write("e 1 4\n")
      graphfile.write("e 1 5\n")     
      graphfile.write("e 2 3\n")
      graphfile.write("e 2 4\n")
      graphfile.write("e 3 5\n")      
      graphfile.write("e 4 5\n")
      
      graphfile.close()


def main():

    app = QApplication(sys.argv)
    
    ex = MainWindow()
    #w.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()