import sys
import os
import shutil

f = open("List_of_path_to_thumbnails.txt", "r")
destination = r'c:\temp\\Thumbnail_Folder'


try:
    A = f.readlines()
    for lines in A:
        #print(lines, "AOF")
        lines = lines[1:-2]
        path = lines.strip('/')
        newfilename = os.path.join(destination, path[45:53] + ".png")
        print("Copying...", lines, "to...", newfilename)
        # shutil.copy(lines,newfilename)
        #print("Copied...", lines, "to...", newfilename)
except IOError:
    print("File Read Error")

print("Python script ended here")
