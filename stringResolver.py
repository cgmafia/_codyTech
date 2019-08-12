
def ssplit(artNo)
	artno.split("_")
	article = artno[0]
	part = artno[1]
	return article, part

def main()
	c = input("Input the article string")
	ssplit(c)
	print("***END***")

main()
