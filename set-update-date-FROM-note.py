# coding=utf-8

from helper_routines import creation_date
from helper_routines import modification_date
from helper_routines import access_date
from helper_routines import checkPath
from helper_routines import getListOfFiles

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

listOfFiles = getListOfFiles(notesPath)


for eachFile in listOfFiles:
    tryingToFindTheMdFile = notesPath + eachFile
    try:
        #print(tryingToFindTheMdFile)
        with codecs.open(tryingToFindTheMdFile, 'r', encoding='utf-8') as file:

            lines = file.read().splitlines()
            file.close()

            while lines[-1].strip() == "":
              del lines[-1]

            tag_line = lines[-1]

            if tag_line.find("created:") == -1:
                print eachFile + " > " + tag_line


            a = "created: 2019-12-21 19:06:19 modified: 2019-12-21 22:02:24"
            theSplit = tag_line.split(" ")
            #print(theSplit)
            modificationDateParsed = dateutil.parser.parse(theSplit[4]+" " + theSplit[5])
            #creationDateParsed = dateutil.parser.parse(theSplit[1]+" " + theSplit[2])
            #print(modificationDateParsed)
            theModificationDate = time.mktime(modificationDateParsed.timetuple())
            #print(theTime)
            #print(str(datetime.utcfromtimestamp(theTime)))

            theAccessDate = math.floor(access_date(tryingToFindTheMdFile))
            os.utime(tryingToFindTheMdFile,(theAccessDate, theModificationDate))

            theSplitCreationDate = theSplit[1].split("-")


            #command = 'SetFile -d ' + '"05/06/2019 "' + '00:00:00 ' + complete_path
            command = 'SetFile -d ' + '"' + theSplitCreationDate[1] + "/" + theSplitCreationDate[2] + "/" + theSplitCreationDate[0] + " " + theSplit[2] + '" "' + tryingToFindTheMdFile.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`') + '"'
            print(command)
            call(command, shell=True)


    except Exception, e:
        print("EXCEPTION" + str(e) )
