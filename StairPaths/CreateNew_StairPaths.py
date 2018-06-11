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

import sys
#Specify location path for IronPython install
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)


doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def UnwrapNestedList(e):
	return UnwrapElement(e)
	
if isinstance(IN[0], list):
	stairs = ProcessList(UnwrapNestedList, IN[0])
else:
	stairs = [UnwrapElement(IN[0])]
if isinstance(IN[1], list):
	views = ProcessList(UnwrapNestedList, IN[1])
else:
	views = [UnwrapElement(IN[1])]	

typelist = list()

newpathslst = list()
TransactionManager.Instance.EnsureInTransaction(doc)


#find stairpathtype
collpathtype = FilteredElementCollector(doc)
filtpathtype = ElementCategoryFilter(BuiltInCategory.OST_StairsPaths)
stairpathtypes = collpathtype.WherePasses(filtpathtype).ToElements()

for stairpathtype in stairpathtypes:
	istype = stairpathtype.ToString()
	if istype == "Autodesk.Revit.DB.Architecture.StairsPathType":
		typelist.append(stairpathtype)

stairpathtype = typelist[0]
pathid = stairpathtype.Id

for v in views:
#create stair path for stair runs
	try:
		for st in stairs:
			newpaths = list()
			for stair in st:
				stairid = LinkElementId(stair.Id)
				newpath = Autodesk.Revit.DB.Architecture.StairsPath.Create(doc, stairid, pathid, v.Id)
				newpaths.append(newpath)
		newpathslst.append(newpaths)
	except:
		import traceback
		errorReport = traceback.format_exc()

TransactionManager.Instance.TransactionTaskDone()

doc.Regenerate()
uidoc.RefreshActiveView()

OUT = newpaths