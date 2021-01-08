try(destroydialog CameraCreatorDialog) catch()
rollout CameraCreatorDialog "Camera Creator" width:200
(	
	edittext cameraname_tx "Name:" text:cameraname fieldwidth:150 align:#right offset:[9,0]
	pickbutton chooseit "Select Surface" width:140
	pickbutton lookme "Camera Target" width:140
	button createcam_bt "Create Cameras" width:192 align:#right offset:[9,4]
	
	
	on cameraname_tx changed text do 
	(
		if (cam = getCamera()) != undefined do cam.name = text
		cameraname = text
	)
	
	on createcam_bt pressed do if (cam = getCamera()) == undefined do undo "Create Camera" on
	(
		
		theObj = chooseit
		targetLook = lookme

		convertTo theObj Editable_Poly

		theFacesToSelect = #{} 
		numFaces = polyOp.getNumFaces theObj

		cams = for x in numFaces do
		(
			polyOp.setFaceSelection  theObj #{x}
            tm = theObj #{x}
            name = node.name + "_" + cameraname
			c = TargetCamera name:cameraname target:(TargetObject name:(cameraname + ".Target")) transform:tm.transform parent:node isselected:on
		)
		select cams
	)
)
createdialog CameraCreatorDialog