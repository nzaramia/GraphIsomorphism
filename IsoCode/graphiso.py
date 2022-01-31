import graph 
import isotree
import time

######################################################################################################

class GraphIso:  
          
    def convertGraphToTree(self, g, nodeIndex, killNodes, maxTreeHeight):
       print("convert graph to a tree")
       # keep track of nodes to be checked
       currentLevel = 0
       iterationCount = 0

       #reset all vertices
       numVertices = len(g.vertList)  
       for i in range(numVertices): 
          g.vertList[i].alive = True
          g.vertList[i].cycles.clear()
          g.vertList[i].currentLevel.clear()
          g.vertList[i].parent.clear()

       g.vertList[nodeIndex].currentLevel.append(currentLevel)
       vertexQueue = [g.vertList[nodeIndex]]
       nodesToKill = []
       
       numVertices = len(g.vertList)
       
       node = vertexQueue.pop(0)
       node.parent.append(None)
       node.treeLevel = 0;
       nodeCurrentLevel = node.currentLevel.pop(0)
       nodeCurrentParent = node.parent.pop(0)

       LiveNodes = True
       
       #Tree to return
       t = isotree.IsoTree()
       t.setName(g.getName())
       numNodesInTree = 0
       
       t.show_node_size()
       
       parentInTreeIndexQueue = []
       parentInTreeIndex = None

       numProcNodes = 0
          
       LoopCondition = True
       nm = 0
       
       if killNodes:
          LoopCondition = LiveNodes
       else:
          LoopCondition = (nm <= numVertices)

       numLoop = -1
       
       # keep looping for num vertices times
       while LoopCondition:
         LiveNodes = False
         numLoop += 1
                
         #lists of unique subtrees on this level    
         currentLevel_Live_Node = []
         currentLevel_Live_Node_Parent = []
         
         currentLevelUniqueNodes = 0
         
         numNodesCurLevel = 0
         
         curLevelNodeDictionary = {}
         
         PreviousStartTime = time.time()     

         while (nodeCurrentLevel == currentLevel and node != None):
            
            StartTime = time.time()
            BenchStart = StartTime
            
            numNodesCurLevel += 1    
            
            if StartTime - PreviousStartTime >= 20:        
               print("num nodes current level: ", numNodesCurLevel, " Level: ", currentLevel)        
               PreviousStartTime = StartTime
                    
            #update the new nodes cycle information
            node.cycles.append(currentLevel)    

            #add the current node to the tree
            t.addVertex(numNodesInTree)
            t.vertList[numNodesInTree].setId(node.getId())
            t.vertList[numNodesInTree].cycles = node.cycles
            t.vertList[numNodesInTree].index = numNodesInTree        
            t.vertList[numNodesInTree].treeLevel = currentLevel   
            
                                  
            if (parentInTreeIndex is not None):
               t.addChild(parentInTreeIndex, numNodesInTree)
               t.vertList[numNodesInTree].parent.append(parentInTreeIndex)
                                  
            ##############################################################################################
            #Look for this subtree in the list of subtrees, if it exists then we don't have to process it.
            #####################
            node_withParent = None
           
            if (parentInTreeIndex is not None):
               cur_nodeId = t.vertList[numNodesInTree].id
               cur_parent_nodeId = t.vertList[parentInTreeIndex].id
              
               if cur_nodeId in curLevelNodeDictionary:                 
                  if cur_parent_nodeId in curLevelNodeDictionary[cur_nodeId]:
                     node_withParent = curLevelNodeDictionary[cur_nodeId][cur_parent_nodeId][0]
                                                     
            #ATTACH THE NODE TO THE TREE IN THE SUBTREE VARIABLE if same parent and child found
            #####################
            if (node_withParent is not None):           
               t.vertList[numNodesInTree].subTree.append(node_withParent)
               
               t.vertList[numNodesInTree].subTree[0].subTreeUsageCount += 1
                                     
            else: #attach itself
               
               t.vertList[numNodesInTree].subTree.append(t.vertList[numNodesInTree])
            ##########################################################################################        

            numNodesInTree = numNodesInTree + 1
                    
            processNodeCondition = True
            
            if killNodes:
               processNodeCondition = (node.alive) and (node_withParent is None)
            else:
               processNodeCondition = (node_withParent is None)
               #Might put this back
               processNodeCondition = processNodeCondition and ((numLoop == 0) or (node != g.vertList[nodeIndex]))  #do not process the node if the lineage is back to the root

            if (processNodeCondition):
               LiveNodes = True
               
               #if this unique subtree was not found in the list then add it
               if (parentInTreeIndex is not None):

                  if not t.vertList[numNodesInTree-1].id in curLevelNodeDictionary:
                     curLevelNodeDictionary[t.vertList[numNodesInTree-1].id] = {}
                     
                  curLevelNodeDictionary[t.vertList[numNodesInTree-1].id][t.vertList[parentInTreeIndex].id] = []              
                  curLevelNodeDictionary[t.vertList[numNodesInTree-1].id][t.vertList[parentInTreeIndex].id].append(t.vertList[numNodesInTree-1].subTree[0])             
               
               neighbours = node.getConnections()     
               
               #STOP IF YOU MEET THE ROOT AGAIN!!!
               # only process neighbors of the root if first time we see it because otherwise the cycle is complete                                                            
               if (node.id != t.vertList[0].id or nodeCurrentParent == None):  
                  # add neighbours of node to queue
                  for neighbour in neighbours:
                     iterationCount += 1               
                     if (nodeCurrentParent == None or neighbour.getId() != nodeCurrentParent.getId()):
                        neighbour.currentLevel.append(currentLevel + 1)

                        neighbour.parent.append(node)
                        vertexQueue.append(neighbour)
                        parentInTreeIndexQueue.append(numNodesInTree-1)                                    
               
               if killNodes:
                  nodesToKill.append(node)
               
               EndTime = time.time()
               
            if (vertexQueue):        
               node = vertexQueue.pop(0)
               nodeCurrentLevel = node.currentLevel.pop(0)
               nodeCurrentParent = node.parent.pop(0)
               parentInTreeIndex = parentInTreeIndexQueue.pop(0)
            else:
               node = None
                            
         currentLevel = currentLevel + 1
               
         if killNodes:
            LoopCondition = LiveNodes and (node is not None)
         else:
            nm += 1
            LoopCondition = (nm < numVertices) and (node is not None) and ( (maxTreeHeight == -1) or (currentLevel < maxTreeHeight) )
                            
         if killNodes:
            while (nodesToKill):
               nodeToKill = nodesToKill.pop(0)
               nodeToKill.alive = False

       t.treeHeight = currentLevel
       return t

    ######################################################################################################            
    def childCmp_descriptor(self, a):
       return a.descriptor
          
    def childCmp_ID(self, a):
       return a.id      
       
    ######################################################################################################          
    def sort_tree_unique_subtree(self, t, withNodeOrder=False):
       print("sorting tree")
       numVertices = len(t.vertList)
       iterationCount = 0
      
       nextParentList = []

       #reset all vertices
       numVertices = len(t.vertList)  
       for i in range(numVertices): 
          t.vertList[i].descriptor = ""
             
       currentLevel = t.treeHeight-1
       
       #start from the last level and go up all the way to the root   
       vertexIndex = numVertices-1
       childDescriptorList = []
      
       while vertexIndex>= 0:  #process all levels including the root (level 0)                     
          currentLevel = t.vertListLevelOrder[vertexIndex].treeLevel
                
          currentLevelVertices = []
          #Get current level vertices
          while vertexIndex>=0 and t.vertListLevelOrder[vertexIndex].treeLevel == currentLevel:                  
             currentLevelVertices.append(t.vertListLevelOrder[vertexIndex])
             vertexIndex -= 1
                 
          childDescriptorList = []
          
          #Sort the subtree descriptors of that level and assign them a rank number.
          #If two subtrees are equal then they have the same rank number.
          #Also when comparing the two trees a comparison of the actual subtree descriptors is required for each level.
          #The rank number will replace the descriptor in the parent's descriptor.
          
          for v in currentLevelVertices:
             if (v.subTree[0].descriptor == ""):
                childDescriptorList.clear()      
                neighbours = v.subTree[0].getConnections()                          
             
                # add neighbours of node to queue
                for neighbour in neighbours:
                   childDescriptorList.append(str(neighbour.subTree[0].subtreeRank))
                               
                childDescriptorList.sort()
                v.subTree[0].cycles.sort()
             
                v.subTree[0].descriptor += "("
                v.subTree[0].descriptor += str(len(v.subTree[0].getConnections()))
                v.subTree[0].descriptor += ","
                               
                
                for c in v.subTree[0].cycles:
                   v.subTree[0].descriptor += str(c)
                   v.subTree[0].descriptor += ","
           
                v.subTree[0].descriptor += "("     
          
                for c in childDescriptorList:
                   v.subTree[0].descriptor += str(c)
                   v.subTree[0].descriptor += ","
                         
                v.subTree[0].descriptor += ")"
                
                if withNodeOrder:
                   v.subTree[0].descriptor += "("
                   v.subTree[0].descriptor += str(t.getIdOrder(v.id))
                   v.subTree[0].descriptor += ")"
                
                v.subTree[0].descriptor += ")"
                         
                t.SortChildren(v.subTree[0].index)                   
                
             v.descriptor = v.subTree[0].descriptor 

             if not withNodeOrder:
                v.descriptorWithoutOrder = v.descriptor
             
          currentLevelRealSubtrees = []
          #Get current level real subtrees
          for c in currentLevelVertices:
             if c.index == c.subTree[0].index:
                currentLevelRealSubtrees.append(c)
                      
          #Sort the subtrees according to their descriptor
          currentLevelRealSubtrees.sort(key=self.childCmp_ID)  #this is for deterministic behaviour
          currentLevelRealSubtrees.sort(key=self.childCmp_descriptor)
          
          #Set each subtree's rank
          currentRank = 0
          sLength = len(currentLevelRealSubtrees)
          
          if (sLength > 0):
             currentLevelRealSubtrees[0].subtreeRank = currentRank
          
          for i in range(1, sLength):
             if currentLevelRealSubtrees[i].descriptor != currentLevelRealSubtrees[i-1].descriptor:
                currentRank += 1
             currentLevelRealSubtrees[i].subtreeRank = currentRank
          
          if not withNodeOrder:
             for i in range(0, sLength):         
                t.completeSubtreeListLevelOrder.insert(0, currentLevelRealSubtrees[i])

    ######################################################################################################          
    def sortTree(self, t):

       #do initial sort
       self.sort_tree_unique_subtree(t)  #pass no id order

       #determine order of id
       t.setIdOrder()

       t.resetSorting()
              
       #sort the tree again with id order
       self.sort_tree_unique_subtree(t, True)  #pass with id order
       
    ####################START NEW SECTION       
    
    #####################################################################################################       
    def MatchFromLeaf(self, g1, g2, t1, t2, t2_leaves, v1, numVertices, GraphMapping):
       newMatch = []
       newMatch.append(False)
       
       foundMatch = False
    
       v2_index = 0
       for v2 in t2_leaves:         
          StartMatch = time.time()
          newMatch[0] = False
          if self.lineageMatch(g1, g2, v1, v2, t1, t2, GraphMapping, newMatch):
            
             foundMatch = True
             if (newMatch[0]):
                self.AssignLineage(v1, v2, t1, t2, GraphMapping)
             t2_leaves.pop(v2_index)
             break
          v2_index += 1
         
          if len(GraphMapping) == len(g1.vertList):
             break
          EndMatch = time.time()
       
       return foundMatch
    
    ######################################################################################################       
    def GetMapping2(self, g1, g2, t1, t2, numVertices):         
       
       print("Mapping the nodes...")
       print("Num nodes in tree t1: ", len(t1.vertList))
       print("****Tree 1 dfs****")
       t1_leaves = t1.GetOrderedLeaves()
       print("")
       print("****Tree 2 dfs****")      
       t2_leaves = t2.GetOrderedLeaves()
       print("")
                    
       print("Num nodes in t1 tree: ", len(t1.vertList))
       print("Num leaves in t1: ", len(t1_leaves))
       
       print("Num nodes in t2 tree: ", len(t2.vertList))
       print("Num leaves in t2: ", len(t2_leaves))
          
       GraphMapping = {}
       
       #count = 0;
       
       while t1_leaves:
       
          LeafMappingFound = True
          
          while (LeafMappingFound):
             LeafMappingFound = False
             t1_leaf_index = 0
             
             for t1_leaf in t1_leaves:
                if t1_leaf.id in GraphMapping:
                   LeafMappingFound = True
                   break
                else:
                   t1_leaf_index += 1
                   
             if LeafMappingFound:
                foundMapping = self.MatchFromLeaf(g1, g2, t1, t2, t2_leaves, t1_leaves[t1_leaf_index], numVertices, GraphMapping)
                isIso = self.partialCheckIso(g1, g2, GraphMapping)
                t1_leaves.pop(t1_leaf_index)

                
          if t1_leaves:          
             foundMapping = self.MatchFromLeaf(g1, g2, t1, t2, t2_leaves, t1_leaves[0], numVertices, GraphMapping)
             t1_leaves.pop(0)
                    
             
       return GraphMapping
