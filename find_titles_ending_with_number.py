# coding=utf-8

from helper_routines import creation_date
from helper_routines import modification_date
from helper_routines import access_date
from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import stripEmptyTailLines

import sys
import os
import codecs
from datetime import datetime
import math
import re


notesPath = sys.argv[1]
checkPath(notesPath)

notesFileNames = getNotesFileNames(notesPath)


for noteFileName in notesFileNames:
    noteFilePath = notesPath + noteFileName
    try:
        #print(noteFilePath)
        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:

            lines = file.read().splitlines()
            file.close()

            tag_line = lines[1]


            m = re.search(r'\d$', tag_line)
            # if the string ends in digits m will be a Match object, or None otherwise.
            if m is not None:
                print noteFileName + " title: >" + tag_line + "<"


    except Exception, e:
        print("ERROR: " + str(e) )
