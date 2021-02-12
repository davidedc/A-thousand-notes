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

    #    _____________________________________
    #  / TODO this code should be factored-out \
    #  \ into the helper-routines file         /
    #    -------------------------------------
    #           \   ^__^ 
    #            \  (oo)\_______
    #               (__)\       )\/\
    #                   ||----w |
    #                   ||     ||

    try:
        #print(noteFilePath)
        needsTagLine = False
        needsFooter = False
        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:

            lines = file.read().splitlines()
            file.close()


            stripEmptyTailLines(lines)

            tag_line = lines[0]

            if tag_line.find("tags:") == -1:
              lines.insert(0, "tags: ")
              needsTagLine = True

            #print(noteFilePath + " > " + tag_line)
            theCreationDate = math.floor(creation_date(noteFilePath))
            theModificationDate = math.floor(modification_date(noteFilePath))
            theAccessDate = math.floor(access_date(noteFilePath))

            last_line = lines[-1]
            if last_line.find("created: ") == -1:
                lines.append("")
                lines.append("___")
                lines.append("created: "  + str(datetime.utcfromtimestamp(theCreationDate)) + " modified: " + str(datetime.utcfromtimestamp(theModificationDate)))
                needsFooter = True


            if args.fix_note and (needsTagLine or needsFooter):
                with codecs.open(noteFilePath, 'w', encoding='utf-8') as fileW:
                    fileW.write("\n".join(lines))
                    fileW.close()
                    os.utime(noteFilePath,(theAccessDate, theModificationDate))
            elif needsTagLine or needsFooter:
                print(noteFileName)

    except Exception, e:
        print("ERROR: " + str(e) )


