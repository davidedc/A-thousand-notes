# coding=utf-8

from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import wordSubstitutions

from slugify import slugify

import sys
import codecs
import re
import string

def mySlugify(input):
    input = slugify(input, stopwords=['the','The','a','A','an','An'], lowercase=False)
    input = re.sub("http-www-", "", input, flags=re.IGNORECASE)
    input = re.sub("https-www-", "", input, flags=re.IGNORECASE)
    input = re.sub("www-", "", input, flags=re.IGNORECASE)
    return re.sub("node-js", "nodejs", input, flags=re.IGNORECASE)


NOTES_ABSOLUTE_PATH = "file:///Users/davidedellacasa/Public/10000notes/"


notesPath = sys.argv[1]
checkPath(notesPath)

notesFileNames = getNotesFileNames(notesPath)


for noteFileName in notesFileNames:

    noteFileName_noExtension = noteFileName[:-3]
    noteFilePath = notesPath + noteFileName

    try:
        #print(noteFilePath)
        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            file.close()

        print(noteFileName_noExtension)

        noteTitle = lines[1][2:]

        noteFileName_noExtension_substituted = wordSubstitutions(noteFileName_noExtension)
        noteTitle_substituted = wordSubstitutions(noteTitle)


        noteFileName_noExtension_substituted_stem = noteFileName_noExtension_substituted.rstrip().rstrip(string.digits).rstrip()
        noteTitle_substituted_stem = noteTitle_substituted.rstrip().rstrip(string.digits).rstrip()

        slugFromNoteFileName_noExtension_substituted_stem = mySlugify(noteFileName_noExtension_substituted_stem)
        slugFromNoteTitle_substituted_stem = mySlugify(noteTitle_substituted_stem)



        if slugFromNoteFileName_noExtension_substituted_stem == slugFromNoteTitle_substituted_stem:
            print("  " + mySlugify(noteFileName_noExtension_substituted))
        else:
            print("  ### " + noteFileName_noExtension)
            print("  ###   " + mySlugify(noteFileName_noExtension_substituted))
            print("  ###   " + mySlugify(noteTitle_substituted))

    except Exception, e:
        print("ERROR: " + str(e) )
