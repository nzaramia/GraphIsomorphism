import tree
import sys
import time


class IsoNode(tree.Node):
   def __init__(self,key):
     self.index = 0 
     self.connectedTo = {}
     self.sortedChildrenKeys = []
     
     self.cycles = []
     self.descriptor = "" 
     self.descriptorWithoutOrder = ""
     self.parent = []
     
     self.treeLevel = 0
     
     self.subTree = []
     self.subTreeUsageCount = 0
     
     self.treeHeight = 0
     
     self.subtreeRank = -1
     
     self.MySubTreeIsACandidate = False    
     self.SubtreeLineagePotentialMapping = {}
     
     self.SubtreeLineageMappingIsComplete = False
     
     self.explored = False
     
       

class IsoTree(tree.Tree):   
   
   def __init__(self):
      tree.Tree.__init__(self)
      self.vertListLevelOrder = []
      self.completeSubtreeListLevelOrder = []
      self.id_Order = {}
      
   def addVertex(self,key):
     self.numVertices = self.numVertices + 1
     newVertex = IsoNode(key)
     self.vertList[key] = newVertex
     self.vertListLevelOrder.append(newVertex)    
     return newVertex
          
   def childCmp_descriptor(self, a):
      return self.vertList[a.index].descriptor
      
   def childCmp_ID(self, a):
      return self.vertList[a.index].id      
      

   def SortChildren(self, nodeKey):
      children = self.vertList[nodeKey].getConnections()
            
      for childKey in children:
         self.vertList[nodeKey].sortedChildrenKeys.append(childKey)

      #This gives it a deterministic behaviour because order in dictionary is not determ. in Python.
      self.vertList[nodeKey].sortedChildrenKeys.sort(key=self.childCmp_ID)
               
      self.vertList[nodeKey].sortedChildrenKeys.sort(key=self.childCmp_descriptor, reverse=True)
      

#################################

   def show_node_size(self):
      print("Node size in bytes: ", sys.getsizeof(IsoNode))

#################################

   def resetSorting(self):
      numVertices = len(self.vertList)
            
      for i in range(numVertices): 
         self.vertList[i].sortedChildrenKeys = []

