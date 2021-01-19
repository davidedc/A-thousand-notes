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
            for match in re.finditer('\[([^\n\]]*)\]\(([^\n\)]+)\)', data):

                countOpenBrackets = match.group(1).count('[')
                countClosedBrackets = match.group(1).count(']')

                countOpenParens = match.group(2).count('(')
                countClosedParens = match.group(2).count(')')

                if (countOpenBrackets != countClosedBrackets) and (countOpenParens == countClosedParens):

                    for match2 in re.finditer('\[(' + re.escape(match.group(1)) + '\][^\n\]]*)\]\(([^\n\)]+)\)', data):

                        countOpenBrackets2 = match2.group(1).count('[')
                        countClosedBrackets2 = match2.group(1).count(']')

                        countOpenParens2 = match2.group(2).count('(')
                        countClosedParens2 = match2.group(2).count(')')

                        if (countOpenBrackets2 != countClosedBrackets2) or (countOpenParens2 != countClosedParens2):
                            print ("1 " + match.group(0))
                            print ("1 " + match.group(1) + " ## " + match.group(2))
                            print ("1   " + match2.group(1) + " ## " + match2.group(2))

                if (countOpenBrackets == countClosedBrackets) and (countOpenParens != countClosedParens):

                    for match2 in re.finditer('\[([^\n\]]*)\]\(([^\n\)]*\)[^\n\)]*)\)', data):

                        countOpenBrackets2 = match2.group(1).count('[')
                        countClosedBrackets2 = match2.group(1).count(']')

                        countOpenParens2 = match2.group(2).count('(')
                        countClosedParens2 = match2.group(2).count(')')

                        if (countOpenBrackets2 != countClosedBrackets2) or (countOpenParens2 != countClosedParens2):
                            print ("2  " + match2.group(1) + " ## " + match2.group(2))

                if (countOpenBrackets != countClosedBrackets) and (countOpenParens != countClosedParens):
                    for match2 in re.finditer('\[([^\n\]]*\][^\n\]]*)\]\(([^\n\)]*\)[^\n\)]*)\)', data):

                        countOpenBrackets2 = match2.group(1).count('[')
                        countClosedBrackets2 = match2.group(1).count(']')

                        countOpenParens2 = match2.group(2).count('(')
                        countClosedParens2 = match2.group(2).count(')')

                        if (countOpenBrackets2 != countClosedBrackets2) or (countOpenParens2 != countClosedParens2):
                            print ("3  " + match2.group(1) + " ## " + match2.group(2))


    except Exception, e:
        print("ERROR: " + str(e) )
