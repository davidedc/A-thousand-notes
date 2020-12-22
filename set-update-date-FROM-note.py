# coding=utf-8

import sys
import os
import glob
import ntpath
import codecs
import platform
from datetime import datetime
import math
import dateutil.parser
import time
from subprocess import call


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def modification_date(path_to_file):
    return os.path.getmtime(path_to_file)

def access_date(path_to_file):
    return os.path.getatime(path_to_file)


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
