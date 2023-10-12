import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import sys
import clr

clr.AddReference("System.Core")
clr.AddReference("Grafit") 
clr.AddReference("GrafitRhino")  

#clr.AddReferenceToFile(LibPathGrafit)
#clr.AddReferenceToFile(LibPathGrafitRhino)  
from System.Linq import *
from Grafit import *
from GrafitRhino import *
from System import Array

from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path 

graph = Graph 

if isinstance(Graph, CDualUndirectedGraph[rg.Point3d, rg.Line]): 
    graph = Graph.PrimalDirectedGraph

subgraphsList = graph.GetDisconnectedParts()

tree = DataTree[int]()   
 
for i in range(subgraphsList.Count): 
    tree.AddRange(subgraphsList[i], GH_Path(i));

Subgraphs = tree;