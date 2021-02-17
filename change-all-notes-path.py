# coding=utf-8

# Example:
# python change-all-notes-path.py /Users/davidedellacasa/Public/10000notes -n /Users/davidedellacasa/Desktop/Davide/notes-vault -f

from helper_routines import creation_date
from helper_routines import modification_date
from helper_routines import access_date
from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import stripEmptyTailLines
from helper_routines import changeNoteNameAssetDirNameAndAssetsLinks

import sys
import os
import codecs
from datetime import datetime
import math


import argparse
import time


parser = argparse.ArgumentParser(description="My parser")
parser.add_argument('path')
parser.add_argument('-f', '--fix-notes', action='store_true')
parser.add_argument('-n', '--new-path')
parser.add_argument('-v', '--verbose')
args = parser.parse_args()

notesOldPath = os.path.join(args.path, '') # add trailing slash if it's not there
checkPath(notesOldPath)

notesNewPath = os.path.join(args.new_path, '') # add trailing slash if it's not there
checkPath(notesNewPath)

notesFileNames = getNotesFileNames(notesOldPath)


for noteFileName in notesFileNames:
    noteFilePath = notesOldPath + noteFileName

    changeNoteNameAssetDirNameAndAssetsLinks(args.fix_notes, args.verbose, notesOldPath, noteFileName[:-3], noteFileName[:-3], notesNewPath)
