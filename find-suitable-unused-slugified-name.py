# coding=utf-8
# Example:
#    python find-suitable-unused-slugified-name.py download-google-images/downloads/Eric\ Owen\ Moss.md -v ../../Davide/notes-vault/

from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import wordSubstitutions
from helper_routines import bearEscapeDirectoryName
from helper_routines import quotePathForShell
from helper_routines import sanitizeFileName
from helper_routines import changeNoteNameAssetDirNameAndAssetsLinks
from helper_routines import mySlugify

import sys
import codecs
import re
import string


import argparse
from argparse import RawTextHelpFormatter

import ntpath
import os


parser = argparse.ArgumentParser(description="slugifies note file names starting from the note title.\n\nExamples:\npython slugify-notes.py ../../../Public/10000notes/\npython slugify-notes.py -f ../../../Public/10000notes/", formatter_class=RawTextHelpFormatter)
parser.add_argument('path', help="note's path")
parser.add_argument('-v', '--vault-path', help="TODO THIS HELP")
args = parser.parse_args()

notesPath = os.path.join(args.vault_path, '') # add trailing slash if it's not there
checkPath(notesPath)

notesFileNames = getNotesFileNames(notesPath)
notesFileNames_lower = [x.lower() for x in notesFileNames]

fse = sys.getfilesystemencoding()

noteName = unicode(ntpath.basename(args.path), fse)
#noteName = "untitled.md"

slugifiedFileNameWithoutExtension = mySlugify(noteName[:-3])
slugFromNoteFileName = slugifiedFileNameWithoutExtension + ".md"

#print(notesFileNames_lower)
#print(slugFromNoteFileName)

if slugFromNoteFileName.lower() not in notesFileNames_lower:
    print("good!")
else:
    tryAddingThisNumberToEnd = 2
    while (slugifiedFileNameWithoutExtension + "-"+ str(tryAddingThisNumberToEnd) + ".md").lower() in notesFileNames_lower:
        tryAddingThisNumberToEnd = tryAddingThisNumberToEnd + 1
    print("new name: " + (slugifiedFileNameWithoutExtension + "-"+ str(tryAddingThisNumberToEnd) + ".md") )

