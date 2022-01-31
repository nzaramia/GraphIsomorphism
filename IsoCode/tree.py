import graph   
import sys
import time


class Node:
   def __init__(self,key):
     __slots__ = ['id']
     self.id = key     
   
   def setId(self,id):
     self.id = id
   
   def addNeighbor(self,nbr,weight=0):
     self.connectedTo[nbr] = weight

   def __str__(self):
     return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

   def getConnections(self):
     return self.connectedTo.keys()

   def getId(self):
     return self.id

   def getWeight(self,nbr):
     return self.connectedTo[nbr]


class Tree(graph.Graph):   
   
   def __init__(self):
      graph.Graph.__init__(self)
      self.vertListLevelOrder = []
      self.completeSubtreeListLevelOrder = []

   def addVertex(self,key):
     self.numVertices = self.numVertices + 1
     newVertex = Node(key)
     self.vertList[key] = newVertex
     self.vertListLevelOrder.append(newVertex)     
     return newVertex
     
   def addChild(self,f,t,weight=0):
     if f not in self.vertList:
         nv = self.addVertex(f)
     if t not in self.vertList:
         nv = self.addVertex(t)
     self.vertList[f].addNeighbor(self.vertList[t], weight)
     
      
