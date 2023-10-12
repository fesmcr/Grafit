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
    
 