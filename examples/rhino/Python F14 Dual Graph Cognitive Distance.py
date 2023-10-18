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

# Positive infinity (similar to double.PositiveInfinity in C#)
double_PositiveInfinity = float('inf')

# Maximum finite positive value (similar to double.MaxValue in C#)
double_MaxValue = sys.float_info.max


#Create Primal Graph from which Dual Graph will be created
if True: 
    lineGeometry = Array[CWLine](map(lambda s: CWLine(s), LineGeometry))

    graphElements, edgeLengths = GeometryToGraphElements.GetNodesAndEdgesFromLines(lineGeometry)

    primalGraph = CPrimalDirectedGraph(graphElements)
    primalGraph.AddWeightMatrix(edgeLengths)            # index 0
    primalGraph.AddEmptyWeightMatrix()                  # index 1 - angles
    primalGraph.AddEmptyWeightMatrix(double_MaxValue);  # index 2 - steps
    primalGraph.AddEmptyWeightMatrix(double_MaxValue);  # index 3 - time
    
    for i in range(len(primalGraph.UndirectedEdges)):
        n1 = primalGraph.UndirectedEdges[i][0]  # start node of edge #i
        n2 = primalGraph.UndirectedEdges[i][1]  # end node of edge #i
    
        weight_1 = 0.0  # angle of a single edge is 0.0 deg 
        weight_2 = 0.0  # step of a single edge is 0 
    
        primalGraph.SetWeightMatrixAndEdgeValue(weight_1, n1, n2, 1)  # forward direction angles
        primalGraph.SetWeightMatrixAndEdgeValue(weight_1, n2, n1, 1)  # backward direction angles
        
        primalGraph.SetWeightMatrixAndEdgeValue(weight_2, n1, n2, 2)  # forward direction steps
        primalGraph.SetWeightMatrixAndEdgeValue(weight_2, n2, n1, 2)  # backward direction steps
        
        primalGraph.SetWeightMatrixAndEdgeValue(TimeWeightsIn[i], n1, n2, 3)  # forward direction time
        primalGraph.SetWeightMatrixAndEdgeValue(TimeWeightsOut[i], n2, n1, 3)  # backward direction time

