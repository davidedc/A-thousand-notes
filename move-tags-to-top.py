# coding=utf-8

from helper_routines import creation_date
from helper_routines import modification_date
from helper_routines import access_date

import sys
import os
import glob
import ntpath
import codecs
import platform
from datetime import datetime
import math


fn = sys.argv[1]
if not os.path.exists(fn):
    exit("no such path")

fse = sys.getfilesystemencoding()


#print listOfDirectories

listOfFiles = [unicode(ntpath.basename(x), fse) for x in glob.glob(os.path.normpath(fn) + "/*.md")]


for eachFile in listOfFiles:
    tryingToFindTheMdFile = fn + eachFile
    try:
        #print(tryingToFindTheMdFile)
        with codecs.open(tryingToFindTheMdFile, 'r', encoding='utf-8') as file:

            lines = file.read().splitlines()
            file.close()

            while lines[-1].strip() == "":
              del lines[-1]

            tag_line = lines[-1]

            if tag_line.find("#fromEvernote") == -1:
                print eachFile + " > " + tag_line
            else:
              del lines[-1]
              lines.insert(0, "tags: " + tag_line)

            #print(tryingToFindTheMdFile + " > " + tag_line)
            theCreationDate = math.floor(creation_date(tryingToFindTheMdFile))
            theModificationDate = math.floor(modification_date(tryingToFindTheMdFile))
            theAccessDate = math.floor(access_date(tryingToFindTheMdFile))
            #print("     created: "  + str(theCreationDate) + " modified: " + str(theModificationDate))
            #print("     created: "  + str(datetime.utcfromtimestamp(theCreationDate)) + " modified: " + str(datetime.utcfromtimestamp(theModificationDate)))

            lines.insert(-1, "")
            lines.insert(-1, "___")
            lines.insert(-1, "created: "  + str(datetime.utcfromtimestamp(theCreationDate)) + " modified: " + str(datetime.utcfromtimestamp(theModificationDate)))

            with codecs.open(tryingToFindTheMdFile, 'w', encoding='utf-8') as fileW:
                fileW.write("\n".join(lines))
                fileW.close()
                os.utime(tryingToFindTheMdFile,(theAccessDate, theModificationDate))

    except Exception, e:
        print("EXCEPTION" + str(e) )
