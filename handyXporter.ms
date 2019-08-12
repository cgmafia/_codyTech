rollout handyXploder "Handy Exploder" width:220 height:500
(
    edittext prefix_txt "Name prefix:" fieldWidth:200 labelOnTop:true
    edittext path_txt "rootPath:" fieldWidth:200 labelOnTop:true
    button 'btn1' "Detach as object" pos:[15,120] width:150 height:25
    button 'btn2' "Batch Xport" pos:[15,160] width:150 height:25
    button 'btn3' "Batch Show" pos:[15,190] width:150 height:25
	
	
	on btn1 pressed  do
	(
	$.EditablePoly.detachToElement #Face keepOriginal:off
	$Object01.name = prefix_txt.text+"_P00_S00_NV00_PQPM0100"
	messageBox "Pressed Subobjects selection"
    )
    

	on btn2 pressed  do
	(
    makeDir @"c:\temp\workingDir" all:true
    dir= "c:\temp\workingDir"   -- the target directory
    typ=".max"      -- change this to the filetype you want
    sel=selection as array
     for s in sel do
     (
         f=dir+s.name+typ
         if typ==".max" then
         (
             saveNodes s f quiet:true
         ) else
         (
            select s
            exportfile f selectedOnly:true --#noprompt
         )
     )
     messageBox "Task Done Xporter"
    )
	
	
	on btn3 pressed  do
	(
	messageBox "Batch Job Testing"
    )

createDialog handyXploder