# Create Dual Graph
if True:    
    # Get dual nodes and edges from primal graph
    graphElements, edgeLengths, edgeAngles = GeometryToGraphElements.GetDualNodesAndEdgesFromPrimalGraph(primalGraph)
    
    # Create the dual graph using the primal graph and dual graph elements
    dualGraph = CDualUndirectedGraph(primalGraph, graphElements)

    # The order of dual graph weight matrices must be the same as in the primal graph
    # Dual lengths
    dualGraph.AddWeightMatrix(edgeLengths)  # index 0
    # Dual angles
    dualGraph.AddWeightMatrix(edgeAngles)  # index 1
    
    dualGraph.AddEmptyWeightMatrix(double_MaxValue);      #index 2 - steps
    dualGraph.AddEmptyWeightMatrix(double_MaxValue);      #index 3 - time 
    
    # Calculate dual edge values for weight matrices #2 and #3
    for i in range(dualGraph.UndirectedEdges.Count):
        edge = dualGraph.UndirectedEdges[i]
        primDirEdgeId_0 = edge[0]
        primDirEdgeId_1 = edge[1]
    
        e0n1 = dualGraph.Nodes[primDirEdgeId_0].PrimId1  # primal node from of edge 0
        e0n2 = dualGraph.Nodes[primDirEdgeId_0].PrimId2  # primal node to of edge 0
    
        e1n1 = dualGraph.Nodes[primDirEdgeId_1].PrimId1   # primal node from of edge 1
        e1n2 = dualGraph.Nodes[primDirEdgeId_1].PrimId2   # primal node to of edge 1

        # Edge to opposite itself
        if e0n1 == e1n2:
            oppositePrimDirEdgeId_0 = primalGraph.GetOppositeEdgeId(primDirEdgeId_0)
            oppositePrimDirEdgeId_1 = primalGraph.GetOppositeEdgeId(primDirEdgeId_1)
            
            # index 2 - steps
            dualGraph.SetWeightMatrixAndEdgeValue(double_PositiveInfinity, primDirEdgeId_0, primDirEdgeId_1, 2)
            dualGraph.SetWeightMatrixAndEdgeValue(double_PositiveInfinity, oppositePrimDirEdgeId_1, oppositePrimDirEdgeId_0, 2)
    
            # index 3 - time 
            dualGraph.SetWeightMatrixAndEdgeValue(double_PositiveInfinity, primDirEdgeId_0, primDirEdgeId_1, 3)
            dualGraph.SetWeightMatrixAndEdgeValue(double_PositiveInfinity, oppositePrimDirEdgeId_1, oppositePrimDirEdgeId_0, 3)
            continue
    
        undirPrimDirEdgeId_0 = primalGraph.GetUndirectedEdgeId(primDirEdgeId_0)
        undirPrimDirEdgeId_1 = primalGraph.GetUndirectedEdgeId(primDirEdgeId_1)
        
        isEdgeLink_0 = EdgeIsLinkUndir[undirPrimDirEdgeId_0]
        isEdgeLink_1 = EdgeIsLinkUndir[undirPrimDirEdgeId_1]
    
        iEdgeIsActivityNodeLink_0 = EdgesIsActivityNodeLinkUndir[undirPrimDirEdgeId_0]
        iEdgeIsActivityNodeLink_1 = EdgesIsActivityNodeLinkUndir[undirPrimDirEdgeId_1]

        # 0 = normal segment
        # 1 = modal link
        # 2 = activity node link
    
        # start
        LinkType_0 = 0
    
        if isEdgeLink_0:
            LinkType_0 = 1
    
        if iEdgeIsActivityNodeLink_0:
            LinkType_0 = 2
    
        # end
        LinkType_1 = 0
    
        if isEdgeLink_1:
            LinkType_1 = 1
    
        if iEdgeIsActivityNodeLink_1:
            LinkType_1 = 2
     
        dualStepWeight = 0.00000001
    
        # step between two default segments
        # penalty based on the angular deviation between the segments and presence of crossings
        # if there is no crossing the penalty is 0. if there is a crossing and we have to turn more than 30 degrees from the original direction, the penalty is 1
        
        if LinkType_0 == 0 and LinkType_1 == 0:  
            angle = dualGraph.GetEdgeValue(i, 1)
            if angle > 30.0 and len(primalGraph.Nodes[e0n2].OutNeighbourEdges) > 2:
                dualStepWeight = 1.0
    
        # step between default segment and activity node link
        # penalty is 1000 (a link penalty to avoid internal shortcuts) + 1 (to count for one decision)
        if (LinkType_0 == 2 and LinkType_1 == 0) or (LinkType_1 == 2 and LinkType_0 == 0):
            dualStepWeight = 1 + 1000
    
        # step between activity node and modal link
        # penalty is 0.5 (modal penalty is always in entry-exit pairs, we use 0.5 so that the full modal change takes 1 decision) + 1000 (activity node penalty)
        if (LinkType_0 == 2 and LinkType_1 == 1) or (LinkType_1 == 2 and LinkType_0 == 1):
            dualStepWeight = 0.5 + 1000
    
        # step between activity node link and activity node link
        # penalty is 1000 (activity node penalty)
        if (LinkType_0 == 2 and LinkType_1 == 2):
            dualStepWeight = 1000 + 1000
    
        # step between modal link and modal link
        # penalty is 1, this is used when traveling through the internal network
        if (LinkType_0 == 1 and LinkType_1 == 1):
            dualStepWeight = 1
    
        # step between modal link and default segment
        # penalty is 0.5 (modal penalty is always in entry-exit pairs, we use 0.5 so that the full modal change takes 1 decision)
        if (LinkType_0 == 1 and LinkType_1 == 0) or (LinkType_1 == 1 and LinkType_0 == 0):
            dualStepWeight = 0.5
    
        dualGraph.SetWeightMatrixAndEdgeValue(dualStepWeight, primDirEdgeId_0, primDirEdgeId_1, 2)  # index 2 - steps
        dualGraph.SetWeightMatrixAndEdgeValue(dualStepWeight, primalGraph.GetOppositeEdgeId(primDirEdgeId_1), primalGraph.GetOppositeEdgeId(primDirEdgeId_0), 2)
    
        dualEdgeTimeWeight1 = (primalGraph.GetEdgeValue(primDirEdgeId_0, 3) + primalGraph.GetEdgeValue(primDirEdgeId_1, 3)) / 2.0
        dualEdgeTimeWeight2 = (primalGraph.GetEdgeValue(primalGraph.GetOppositeEdgeId(primDirEdgeId_1), 3) + primalGraph.GetEdgeValue(primalGraph.GetOppositeEdgeId(primDirEdgeId_0), 3)) / 2.0
    
        dualGraph.SetWeightMatrixAndEdgeValue(dualEdgeTimeWeight1, primDirEdgeId_0, primDirEdgeId_1, 3)  # index 3 - time
        dualGraph.SetWeightMatrixAndEdgeValue(dualEdgeTimeWeight2, primalGraph.GetOppositeEdgeId(primDirEdgeId_1), primalGraph.GetOppositeEdgeId(primDirEdgeId_0), 3)
    
    
# Calculate shortest paths
dualGraph.APShortestPathsByManyWeights(WeightMatrixIndexMain, WeightMatrixIndexFilter, GPU, 0.0000000001)
#dualGraph.APShortestPathsByOneWeight(WeightMatrixIndexMain, GPU) 

 
# Calculate all other Weight Matrices, which are not WeightMatrixIndexMain
allIds = list(range(len(dualGraph.weightMatrices)))
otherMatricesIds = [i for i in allIds if i != WeightMatrixIndexMain]
dualGraph.FillWeightMatrixBySPRestore(Array[int](otherMatricesIds), GPU)
    
DualGraph = dualGraph   
 


