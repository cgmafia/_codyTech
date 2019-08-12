import sys
import os

root_dir = r'C:\Temp\Split_parts'
list_of_articles = os.listdir(root_dir)
# list_of_articles = [10324914BAG.max, 10324914Object001.max, 10324914Object002.max]
count = len(list_of_articles)

# navigating root dir
for a in list_of_articles:
    contents = os.listdir(os.path.join(root_dir, a))
    # navigating contents of article folder
    for c in contents:
        source = os.path.join(root_dir, a, c)
        destination = os.path.join(
            root_dir, a, a + "_" + c[-7:-4] + "_S00_NV00_PQPM0100.max")
        alt_destination = os.path.join(
            root_dir, a, a + "_" + c[-7:-4] + "_S00_NV00_PQPM0100_.max")
        print source, "  Renamed to  ", destination, " Successfully! "
        try:
            os.rename(source, destination)
        except WindowsError:
            os.rename(source, alt_destination)
