# coding=utf-8

from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import bearUnescapeDirectoryName

import sys
import codecs
import re

import os

import argparse


parser = argparse.ArgumentParser(description="My parser")
parser.add_argument('-p','--path')
args = parser.parse_args()

notesPath = args.path
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
            for match in re.finditer('\[([^\n\]]*)\]\(file://([^\n\)]+)\)', data):
                countOpenBrackets = match.group(1).count('[')
                countClosedBrackets = match.group(1).count(']')

                countOpenParens = match.group(2).count('(')
                countClosedParens = match.group(2).count(')')

                if (countOpenBrackets == countClosedBrackets) and (countOpenParens == countClosedParens):
                    print (noteFileName)
                    print ("  " + match.group(1) + " ## " + match.group(2))
                    if not os.path.exists(bearUnescapeDirectoryName(match.group(2))):
                        print ("  ERROR: DIR OR ASSET DOESN'T EXIST ")

                if (countOpenBrackets != countClosedBrackets):
                    print (noteFileName)
                    print ("  ERROR: MISMBRACKETS " + match.group(1) + " ## " + match.group(2))
                if (countOpenParens != countClosedParens):
                    #print (noteFileName)
                    #print ("  MISMPARENSES " + match.group(1) + " ## " + match.group(2))

                    for match2 in re.finditer('\[(' + re.escape(match.group(1)) + ')\]\(file://([^\n\)]*\)[^\n\)]*)\)', data):

                        countOpenBrackets2 = match2.group(1).count('[')
                        countClosedBrackets2 = match2.group(1).count(']')

                        countOpenParens2 = match2.group(2).count('(')
                        countClosedParens2 = match2.group(2).count(')')

                        print (noteFileName)
                        if (countOpenBrackets2 != countClosedBrackets2) or (countOpenParens2 != countClosedParens2):
                            print ("  ERROR: MISMPARENSES " + match2.group(1) + " ## " + match2.group(2))
                        else:
                            print ("  " + match2.group(1) + " ## " + match2.group(2))
                            if not os.path.exists(bearUnescapeDirectoryName(match2.group(2))):
                                print ("  ERROR: DIR OR ASSET DOESN'T EXIST ")


            for match in re.finditer('\[([^\n\]]*)\]\((assets/[^\n\)]+)\)', data):
                countOpenBrackets = match.group(1).count('[')
                countClosedBrackets = match.group(1).count(']')

                countOpenParens = match.group(2).count('(')
                countClosedParens = match.group(2).count(')')

                if (countOpenBrackets == countClosedBrackets) and (countOpenParens == countClosedParens):
                    print (noteFileName)
                    print ("  " + match.group(1) + " ## " + match.group(2))
                    if not os.path.exists(notesPath + bearUnescapeDirectoryName(match.group(2))):
                        print ("  ERROR: DIR OR ASSET DOESN'T EXIST ")
                        print ("    " + (notesPath + bearUnescapeDirectoryName(match.group(2))))

                if (countOpenBrackets != countClosedBrackets):
                    print (noteFileName)
                    print ("  ERROR: MISMBRACKETS " + match.group(1) + " ## " + match.group(2))
                if (countOpenParens != countClosedParens):
                    #print (noteFileName)
                    #print ("  MISMPARENSES " + match.group(1) + " ## " + match.group(2))

                    for match2 in re.finditer('\[(' + re.escape(match.group(1)) + ')\]\((assets/[^\n\)]*\)[^\n\)]*)\)', data):

                        countOpenBrackets2 = match2.group(1).count('[')
                        countClosedBrackets2 = match2.group(1).count(']')

                        countOpenParens2 = match2.group(2).count('(')
                        countClosedParens2 = match2.group(2).count(')')

                        print (noteFileName)
                        if (countOpenBrackets2 != countClosedBrackets2) or (countOpenParens2 != countClosedParens2):
                            print ("  ERROR: MISMPARENSES " + match2.group(1) + " ## " + match2.group(2))
                        else:
                            print ("  " + match2.group(1) + " ## " + match2.group(2))
                            if not os.path.exists(notesPath + bearUnescapeDirectoryName(match2.group(2))):
                                print ("  ERROR: DIR OR ASSET DOESN'T EXIST ")


    except Exception, e:
        print("ERROR: " + str(e) )

# some incorrect that could still be helpful
"""
if (countOpenBrackets == countClosedBrackets) and (countOpenParens != countClosedParens):
    for match2 in re.finditer('\[([^\n\]]*)\]\(([^\n\)]*\)[^\n\)]*)\)', data):

if (countOpenBrackets != countClosedBrackets) and (countOpenParens != countClosedParens):
    for match2 in re.finditer('\[([^\n\]]*\][^\n\]]*)\]\(([^\n\)]*\)[^\n\)]*)\)', data):
"""
