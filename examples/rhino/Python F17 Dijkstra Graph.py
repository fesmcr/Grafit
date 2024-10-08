import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import sys
import clr 

clr.AddReference("System.IO")

from System import Environment
from System.IO import *

if CustomLibPath is not None: 
	# Check if the assembly is loaded
	if "Grafit" not in sys.modules: 
		searchResult = Directory.GetFiles(CustomLibPath, "Grafit.dll", SearchOption.AllDirectories)

		if len(searchResult) == 0:
			raise Exception("Grafit.dll is not found in folder.")
			
		LibPathGrafit = searchResult[0] 
		LibPathGrafitRhino = Path.GetDirectoryName(LibPathGrafit) + "\\"  + "GrafitRhino.dll"   
	
		clr.AddReferenceToFileAndPath(LibPathGrafit)
		clr.AddReferenceToFileAndPath(LibPathGrafitRhino) 
else:
	clr.AddReference("Grafit") 
	clr.AddReference("GrafitRhino")  

from Grafit import *
from GrafitRhino import *
from System import Array

primalGraph = {}

# prepare graph geometry
lineGeometry = Array[CWLine](map(lambda s: CWLine(s), LineGeometry))
graphElements, edgeLengths = GeometryToGraphElements.GetNodesAndEdgesFromLines(lineGeometry)

# create graph
primalGraph = CPrimalDirectedGraph(graphElements)

# add weight matrices
primalGraph.AddWeightMatrix(edgeLengths)  # index 0 - metric (or any other)
primalGraph.AddEmptyWeightMatrix(0, True )  # index 1 - angles (should always be #1) 

# init angle matrix
for i in range(len(primalGraph.UndirectedEdges)):
    n1 = primalGraph.UndirectedEdges[i][0]  # start node of edge #i
    n2 = primalGraph.UndirectedEdges[i][1]  # end node of edge #i 

    weight_1 = 0.0  # angle of a single edge is 0.0 deg
    weight_matrix_id = 1

    primalGraph.SetWeightMatrixAndEdgeValue(weight_1, n1, n2, weight_matrix_id)  # forward direction
    primalGraph.SetWeightMatrixAndEdgeValue(weight_1, n2, n1, weight_matrix_id)  # backward direction   
  

StartNodeIds = Array[int](OriginIds)
WeightMatrixId = WeightMatrixIndex
RadiusMatrixId = RadiusMatrixIndex
Tolerance = 0.000001

primalGraph.APDijkstraSPSingleWeight(Radius, StartNodeIds, WeightMatrixId, RadiusMatrixId, Tolerance) 
graph = primalGraph  
