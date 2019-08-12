import os

path = raw_input("Enter the path here (//root) :")
ext = raw_input("Enter the ext here (*.ext) :")
#path = "\\\\ITSEELM-NT0030.ikea.com\Common_I\ICOM-3D-MODEL-PARTS-A\Assemblies"
#ext = "json"
i = 1
for root, dirs, files in os.walk(path):
    print("Path: ", path)
    for file in files:
        if file.endswith(ext):
             print("File", i, os.path.join(root, file))
             i = i + 1
