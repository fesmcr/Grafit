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

   
 
n = Graph.NodesCount 

# Create a list of lists to represent the jagged array
odwmtmp = [[0.0] * n for _ in range(n)]

# Convert the list of lists to a jagged array
odwm = Array[Array[float]]([Array[float](row) for row in odwmtmp])

fc = range(len(From))
tc = range(len(To))

if(len(From) == 0): 
	fc = range(n)
	From = list(fc)
	
if(len(To) == 0):
	tc = range(n) 
	To = list(tc)

for i in fc:
    for j in tc:
        odwm[From[i]][To[j]] = ODWeightMatrixReduced[i, j]
		


measurement = CMeasure(Graph)

EdgeGroupsList = [] 

for i in range(EdgeGroups.BranchCount):
    EdgeGroupsList.append(List[int](EdgeGroups.Branches[i]))

BCGroup = measurement.CalculateBCGroup(odwm, List[List[int]](EdgeGroupsList))
 


 
 