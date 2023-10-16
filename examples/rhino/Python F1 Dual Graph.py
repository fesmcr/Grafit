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
dualGraph = {} 


#Create Primal Graph from which Dual Graph will be created
if True: 
    lineGeometry = Array[CWLine](map(lambda s: CWLine(s), LineGeometry))

    graphElements, edgeLengths = GeometryToGraphElements[rg.Point3d, rg.Line].GetNodesAndEdgesFromLines(lineGeometry)

    primalGraph = CPrimalDirectedGraph[rg.Point3d, rg.Line](graphElements)
    primalGraph.AddWeightMatrix(edgeLengths)  # index 0
    primalGraph.AddEmptyWeightMatrix()  # index 1 - angles
    
    for i in range(len(primalGraph.UndirectedEdges)):
        n1 = primalGraph.UndirectedEdges[i][0]  # start node of edge #i
        n2 = primalGraph.UndirectedEdges[i][1]  # end node of edge #i
    
        weight_1 = 0.0  # angle of a single edge is 0.0 deg
        weight_matrix_id = 1
    
        primalGraph.SetWeightMatrixAndEdgeValue(weight_1, n1, n2, weight_matrix_id)  # forward direction
        primalGraph.SetWeightMatrixAndEdgeValue(weight_1, n2, n1, weight_matrix_id)  # backward direction

# Create Dual Graph
if True:    
    # Get dual nodes and edges from primal graph
    graphElements, edgeLengths, edgeAngles = GeometryToGraphElements[rg.Point3d, rg.Line].GetDualNodesAndEdgesFromPrimalGraph(primalGraph)
    
    # Create the dual graph using the primal graph and dual graph elements
    dualGraph = CDualUndirectedGraph[rg.Point3d, rg.Line](primalGraph, graphElements)

    # The order of dual graph weight matrices must be the same as in the primal graph
    # First, add dual lengths
    dualGraph.AddWeightMatrix(edgeLengths)  # index 0
    # Second, add dual angles
    dualGraph.AddWeightMatrix(edgeAngles)  # index 1
    
    # If you need to set individual weight matrix values, you can do so here
    # some_weight = 0
    # weight_matrix_index = 2
    # dualGraph.SetWeightMatrixValue(some_weight, prim_edge_id_0, prim_edge_id_1, weight_matrix_index)
    
    if UseFilterMatrix:
        dualGraph.APShortestPathsByManyWeights(WeightMatrixIndexMain, WeightMatrixIndexFilter, GPU)
    else:
        dualGraph.APShortestPathsByOneWeight(WeightMatrixIndexMain, GPU) 

# If graph has more than 1 weight matrix, calculate distances along shortest paths according to all other weights
if CalculateAllMatrices:
    # Select which weights are needed to measure shortest paths
    # By default, all other matrices which are not the main are selected
    allIds = list(range(len(dualGraph.weightMatrices)))
    otherMatricesIds = [i for i in allIds if i != WeightMatrixIdxMain]
    dualGraph.FillWeightMatrixBySPRestore(otherMatricesIds, GPU)
    
DualGraph = dualGraph    
