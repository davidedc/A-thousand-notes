# coding=utf-8

from helper_routines import creation_date
from helper_routines import modification_date
from helper_routines import access_date
from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import stripEmptyTailLines
from helper_routines import wrapNoteInTagLineAndFooter

import sys
import os
import codecs
from datetime import datetime
import math


import argparse
import time


parser = argparse.ArgumentParser(description="My parser")
parser.add_argument('path')
parser.add_argument('-f', '--fix-note', action='store_true')
args = parser.parse_args()

notesPath = os.path.join(args.path, '') # add trailing slash if it's not there
checkPath(notesPath)

notesFileNames = getNotesFileNames(notesPath)


for noteFileName in notesFileNames:
    noteFilePath = notesPath + noteFileName

    wrapNoteInTagLineAndFooter(args.fix_note, noteFilePath)
