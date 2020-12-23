# coding=utf-8

from helper_routines import checkPath
from helper_routines import getListOfFiles

import sys
import codecs

notesPath = sys.argv[1]
checkPath(notesPath)

listOfFiles = getListOfFiles(notesPath)

print(listOfFiles)

for eachFile in listOfFiles:
    tryingToFindTheMdFile = notesPath + eachFile
    try:
        #print(tryingToFindTheMdFile)
        with codecs.open(tryingToFindTheMdFile, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()

            data = data.replace(u"![](",u"![](assets/")

            with codecs.open(tryingToFindTheMdFile, 'w', encoding='utf-8') as fileW:
                print(tryingToFindTheMdFile)
                fileW.write(data)
                fileW.close()
                #raw_input("Press Enter to continue...")
    except:
        print("EXCEPTION")
