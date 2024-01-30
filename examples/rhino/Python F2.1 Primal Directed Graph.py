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

# Positive infinity (similar to double.PositiveInfinity in C#)
double_PositiveInfinity = float('inf')

# Maximum finite positive value (similar to double.MaxValue in C#)
double_MaxValue = sys.float_info.max

primalGraph = {} 
 
#Create Primal Graph
lineGeometry = Array[CWLine](map(lambda s: CWLine(s), LineGeometry))

graphElements, edgeLengths = GeometryToGraphElements.GetNodesAndEdgesFromLines(lineGeometry)

primalGraph = CPrimalDirectedGraph(graphElements)
primalGraph.AddWeightMatrix(edgeLengths)    # index 0
primalGraph.AddEmptyWeightMatrix(double_MaxValue)          # index 1  
primalGraph.AddEmptyWeightMatrix(double_MaxValue)          # index 2  

for i in range(len(primalGraph.UndirectedEdges)):
    n1 = primalGraph.UndirectedEdges[i][0]  # start node of edge #i
    n2 = primalGraph.UndirectedEdges[i][1]  # end node of edge #i
 
    
	
    if EdgeWeightsForward[i] <= 0:
        EdgeWeightsForward[i] = 0.00001	
    if EdgeWeightsBackward[i] <= 0:
        EdgeWeightsBackward[i] = 0.00001
    if EdgeWeightsForward2[i] <= 0:
        EdgeWeightsForward2[i] = 0.00001	
    if EdgeWeightsBackward2[i] <= 0:
        EdgeWeightsBackward2[i] = 0.00001

    weight_matrix_id = 1
    primalGraph.SetWeightMatrixAndEdgeValue(EdgeWeightsForward[i], n1, n2, weight_matrix_id)  # forward direction
    primalGraph.SetWeightMatrixAndEdgeValue(EdgeWeightsBackward[i], n2, n1, weight_matrix_id)  # backward direction 

    weight_matrix_id = 2
    primalGraph.SetWeightMatrixAndEdgeValue(EdgeWeightsForward[i], n1, n2, weight_matrix_id)  # forward direction 2
    primalGraph.SetWeightMatrixAndEdgeValue(EdgeWeightsBackward[i], n2, n1, weight_matrix_id)  # backward direction 2 

if UseFilterMatrix:
  primalGraph.APShortestPathsByManyWeights(WeightMatrixIndexMain, WeightMatrixIndexFilter, GPU, 0.000001);
else:
  primalGraph.APShortestPathsByOneWeight(WeightMatrixIndexMain, GPU);
 
# If graph has more than 1 weight matrix, calculate distances along shortest paths according to all other weights
if CalculateAllMatrices:
    # Select which weights are needed to measure shortest paths
    # By default, all other matrices which are not the main are selected
    allIds = list(range(primalGraph.WeightMatricesCount))
    otherMatricesIds = [i for i in allIds if i != WeightMatrixIndexMain]
    primalGraph.FillWeightMatrixBySPRestore(Array[int](otherMatricesIds), GPU)
    
PrimalDirGraph = primalGraph    
