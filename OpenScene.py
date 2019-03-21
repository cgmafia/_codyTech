import os
import sys
from pymxs import runtime as rt
from ArticleManager import get_article_path

# Change this path to the MONTERA working folder.
# Production path
# montera_root = r'\\ITSEELM-NT0030.IKEA.COM\Common_I\ICOM-3D-MODEL-PARTS-A\Montera\working'
# Testing path
montera_root = r'\\ITSEELM-NT0030.ikea.com\Common_I\ICOM-3D-MODEL-PARTS-A\Montera\working'

def parse_name(article_number):
    split_article = article_number.split('-')
    part_info = ''
    if len(split_article) > 1:
        part_info = split_article[1]
        article_number = split_article[0]

    # If the object is a part, name the file appropriately.
    print 'Article: {}'.format(article_number)

    return article_number, part_info


def main(article_number):
    ''' Creates a 3ds Max scene and references the supplied articles into it.
    '''
    if article_number == None or article_number == '':
        print 'Empty text box.'
        return

    print 'Parsing file name...'
    article_number, part_info = parse_name(article_number)

    if part_info:
        print 'Part info: {}'.format(part_info)
        montera_file = '{}-{}_Montera.max'.format(article_number, part_info)
    else:
        montera_file = '{}_Montera.max'.format(article_number)

    montera_path = os.path.join(montera_root, article_number)
    print 'Path: {}'.format(montera_path)

    try:
        if part_info:
            print 'Model path: {}'.format(get_article_path(article_number, part_info)[1])
            path_0100, path_5000 = get_article_path(article_number, part_info)
        else:
            print 'Model path: {}'.format(get_article_path(article_number, part_info)[1])
            path_0100, path_5000 = get_article_path(article_number)
    except:
        print 'Invalid article number: {}'.format(article_number)
        return

    # If the file already exists, return.
    if os.path.isdir(montera_path):
        if os.path.isfile(os.path.join(montera_path, montera_file)):
            print 'Montera file exists: {}'.format(montera_file)
            print 'Opening file...'
            rt.loadMaxFile(os.path.join(montera_path, montera_file))
            return
    else:
        os.mkdir(montera_path)
        
    rt.resetMaxFile()

    print 'Creating new file...'

    # Reference the high resolution file and rename the geometry to prevent conflicts.
    reference = rt.objXRefMgr.AddXrefItemsFromFile(path_5000)
    
    for geo in rt.Geometry:
        geo.Name = 'PQPM5000'
        geo.pos = rt.Point3(0,0,0)

    rt.saveMaxFile(os.path.join(montera_path, montera_file))

    print '... created the following scene: {}'.format(os.path.join(montera_root, article_number, montera_file))
