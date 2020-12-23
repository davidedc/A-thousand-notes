# coding=utf-8

from helper_routines import checkPath
from helper_routines import getNotesFileNames

import sys
import codecs

notesPath = sys.argv[1]
checkPath(notesPath)

notesFileNames = getNotesFileNames(notesPath)

print(notesFileNames)

for noteFileName in notesFileNames:
    noteFilePath = notesPath + noteFileName
    try:
        #print(noteFilePath)
        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()

            data = data.replace(u"![](",u"![](assets/")

            with codecs.open(noteFilePath, 'w', encoding='utf-8') as fileW:
                print(noteFilePath)
                fileW.write(data)
                fileW.close()
                #raw_input("Press Enter to continue...")
    except Exception, e:
        print("ERROR: " + str(e) )
