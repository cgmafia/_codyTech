#Accessing a text file
file = open("fy16.txt","r")
file2 = open("fy16_stringed.txt","r")
starter = '<string>\\IKEA.COM\3D-Model$\IKEAassetApprovedFY10\ '
ender = '</string>'

print(starter, ender)


for line in file:
  fields = []
  fields =(starter, line, ender)
  #print(fields)
  print(starter, line, ender)
  #file2.write(fields)

file.close()