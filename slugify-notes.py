# coding=utf-8

from helper_routines import checkPath
from helper_routines import getNotesFileNames
from slugify import slugify

import sys
import codecs
import re
import string


NOTES_ABSOLUTE_PATH = "file:///Users/davidedellacasa/Public/10000notes/"


notesPath = sys.argv[1]
checkPath(notesPath)

notesFileNames = getNotesFileNames(notesPath)


for noteFileName in notesFileNames:
    noteFilePath = notesPath + noteFileName
    try:
        #print(noteFilePath)
        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            file.close()

        print(noteFileName[:-3])

        noteFileNameStem = noteFileName[:-3].rstrip().rstrip(string.digits).rstrip()
        noteTitleStem = lines[1][2:].rstrip().rstrip(string.digits).rstrip()

        slugFromNoteNameStem = slugify(noteFileNameStem, stopwords=['the'], lowercase=False)
        slugFromNoteTitleStem = slugify(noteTitleStem, stopwords=['the'], lowercase=False)

        if slugFromNoteNameStem == slugFromNoteTitleStem:
            print("  " + slugify(noteFileName[:-3], stopwords=['the'], lowercase=False))
        else:
            print("  ### " + slugify(noteFileName[:-3], stopwords=['the'], lowercase=False))
            print("  ### " + slugify(lines[1][2:], stopwords=['the'], lowercase=False))

    except Exception, e:
        print("ERROR: " + str(e) )
