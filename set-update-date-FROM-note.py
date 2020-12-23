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
import dateutil.parser
import time
from subprocess import call


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

            stripEmptyTailLines(lines)

            createdUpdated_line = lines[-1]

            if createdUpdated_line.find("created:") == -1:
                print "ERROR: there should be created: in " + noteFileName + " found instead: >" + createdUpdated_line + "<"
                print noteFileName + " > " + createdUpdated_line
            else:
                theSplit = createdUpdated_line.split(" ")
                #print(theSplit)
                modificationDateParsed = dateutil.parser.parse(theSplit[4]+" " + theSplit[5])
                #creationDateParsed = dateutil.parser.parse(theSplit[1]+" " + theSplit[2])
                #print(modificationDateParsed)
                theModificationDate = time.mktime(modificationDateParsed.timetuple())
                #print(theTime)
                #print(str(datetime.utcfromtimestamp(theTime)))

                theAccessDate = math.floor(access_date(noteFilePath))
                os.utime(noteFilePath,(theAccessDate, theModificationDate))

                theSplitCreationDate = theSplit[1].split("-")


                #command = 'SetFile -d ' + '"05/06/2019 "' + '00:00:00 ' + complete_path
                command = 'SetFile -d ' + '"' + theSplitCreationDate[1] + "/" + theSplitCreationDate[2] + "/" + theSplitCreationDate[0] + " " + theSplit[2] + '" "' + noteFilePath.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`') + '"'
                print(command)
                call(command, shell=True)


    except Exception, e:
        print("ERROR: " + str(e) )
