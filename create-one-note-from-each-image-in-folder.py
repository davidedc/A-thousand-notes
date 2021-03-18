# coding=utf-8

# Example:
#   python create-one-note-from-each-image-in-folder.py simple_images/bear/* -v downloads

import sys
import os
import ntpath
import codecs
import argparse

# enables to import from upper directory
# sys.path.insert(1, os.path.join(sys.path[0], '..'))

from helper_routines import checkPath
from helper_routines import getFileNames
from helper_routines import bearEscapeDirectoryName

from shutil import copyfile

parser = argparse.ArgumentParser(description="My parser")
parser.add_argument('imageFiles', nargs='+')
parser.add_argument('-v', '--vault-path')
args = parser.parse_args()

notesPath = os.path.join(args.vault_path, '') # add trailing slash if it's not there


fse = sys.getfilesystemencoding()

for f in args.imageFiles:
    print(f)

    eachImageFileName = unicode(ntpath.basename(os.path.normpath(f)), fse)
    if eachImageFileName == ".DS_Store":
        continue
    
    eachImageFileName_noExtension = os.path.splitext(eachImageFileName)[0]
    noteContents = "# " + eachImageFileName_noExtension + "\n\n![](assets/" + bearEscapeDirectoryName(eachImageFileName_noExtension) + "/" + bearEscapeDirectoryName(eachImageFileName) +")"

    with codecs.open(notesPath + eachImageFileName_noExtension + ".md", 'w', encoding='utf-8') as fileW:
        fileW.write(noteContents)
        fileW.close()

    imageDestinationPath = notesPath + "assets/" + eachImageFileName_noExtension
    os.mkdir(imageDestinationPath)
    copyfile(f, imageDestinationPath + "/" + eachImageFileName)

