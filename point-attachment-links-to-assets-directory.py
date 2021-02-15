# coding=utf-8

from helper_routines import checkPath
from helper_routines import getNotesFileNames

import sys
import codecs
import re
import os

notesPath = sys.argv[1]
checkPath(notesPath)

NOTES_ABSOLUTE_PATH = "file://" + os.path.abspath(notesPath) + "/"
ASSETS_ABSOLUTE_PATH = NOTES_ABSOLUTE_PATH + "assets/"

notesFileNames = getNotesFileNames(notesPath)

print(notesFileNames)

for noteFileName in notesFileNames:
    noteFilePath = notesPath + noteFileName
    try:
        #print(noteFilePath)
        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()

            data_new = data.replace("]("+ NOTES_ABSOLUTE_PATH, "]("+ NOTES_ABSOLUTE_PATH + "assets/")
            data_new = data_new.replace("![](", "![](assets/")


            if data_new != data:
                with codecs.open(noteFilePath, 'w', encoding='utf-8') as fileW:
                    print(noteFilePath)
                    fileW.write(data_new)
                    fileW.close()
                    #raw_input("Press Enter to continue...")
    except Exception, e:
        print("ERROR: " + str(e) )
