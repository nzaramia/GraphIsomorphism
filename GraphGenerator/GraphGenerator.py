import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QApplication, QPushButton
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QTextCursor, QPixmap, QFont
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, QApplication, QPushButton, QTabWidget, QVBoxLayout, QTextBrowser, QHBoxLayout, QSplitter, QFrame, QFileDialog, QFormLayout, QDateTimeEdit, QCheckBox, QGridLayout, QGroupBox)

import random
import time

#NEXT 
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
      palette = self.palette()
      palette.setColor(self.backgroundRole(), Qt.lightGray)

      self.vertical_box_layout = QVBoxLayout(self)

      self.tab_widget = QTabWidget()
      self.console_output_browser = QTextBrowser()
      

      self.top_frame = QFrame()
      layout = QVBoxLayout(self.top_frame)
      layout.addWidget(self.tab_widget)

      self.console_output_controls = QWidget()
      self.console_output_controls_layout = QHBoxLayout()
      self.console_status_text = QLabel("")
      self.console_status_text.setFont(QFont('Arial', 12))

      self.clear_console = QPushButton()
      self.clear_console.clicked.connect(self.clear_console_browser_text)
      self.clear_console.setText("Clear Text")

      self.console_output_controls_layout.addWidget(self.console_status_text)
      self.console_output_controls_layout.addWidget(self.clear_console)
      self.console_output_controls.setLayout(self.console_output_controls_layout)

      self.bottom_frame = QFrame()
      layout = QVBoxLayout(self.bottom_frame)
      layout.addWidget(self.console_output_browser)
      layout.addWidget(self.console_output_controls)

      self.top_frame.setFrameShape(QFrame.StyledPanel)
      self.bottom_frame.setFrameShape(QFrame.StyledPanel)

      self.SetupFirstTab()

      self.splitter = QSplitter(QtCore.Qt.Vertical)
      self.splitter.addWidget(self.top_frame)
      self.splitter.addWidget(self.bottom_frame)
      self.splitter.setSizes([100, 500])

      self.vertical_box_layout.addWidget(self.splitter)
      self.setLayout(self.vertical_box_layout)

      self.setWindowTitle("Graph Generator")
      self.setGeometry(100, 50, 800, 800)

      #self.resize(1200, 650)
      #self.move(80, 20)
      #self.setWindowTitle('Graph Generator')
                   
          
      #TODO the degree given by the user cannot be greater than #nodes-1
      #Also, minimum degree should be 1

   def SetupFirstTab(self):
      self.tab1 = QWidget()
      self.tab_widget.addTab(self.tab1, "Generate Graph")

      main_layout = QFormLayout()
      main_layout.setSpacing(20)
      main_layout.setContentsMargins(50, 50, 200, 200)

      self.numNodes = QLineEdit()
      self.averageDegree = QLineEdit()
      self.fileName = QLineEdit()

      self.fileName.setText("NZ-1")
      
      main_layout.addRow("Number of Nodes", self.numNodes)
      main_layout.addRow("Average Degree", self.averageDegree)
      main_layout.addRow("File name", self.fileName)      

      self.generate_graph_button = QPushButton()
      self.generate_graph_button.clicked.connect(self.generateGraph)
      self.generate_graph_button.setText("Generate Graph")

      self.generate_graph_button.setFixedSize(100, 40)
      main_layout.addWidget(self.generate_graph_button)

      self.tab1.setLayout(main_layout)


   @pyqtSlot()
   def clear_console_browser_text(self):
      self.console_output_browser.setText("")
      
   def generateGraph(self):
      self.console_output_browser.clear()
      
      try:
         requestedDegree = int(self.averageDegree.text())
         numNodes = int(self.numNodes.text())
      except:
         self.console_output_browser.append("You must enter a number.")
         return
      
      fileName = self.fileName.text()   

      self.console_output_browser.clear()
      self.console_output_browser.append("Generating graph, please wait...")
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
         #print("v ", v)
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
      self.console_output_browser.append("Graph generation complete.")

      #Calcualte the average degree
      edgeCount = 0
      for v in generatedGraph:
         edgeCount += len(v.vertexNeighbors)
      avgDeg = edgeCount / numNodes

      self.console_output_browser.append("Average degree: " + str(avgDeg))

      generateIsomorphism(generatedGraph, graphEdgeList, fileName)

def generateIsomorphism(generatedGraph, graphEdgeList, fileName):
   
   numNodes = len(generatedGraph)
   #create a list of node indices and shuffle them
   nodeList = []

   for i in range(numNodes):
      nodeList.append(i)

   random.shuffle(nodeList)
   #write the graph into a file
   graphfile  = open(fileName+"_iso", "w") 
      
   graphfile.write("p edge " + str(numNodes) + " " + str(len(graphEdgeList)) + "\n")

   for e in graphEdgeList:
      graphfile.write("e " + str(nodeList[e.vertexIdStart]+1) + ' ' + str(nodeList[e.vertexIdEnd]+1) + "\n")
      
   graphfile.close()



def main():

    app = QApplication(sys.argv)
    
    ex = MainWindow()
    ex.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()