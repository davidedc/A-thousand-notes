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
args = parser.parse_args()

noteFileName = args.path
checkPath(noteFileName)

noteFilePath = noteFileName
try:
    #print(noteFilePath)
    with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:

        lines = file.read().splitlines()
        file.close()


        stripEmptyTailLines(lines)

        tag_line = lines[0]

        if tag_line.find("tags:") == -1:
          lines.insert(0, "tags: ")

        #print(noteFilePath + " > " + tag_line)
        theCreationDate = int(round(time.time()))
        theModificationDate = theCreationDate
        theAccessDate = theCreationDate

        last_line = lines[-1]
        if last_line.find("created: ") == -1:
            lines.append("")
            lines.append("___")
            lines.append("created: "  + str(datetime.utcfromtimestamp(theCreationDate)) + " modified: " + str(datetime.utcfromtimestamp(theModificationDate)))


        with codecs.open(noteFilePath, 'w', encoding='utf-8') as fileW:
            fileW.write("\n".join(lines))
            fileW.close()
            os.utime(noteFilePath,(theAccessDate, theModificationDate))

except Exception, e:
    print("ERROR: " + str(e) )


