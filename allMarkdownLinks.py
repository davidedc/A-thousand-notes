# coding=utf-8

from helper_routines import checkPath
from helper_routines import getNotesFileNames

import sys
import codecs
import re


notesPath = sys.argv[1]
checkPath(notesPath)

notesFileNames = getNotesFileNames(notesPath)


for noteFileName in notesFileNames:
    noteFilePath = notesPath + noteFileName
    try:
        #print(noteFilePath)
        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()


            #print (noteFileName)
            for match in re.finditer('\[([^\]]*)\]\(([^\)]+)\)', data):

                countOpenBrackets = match.group(1).count('[')
                countClosedBrackets = match.group(1).count(']')

                countOpenParens = match.group(2).count('(')
                countClosedParens = match.group(2).count(')')

                if (countOpenBrackets != countClosedBrackets) or (countOpenParens != countClosedParens):
                    print (noteFileName)
                    print ("  " + match.group(1) + " " + match.group(2))

    except Exception, e:
        print("ERROR: " + str(e) )
