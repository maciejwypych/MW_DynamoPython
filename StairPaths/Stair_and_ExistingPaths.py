import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#Import DocumentManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

#Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk

#Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
from Autodesk.Revit.DB import *
from Autodesk.Revit.Creation import *
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

views = UnwrapElement(IN[0])
doc = DocumentManager.Instance.CurrentDBDocument
stairswithpathlst = list()
stairslst = list()

# collect existing stairpaths in ActiveView
for v in views:
	collpath = FilteredElementCollector(doc, v.Id)
	filtpath = ElementCategoryFilter(BuiltInCategory.OST_StairsPaths)
	stairpaths = collpath.WherePasses(filtpath).ToElements()
	stairswithpath = []
	# get stairs from stair path
	for i in stairpaths:
		hoststair = (i.StairsId)
		stairid	= hoststair.HostElementId
		stairelem = doc.GetElement(stairid).ToDSType(True)	
		stairswithpath.append(stairelem)
		
	# collect stairs in ActiveView
	collstair = FilteredElementCollector(doc, v.Id)
	filtstair = ElementCategoryFilter(BuiltInCategory.OST_Stairs)
	stairs = collstair.WherePasses(filtstair).ToElements()
	
	stairswithpathlst.append(stairswithpath)
	stairslst.append(stairs)

OUT = stairslst, stairswithpathlst