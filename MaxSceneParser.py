# Copyright (c) 2018 Trimble Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json
import hashlib
import MaxPlus
from pymxs import runtime as rt
from collections import OrderedDict

'''
	Exports Max scene graph as MatterMachine Assembly, Machine and Geometry assets.
	
	Montera must be installed on the local computer prior to running this script to create the needed resources file.
	
'''
import MaxMessageDialog
reload(MaxMessageDialog)

import ScriptResources
reload(ScriptResources)

import ArticleManager
reload(ArticleManager)

# settings
TEMP_DIR = MaxPlus.PathManager.GetTempDir().replace('\\', '/')

# globals
MaxGeoNodesToExport = []
Cache = {}
SnapLibrary = {}

def initialise():
	global MaxGeoNodesToExport
	global Cache
	global SnapLibrary
	
	MaxGeoNodesToExport = []
	Cache = {}
	SnapLibrary = {}

def initialiseScene():
	maxRoot = MaxPlus.Core.GetRootNode()
	# zero out local transform of all PQPM nodes:
	for node in maxRoot.Children:
		if node.Name.startswith("PQPM"):
			node.SetLocalTM(MaxPlus.Matrix3.GetIdentity())

def getNodeLocalTransformAsArray(n):
	resultM3 = n.LocalTransform

	# Each point3 object in the matrix3 == coordinate axis
	# Convert axis in rows to axis as columns in column major serialsised []
	row0 = [resultM3[0].X,resultM3[0].Y, resultM3[0].Z,0]
	row1 = [resultM3[1].X,resultM3[1].Y, resultM3[1].Z, 0]
	row2 = [resultM3[2].X, resultM3[2].Y, resultM3[2].Z, 0]
	row3 = [resultM3[3].X, resultM3[3].Y, resultM3[3].Z, 1]

	return row0 + row1 + row2 + row3

def fileToString(filePath):
	with open(filePath, 'r') as f:
		output = f.read()
	return output

def toPrettyJson(data):
	return json.dumps(data, indent=2, separators=(',', ': '))

def parseScene():
	initialise()
	maxNode = MaxPlus.Core.GetRootNode()
	global AssetDatabase
	global MaxGeoNodesToExport
	global Cache
	global geometryDatabaseID
	global SnapLibrary
	
	false = False
	true = True

	SnapLibrary = ScriptResources.getSnapLibrary()
	maxNodeName = maxNode.Name.upper()
	
	# Build name from filestructure
	file_name = os.path.splitext(rt.maxFileName)[0]
	split_name = file_name.split('-')

	# Different naming conventions for articles and parts.
	part_info = ''
	if len(split_name) > 1:
		part_info = '_'.join(split_name[1].split('_')[0:-1])
		article_number = split_name[0]
	else:
		article_number = split_name[0].split('_')[0]

	#article_number = split_name[0]
	print 'Article: {}'.format(article_number)
	if part_info:
		print 'Part info: {}'.format(part_info)

	try:
		if part_info:
			PQPM0100FileName, PQPM5000FileName = ArticleManager.get_article_path(article_number, part_info)
		else:
			PQPM0100FileName, PQPM5000FileName = ArticleManager.get_article_path(article_number)
	except:
		print 'Failed to get reference path.'

	
	# Get all nodes in the current scene
	preRefNodes = []
	for childNode in maxNode.Children:
		preRefNodes.append(childNode.Name)

	try:
		xrefPQPM0100 = rt.objXRefMgr.AddXrefItemsFromFile(PQPM0100FileName)
	except:
		print "Unable to find PQPM0100 version of .max file."
		return

	postRefNodes = []
	for childNode in maxNode.Children:
		postRefNodes.append(childNode.Name)
	
	# only execute export if the reference PQPM0100 model contains 1 node
	if len(postRefNodes) - len(preRefNodes) != 1:
		print "Reference PQPM0100 file contains more than one node. Exiting."
		rt.objXRefMgr.RemoveRecordFromScene(xrefPQPM0100)
		return
	else:
		currentAssemblyNode = {}
		currentAssemblyNode['name'] = '{}_{}'.format(article_number, part_info)
		currentAssemblyNode['transform'] = getNodeLocalTransformAsArray(maxNode)
		currentAssemblyNode['nodes'] = {}
		
		print "Exporting PQPM0100: "+ currentAssemblyNode['name']

		snaps = []
		for childNode in maxNode.Children:
			childNodeName = childNode.Name.upper()
			if childNode.Name not in preRefNodes:
				
				# make sure PQPM0100 node is visible (won't export otherwise)
				visiblityLayer = childNode.GetLayer()
				visiblityLayer.Hide(False)

				geoData = exportOBJ(childNode)

				# upgrade type from general 'group' to 'machine'
				currentAssemblyNode["transform"] = getNodeLocalTransformAsArray(maxNode)
				if part_info:
					asset_name = '{}-{}'.format(article_number, part_info)
				else:
					asset_name = article_number
				Cache = {
						"assetName": asset_name,
						"geo": geoData,
						}

			# -- 2.2 handle snaps --
			# if parent node of the current node
			
			snapHashWstr = MaxPlus.WStr()
			childNode.GetUserPropBuffer(snapHashWstr)
			snapHash = str(snapHashWstr)
			
			# if the node is a snap node add it to the snap array
			if snapHash in SnapLibrary.keys():
				snap = {"name": childNode.Name, "transform": getNodeLocalTransformAsArray(childNode), "hash": snapHash}
				snaps.append(snap)
			
		Cache["snaps"] = snaps
		
		maxAssetFile = PQPM5000FileName.split("\\")
		assetFileName = maxAssetFile[-1]
		del maxAssetFile[-1]
		assetDirectory  = '/'.join(maxAssetFile)
		
		Cache["assetDirectory"] = assetDirectory
		Cache["assetFileName"] = assetFileName

		print 'Asset directory: {}'.format(assetDirectory)
		print 'Asset filename: {}'.format(assetFileName)
		
		rt.objXRefMgr.RemoveRecordFromScene(xrefPQPM0100)
		
		return Cache


def exportOBJ(maxNode):
	nodeToExport = maxNode  # if the PQPM node holds the geometry (as opposed to its children)

	# Transform node to export to origin to make sure the OBJ is exported
	# as it is in local space (not its world transformed position).
	cTM = nodeToExport.GetWorldTM()
	idTM = MaxPlus.Matrix3.GetIdentity()
	nodeToExport.SetWorldTM(idTM)

	MaxPlus.SelectionManager.ClearNodeSelection()
	nodes = MaxPlus.INodeTab()
	nodes.Append(nodeToExport)
	MaxPlus.SelectionManager.SelectNodes(nodes)

	objName = TEMP_DIR + "/" + nodeToExport.Name + ".obj"

	rt.exportFile(objName , selectedOnly=True)

	header  = "# This OBJ was exported using MatterMachine Max-to-Assembly v1.0.0 export script.\n"
	header += "# Copyright MatterMachine www.mattermachine.com.\n\n"

	objContent = header + fileToString(objName)
	
	# remove temp file
	if os.path.exists(objName):
		os.remove(objName)

	# Transform back to original position/rotation.
	nodeToExport.SetWorldTM(cTM)

	return objContent

def main():
	parseScene()
			
if __name__ == '__main__':

	try:
		import MaxPlus
		MAX_ENVIRONMENT = True
	except Exception as e:
		MAX_ENVIRONMENT = False

	print "START"
	main()
	print "DONE"

	if not MAX_ENVIRONMENT:
		exit(0)
