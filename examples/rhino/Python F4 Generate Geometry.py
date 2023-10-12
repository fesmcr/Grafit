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

graph = Graph 

if isinstance(Graph, CDualUndirectedGraph[rg.Point3d, rg.Line]): 
    graph = Graph.PrimalDirectedGraph

NodeAsPoints = [s.Internal for s in Enumerable.Select(graph.NodesGeometryList, lambda s: s)]
EdgesDirected = [s.Internal for s in Enumerable.Select(graph.GenerateDirectedEdgeGeometry(CWLine.LineFromPoints), lambda s: s)]
EdgesUndirected = [s.Internal for s in Enumerable.Select(graph.GenerateUndirectedEdgeGeometry(CWLine.LineFromPoints), lambda s: s)]