####################END NEW SECTION
       
              
    ######################################################################################################       
    def GetMapping(self, g1, g2, t1, t2, numVertices):         
       
       print("Mapping the nodes...")
       print("Num nodes in tree t1: ", len(t1.vertList))
       print("****Tree 1 dfs****")
       t1_leaves = t1.GetOrderedLeaves()
       print("")
       print("****Tree 2 dfs****")      
       t2_leaves = t2.GetOrderedLeaves()
       print("")
                    
       print("Num nodes in t1 tree: ", len(t1.vertList))
       print("Num leaves in t1: ", len(t1_leaves))
       
       print("Num nodes in t2 tree: ", len(t2.vertList))
       print("Num leaves in t2: ", len(t2_leaves))
          
       GraphMapping = {}
       
       newMatch = []
       newMatch.append(False)
       
       for v1 in t1_leaves:                    
          v2_index = 0
          for v2 in t2_leaves:         
             StartMatch = time.time()
             newMatch[0] = False
             if self.lineageMatch(g1, g2, v1, v2, t1, t2, GraphMapping, newMatch):
                
                if (newMatch[0]):
                   self.AssignLineage(v1, v2, t1, t2, GraphMapping)
                t2_leaves.pop(v2_index)
                break
             v2_index += 1
             
             if len(GraphMapping) == len(g1.vertList):
                break
             EndMatch = time.time()
             
       return GraphMapping
      
    ######################################################################################################             
    def lineageMatch(self, g1, g2, startNode1, startNode2, t1, t2, mapping, newMatch):         
       curNode1 = startNode1
       curNode2 = startNode2
       TempMapping = dict(mapping)#{}
       
       isleaf1_realLeaf = (len(startNode1.subTree[0].getConnections()) == 0)
       isleaf2_realLeaf = (len(startNode2.subTree[0].getConnections()) == 0)
       
       if not (isleaf1_realLeaf and isleaf2_realLeaf):          
          #Bring the two nodes to the same level
          while curNode1.treeLevel < curNode2.treeLevel:
             curNode2 = t1.vertList[curNode2.parent[0]]
          
          while (curNode2.treeLevel < curNode1.treeLevel):
             curNode1 = t1.vertList[curNode1.parent[0]]
          
       if not self.leaves_Comparable(startNode1, startNode2, curNode1, curNode2):
          return False
       
       isMatch = True
       
       while True:            
          if curNode1.id in mapping:   
             if (mapping[curNode1.id] != curNode2.id):
                isMatch = False
                return isMatch
                break
          else:
             #curNode1 is not in mapping, it has to be same for curNode2
             for v in mapping:
               if mapping[v] == curNode2.id:
                  isMatch = False
                  return isMatch
                  break
          
          if (curNode1.id in TempMapping):
             if (TempMapping[curNode1.id] != curNode2.id):
                isMatch = False
                return isMatch
          else:
             #curNode1 is not in mapping, it has to be same for curNode2
             newMatch[0] = True         
             for v in TempMapping:
                if TempMapping[v] == curNode2.id:
                   isMatch = False
                   return isMatch         
                      
          #not a match if the two vertices don't have the same degree
          if len(g1.vertList[curNode1.id].getConnections()) != len(g2.vertList[curNode2.id].getConnections()):
             isMatch = False
             return isMatch         
          
          TempMapping[curNode1.id] = curNode2.id
          
          #if this subtree is not already a candidate
          if not curNode2.subTree[0].MySubTreeIsACandidate and (len(curNode2.subTree[0].getConnections())!= 0):
             #And its a real subtree used more than once and the usage counts are equal
             if (curNode1.subTree[0].subTreeUsageCount > 0) and (curNode1.subTree[0].subTreeUsageCount == curNode2.subTree[0].subTreeUsageCount):         
                curNode2.subTree[0].MySubTreeIsACandidate = True
                curNode2.subTree[0].SubtreeLineagePotentialMapping[curNode1.id] = curNode2.id
          
          isCurNode1Root = len(curNode1.parent) == 0
          isCurNode2Root = len(curNode2.parent) == 0
          
          if (isCurNode1Root) != (isCurNode2Root):
             isMatch = False
             return isMatch
             break
             
          if isCurNode1Root and isCurNode2Root:
             #only accept this lineage mapping if it maintains isomorphism
             #if (self.partialCheckIso(g1, g2, TempMapping)):
             return True
             #else:
             #   return False
             break
                      
          t2.vertList[curNode2.parent[0]].subTree[0].SubtreeLineagePotentialMapping = curNode2.subTree[0].SubtreeLineagePotentialMapping
                    
          curNode1 = t1.vertList[curNode1.parent[0]]
          curNode2 = t2.vertList[curNode2.parent[0]]
                              
       print("****End lineage match****")   
       return isMatch
       
    ######################################################################################################       
    def AssignLineage(self, startNode1, startNode2, t1, t2, mapping):
       curNode1 = startNode1
       curNode2 = startNode2
       
       #Bring the two nodes to the same level
       while curNode1.treeLevel < curNode2.treeLevel:
          curNode2 = t1.vertList[curNode2.parent[0]]
          
       while curNode2.treeLevel < curNode1.treeLevel:
          curNode1 = t1.vertList[curNode1.parent[0]]   
               
       #assign the subtree first
       if curNode2.subTree[0].MySubTreeIsACandidate:
          for id in curNode2.subTree[0].SubtreeLineagePotentialMapping:
             if id not in mapping:
                mapping[id] = curNode2.subTree[0].SubtreeLineagePotentialMapping[id]
       
       while True:              
          #if not mapped 
          if (curNode1.id not in mapping):
             mapping[curNode1.id] = curNode2.id
                               
          #Make sure to add the subtree mapping if it is a candidates
          
          curNode2.subTree[0].SubtreeLineageMappingIsComplete = True
          if curNode1 != t1.vertList[0] and curNode2 != t2.vertList[0]:
             curNode1 = t1.vertList[curNode1.parent[0]]
             curNode2 = t2.vertList[curNode2.parent[0]]
          else:
             break
        
       #reset candidates
       numVertices = len(t2.vertList)  
       for i in range(numVertices): 
          t2.vertList[i].MySubTreeIsACandidate = False
          t2.vertList[i].SubtreeLineagePotentialMapping = {}
             
    ######################################################################################################       
    def leaves_Comparable(self, leaf1, leaf2, leaf1_atlevel, leaf2_atlevel):
       
       isleaf1_realLeaf = (len(leaf1.subTree[0].getConnections()) == 0)
       isleaf2_realLeaf = (len(leaf2.subTree[0].getConnections()) == 0)

       #if both leaf1 and leaf2 are real leaves and they are on the same tree level -> they are comparable
       if isleaf1_realLeaf and isleaf2_realLeaf:
          if leaf1.subTree[0].treeLevel == leaf2.subTree[0].treeLevel:   
             return True
          else:
             return False
       
       #if leaf1 is not a real leaf then leaf2 at same level must have subtree with completed and assigned mapping
       #if it is then it's comparable
       #otherwise not comparable.
       if not isleaf1_realLeaf:
          return leaf2_atlevel.subTree[0].SubtreeLineageMappingIsComplete 
       else:      
          #otherwise if leaf1 is a real leaf then leaf2 must be a potential mapping
          return leaf2.subTree[0].MySubTreeIsACandidate
       
    ######END PREVIOUS VERSION OF MAPPING               
    ######################################################################################################       

    def partialCheckIso(self, g1, g2, mapping):

       numMaps = len(mapping)
       
       v1 = None
       v2 = None
       neighbor1 = None
       ValidMapping = True
       
       for i in range(numMaps):
          
          v1 = g1.vertList[i]
          neighbors1 = v1.getConnections()
          
          if i in mapping:
             v2 = g2.vertList[mapping[i]]
             neighbors2 = v2.getConnections()            
          
             for neighbor1 in neighbors1:         
                neighborFound = False
                if neighbor1.getId() in mapping:
                   for neighbor2 in neighbors2:
                      if neighbor2.getId() == mapping[neighbor1.getId()]:
                         neighborFound = True
                   if not neighborFound:
                      ValidMapping = False
                      break
       return ValidMapping
                         
    ######################################################################################################       

    def checkIso(self, g1, g2, mapping, partial=False):

       numMaps = len(mapping)

       if not partial:
          if numMaps <= 0:
             print("Invalid mapping!!!")
             return False
          print("NumVertices:", len(g1.vertList))
          print("Num maps:", numMaps)
       
       v1 = None
       v2 = None
       neighbor1 = None
       
       for i in range(numMaps):
          neighborFound = False
          
          v1 = g1.vertList[i]
          neighbors1 = v1.getConnections()
          
          if i in mapping:
             v2 = g2.vertList[mapping[i]]
             neighbors2 = v2.getConnections()            
          
             for neighbor1 in neighbors1:         
                neighborFound = False
             
                for neighbor2 in neighbors2:
                   if neighbor1.getId() in mapping:
                      if neighbor2.getId() == mapping[neighbor1.getId()]:
                         neighborFound = True
                         
          if not neighborFound:
             break
             
                
       #create reverse mapping, and check iff g2 mapped to g1
       reverseMapping = {}
       
       for i in range(numMaps):
          if i in mapping:
             reverseMapping[mapping[i]] = i

       if not partial and len(reverseMapping) != len(mapping):
          print("Here: Mapping is not one-to-one!!!")
          return False

       if not neighborFound:
          return False
                
       for i in range(numMaps):
          neighborFound = False
          
          v2 = g2.vertList[i]
          neighbors2 = v2.getConnections()
          
          if i in reverseMapping:
             v1 = g1.vertList[reverseMapping[i]]
             neighbors1 = v1.getConnections()
          
             for neighbor2 in neighbors2:         
                neighborFound = False
             
                for neighbor1 in neighbors1:
                   if neighbor2.getId() in reverseMapping:
                      if neighbor1.getId() == reverseMapping[neighbor2.getId()]:
                         neighborFound = True
                         
          if not neighborFound:
             break
             
       if not neighborFound:
           return False
                                     
       if neighborFound and not partial:
          if (len(g1.vertList) == numMaps and len(g2.vertList) == numMaps):
             return True
          else:
             return False


    ######################################################################################################       
    def TreesMatch(self, t1, t2):
      isMatch = True
      
      t1_Subtree_len = len(t1.completeSubtreeListLevelOrder)
      t2_Subtree_len = len(t2.completeSubtreeListLevelOrder)
      
      isMatch = (t1_Subtree_len == t2_Subtree_len)
      
      for i in range(t1_Subtree_len):     
         isMatch = isMatch and (t1.completeSubtreeListLevelOrder[i].descriptorWithoutOrder == t2.completeSubtreeListLevelOrder[i].descriptorWithoutOrder)
           
         if not isMatch:        
            break
      
      return isMatch
      

    ######################################################################################################       
    ###############################NEXT: start working on the mapping algorithm
    def match(self, g1, g2, g1_minDegreeOccurenceIndex, FindAllIsomorphisms, killNodes, maxTreeHeight):
    
       doTreesMatch = False
       print("G1 tree conversion.")
       t1 = self.convertGraphToTree(g1, g1_minDegreeOccurenceIndex, killNodes, maxTreeHeight)
       
       self.sortTree(t1)
       
       print(t1.vertList[0].descriptor)
       print("")
       
       t2 = None
       
       checkCount = 0
       numIso = 0
       
       for i in range(len(g2.vertList)): #range(15, len(g2.vertList)): 
          g1_len = len(g1.vertList[g1_minDegreeOccurenceIndex].getConnections())
          g2_len = len(g2.vertList[i].getConnections())
          if (len(g2.vertList[i].getConnections()) == len(g1.vertList[g1_minDegreeOccurenceIndex].getConnections())):
             print("G2 vertex index: ", i)
             checkCount += 1
             print("# comparisons: ", checkCount)
             t2 = self.convertGraphToTree(g2, i, killNodes, maxTreeHeight)
             self.sortTree(t2)
             
             print(t2.vertList[0].descriptor)
          
             if (self.TreesMatch(t1, t2)):
                doTreesMatch = True
                
                Mapping = self.GetMapping2(g1, g2, t1, t2, len(g1.vertList))
                print("Num nodes in mapping: ", len(Mapping))               
                
                if self.checkIso(g1, g2, Mapping):
                   print ("Yes, it's isomorphic.")
                   #input("")
                   sortedMapping = sorted(Mapping)
                   print ("Sorted mapping")
                   print("[", end = '')
                   for key in sortedMapping:                   
                      print(key, ":", Mapping[key], ", ", end = '')
                   print("]")
                   numIso += 1
                   
                   if not FindAllIsomorphisms:
                      break               
                else:
                   print("Not isomorphic but trees match.")
                   sortedMapping = sorted(Mapping)
                   print ("Sorted mapping")
                   print("[", end = '')
                   for key in sortedMapping:                   
                      print(key, ":", Mapping[key], ", ", end = '')
                   print("]")
                   #input("")
               
                t1.ResetMappingInfo()           
             else:
                print("Not isomorphic and trees do not match.")
                   
             print("")

       print("Number of tree comparisons:", checkCount)
       stop = True
       
       return numIso, doTreesMatch, t1.treeHeight


    #ONLY USED FOR SPECIFIC MATCHES
    def singlematch(self, g1, g2, g1_minDegreeOccurenceIndex, FindAllIsomorphisms, killNodes, maxTreeHeight):
        
       doTreesMatch = False
       print("G1 tree conversion.")
       t1 = self.convertGraphToTree(g1, 2, killNodes, maxTreeHeight)
       self.sortTree(t1)
       
       print(t1.vertList[0].descriptor)
       print("")
       
       t2 = None
       
       checkCount = 0
       numIso = 0
       
       i = 25
       
       print("# comparisons: ", checkCount)
       t2 = self.convertGraphToTree(g2, i, killNodes, maxTreeHeight)
       self.sortTree(t2)
             
       print(t2.vertList[0].descriptor)
          
       if (self.TreesMatch(t1, t2)):
          doTreesMatch = True
            
          Mapping = self.GetMapping2(g1, g2, t1, t2, len(g1.vertList))
          print("Num nodes in mapping: ", len(Mapping))               
            
          if self.checkIso(g1, g2, Mapping):
             print ("Yes, it's isomorphic.")
             print(Mapping) 
             numIso += 1    
               
          else:
             print("Not isomorphic but trees match.")
             print(Mapping)           
       else:
          print("Not isomorphic and trees do not match.")
               
       print("")

       print("Number of tree comparisons:", checkCount)
       stop = True
       
       return numIso, doTreesMatch, t1.treeHeight


