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
from System.Collections.Generic import List

isovist = CIsovist(
  List[rg.Point3d](VP) ,
  List[rg.Mesh](OS),
  List[rg.Mesh](GS),
  List[rg.Vector3d](VD), 
  VR, HVA,
  VVA,
  HPr, VPr, VAO);

if OHP:
    HitPoints = isovist.hits

MeshIdsPerRay = isovist.surfaceToRaysList
NumberOfRays = isovist.NumberOfRaysPerPoint
    
 