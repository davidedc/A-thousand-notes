# coding=utf-8

# Example:
#   python create-note-around-images.py ./simple_images/Eric\ Owen\ Moss

import sys
import os
import ntpath
import codecs
import argparse

# enables to import from upper directory
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from helper_routines import checkPath
from helper_routines import getFileNames
from helper_routines import bearEscapeDirectoryName



parser = argparse.ArgumentParser(description="My parser")
parser.add_argument('path')
args = parser.parse_args()

imagesPath = os.path.join(args.path, '') # add trailing slash if it's not there
imageFiles = getFileNames(imagesPath)

fse = sys.getfilesystemencoding()
imagesDirectoryName = unicode(ntpath.basename(os.path.normpath(imagesPath)), fse)

#print(imagesDirectoryName)

noteContents = "# " + imagesDirectoryName +"\n"

for eachImageFile in imageFiles:

    if eachImageFile == ".DS_Store":
        continue
    noteContents = noteContents + "\n\n![](assets/" + bearEscapeDirectoryName(imagesDirectoryName) + "/" + bearEscapeDirectoryName(eachImageFile) +")"

with codecs.open(imagesDirectoryName + ".md", 'w', encoding='utf-8') as fileW:
    fileW.write(noteContents)
    fileW.close()
