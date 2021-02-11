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


parser = argparse.ArgumentParser(description="My parser")
parser.add_argument('path')
args = parser.parse_args()

notesPath = os.path.join(args.path, '') # add trailing slash if it's not there
checkPath(notesPath)

notesFileNames = getNotesFileNames(notesPath)


for noteFileName in notesFileNames:
    noteFilePath = notesPath + noteFileName
    try:
        #print(noteFilePath)
        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:

            lines = file.read().splitlines()
            file.close()

            stripEmptyTailLines(lines)

            tag_line = lines[-1]

            if tag_line.find("#fromEvernote") == -1:
                print "ERROR: there should be a tag line in " + noteFileName + " found instead: >" + tag_line + "<"
            else:
              del lines[-1]
              lines.insert(0, "tags: " + tag_line)

            #print(noteFilePath + " > " + tag_line)
            theCreationDate = math.floor(creation_date(noteFilePath))
            theModificationDate = math.floor(modification_date(noteFilePath))
            theAccessDate = math.floor(access_date(noteFilePath))
            #print("     created: "  + str(theCreationDate) + " modified: " + str(theModificationDate))
            #print("     created: "  + str(datetime.utcfromtimestamp(theCreationDate)) + " modified: " + str(datetime.utcfromtimestamp(theModificationDate)))

            lines.insert(-1, "")
            lines.insert(-1, "___")
            lines.insert(-1, "created: "  + str(datetime.utcfromtimestamp(theCreationDate)) + " modified: " + str(datetime.utcfromtimestamp(theModificationDate)))

            with codecs.open(noteFilePath, 'w', encoding='utf-8') as fileW:
                fileW.write("\n".join(lines))
                fileW.close()
                os.utime(noteFilePath,(theAccessDate, theModificationDate))

    except Exception, e:
        print("ERROR: " + str(e) )
