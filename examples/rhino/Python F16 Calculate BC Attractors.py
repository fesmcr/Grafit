import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import sys
import clr

clr.AddReference("System.Core")
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
 
from System.Linq import *
from Grafit import *
from GrafitRhino import * 
from System import *
from System.Collections.Generic import List, Dictionary

from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML  
 
n = Graph.NodesCount 

# Create a list of lists to represent the jagged array
odwmtmp = [[0.0] * n for _ in range(n)]

# Convert the list of lists to a jagged array
odwm = Array[Array[float]]([Array[float](row) for row in odwmtmp])

fc = range(len(From))
tc = range(len(To))

# if From or To lists are empty, total number of nodes is used
if(len(From) == 0): 
	fc = range(n)
	From = list(fc)
	
if(len(To) == 0):
	tc = range(n) 
	To = list(tc)

for i in fc:
    for j in tc:
        odwm[From[i]][To[j]] = ODWeightMatrixReduced[i, j]
		
if(len(EdgeAttractorIds) != len(EdgeAttractorWeights)): 
	ghenv.Component.AddRuntimeMessage(RML.Error , "Length of EdgeAttractorIds and EdgeAttractorWeights lists should be the same")
	
# Create a list 0 weights for all undirected edges
EdgeAttractorWeightsList =  [0.0 for _ in range(Graph.UndirectedEdgesCount)]

# Set input edges to input weights
for i in range(len(EdgeAttractorIds)):
	EdgeAttractorWeightsList[EdgeAttractorIds[i]] = EdgeAttractorWeights[i]
	
measurement = CMeasure(Graph)

# Calculate BC With Attractors
measurement.CalculateBCWithAttractors(odwm, List[float](EdgeAttractorWeightsList)) 

# Init result BC list with 0
EdgeAttractorBCResults = [0.0 for _ in range(len(EdgeAttractorIds))]

# Output BC only for input Edge ids
for i in range(len(EdgeAttractorIds)):
	EdgeAttractorBCResults[i] = measurement.BCEdgesAttractors[EdgeAttractorIds[i]] 

BCAttractors = EdgeAttractorBCResults; 


 
 