import os
import filecmp

x = r"\\ITSEELM-NT0030.ikea.com\Common_I\ICOM-3D-MODEL-PARTS-A\Montera\database\geometry"
y = r"\\ITSEELM-NT0030.ikea.com\Common_I\ICOM-3D-MODEL-PARTS-A\Montera\database\assembly"


txt  = open("compare.txt", "w") 

o = os.listdir(x)
txt.write("Following files not in \n") 
txt.write(y)
txt.write("\n")
for i in os.listdir(x)[:21]:
	if i[:21] not in os.listdir(y)[:21]:
		txt.write(i[:21])
		txt.write("\n")

txt.write("\n")
txt.write("\n")
txt.write("\n")
txt.write("Following files not in \n") 
txt.write(x)
txt.write("\n")


for j in os.listdir(y)[:21]:
	if j[:21] not in os.listdir(x)[:21]:
		txt.write(j[:21])
		txt.write("\n")



txt.write("\n")
txt.write("###################xxxxxxxxxxxxx END OF FILE xxxxxxxxxxxxx#########################")
print("Successful")