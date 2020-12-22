# coding=utf-8

import sys
import os
import glob
import ntpath
import codecs
import platform
from datetime import datetime
import math

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