#################################

   def ResetMappingInfo(self):
      numVertices = len(self.vertList)  
   
      for i in range(numVertices): 
        self.vertList[i].MySubTreeIsACandidate = False    
        self.vertList[i].SubtreeLineagePotentialMapping = {}     
        self.vertList[i].SubtreeLineageMappingIsComplete = False     
        self.vertList[i].explored = False     
     
   #brings all subtrees to the left of the tree
   def NormalizeTree(self):
       self.ResetMappingInfo()
       explored = []

       numVertices = len(self.vertList)  
       
       # keep track of nodes to be checked
       stack = [self.vertList[0]]
             
       PreviousStartTime = time.time()     

       numNodes = 0
       # keep looping until there are nodes still to be checked
       while stack:
           StartTime = time.time()
           
           if StartTime - PreviousStartTime >= 60:        
              PreviousStartTime = StartTime
                  
           # pop shallowest node (first node) from stack
           node = stack.pop()
                           
           if not node.subTree[0].explored: # in explored:
              node.subTree[0].explored = True 
              
              if node != node.subTree[0]:                                  
                 c = 0
                 for n in self.vertList[node.parent[0]].sortedChildrenKeys:
                    if n == node:
                       self.vertList[node.parent[0]].sortedChildrenKeys[c] = node.subTree[0]
                    c += 1
                       
                 c = 0
                 for n in self.vertList[node.subTree[0].parent[0]].sortedChildrenKeys:
                    if n == node.subTree[0]:
                       self.vertList[node.subTree[0].parent[0]].sortedChildrenKeys[c] = node
                    c += 1
                 
                 nodeParent = node.parent            
                 node.parent = node.subTree[0].parent              
                 node.subTree[0].parent = nodeParent                                  
                 node.sortedChildrenKeys  = node.subTree[0].sortedChildrenKeys
                 
              
              #neighbours = node.sortedChildrenKeys
              neighbours = node.subTree[0].sortedChildrenKeys
                                                                            
              # add neighbours of node to stack
              for neighbour in neighbours:
                  stack.append(neighbour)
           numNodes += 1          
       return
  
   def GetOrderedLeaves(self):   
       self.NormalizeTree()
       self.ResetMappingInfo()
       explored = []

       numVertices = len(self.vertList)  
       edgeString = ""
       
       WriteTreeFile = False       
                     
       if WriteTreeFile:
          treefile  = open("Tree_"+self.getName()+".graphml", "w") 
          treefile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><graphml>\n")
          treefile.write("<graph id=\"Graph\" uidGraph=\""+str(numVertices)+"\" uidEdge=\"10000\">\n")
              
       # keep track of nodes to be checked
       stack = [self.vertList[0]]
       
       real_leaves = []
      
       PreviousStartTime = time.time()     

       numNodes = 0
       # keep looping until there are nodes still to be checked
       while stack:
           StartTime = time.time()
           
           if StartTime - PreviousStartTime >= 60:        
              print("num nodes in dfs: ", numNodes)        
              PreviousStartTime = StartTime
                  
           # pop shallowest node (first node) from stack
           node = stack.pop()
                           
           if True:
              print(node.getId(), end = " ")
                                         
              if WriteTreeFile:
                 treefile.write("<node positionX=\""+str(node.index*50)+"\" positionY=\""+str(node.treeLevel*50)+"\" id=\""+str(node.index)+"_"+str(node.getId())+"\" mainText=\""+str(node.getId())+"\" upText=\"\" ></node>\n")

              if len(node.parent)>0 and WriteTreeFile:              
                 parentid = self.vertList[node.parent[0]].id
                 parentindex = self.vertList[node.parent[0]].index
                 nodeid = node.id
                 nodeindex = node.index
                 edgeString += "<edge source=\"" + str(parentindex) +"_"+str(parentid) + "\" target=\"" + str(nodeindex) +"_"+str(nodeid) +  "\" isDirect=\"false\" weight=\"1\" useWeight=\"false\" id=\"10000\" text=\"\" upText=\"\" arrayStyleStart=\"\" arrayStyleFinish=\"\" model_width=\"4\" model_type=\"0\" model_curvedValue=\"0.1\" ></edge>" +"\n"
              
              ################################################

              #if it's a leaf, add it to the list that will be returned.
              if (len(node.getConnections()) == 0 or node.subTree[0].explored):                 
                 real_leaves.append(node)

              neighbours = None
              
              if not node.subTree[0].explored:
                 neighbours = node.sortedChildrenKeys
                 node.subTree[0].explored = True
                                                                           
                 # add neighbours of node to stack
                 for neighbour in neighbours: #reversed(neighbours):
                    print("n:",neighbour.getId(), end = " ")
                    stack.append(neighbour)
              print("")
              numNodes += 1
          
       if WriteTreeFile:
          treefile.write(edgeString)
          treefile.write("</graph></graphml>\n")          
          treefile.close()
       return real_leaves
               
    ######################################################################################################          
   def setIdOrder(self):

       self.id_Order = {}
       nodeCount = 0
       
       #START HERE: Add node and order in dictionary if not in the dictionary already MODIFY MATCH FUNCTION TO RESET THE ORDER DICTIONARY
       # keep track of all visited nodes
       explored = []
       # keep track of nodes to be checked
       queue = [self.vertList[0]]
        
       # keep looping until there are nodes still to be checked
       while queue:
          # pop shallowest node (first node) from queue
          node = queue.pop(0)
          if node not in explored:
              #print(node.getId(), end = " ")
              # add node to list of checked nodes
              explored.append(node)
              neighbours = node.sortedChildrenKeys
              
              
              if not node.getId() in self.id_Order:
                 self.id_Order[node.getId()] = nodeCount
                 nodeCount += 1

              # add neighbours of node to queue
              for neighbour in neighbours:
                  #print("n:",neighbour.getId(), end = " ")                   
                  queue.append(neighbour)
              #print("")
       return explored
       
######################################################################################################          
   def getIdOrder(self, id):
      return self.id_Order[id]