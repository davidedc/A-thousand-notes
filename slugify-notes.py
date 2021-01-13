# coding=utf-8

from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import wordSubstitutions
from helper_routines import bearEscapeDirectoryName
from helper_routines import quotePathForShell


from slugify import slugify

import sys
import codecs
import re
import string

from subprocess import call

def mySlugify(input):
    input = slugify(input, stopwords=['the','The','a','A','an','An'], lowercase=False)
    input = re.sub("http-www-", "", input, flags=re.IGNORECASE)
    input = re.sub("https-www-", "", input, flags=re.IGNORECASE)
    input = re.sub("www-", "", input, flags=re.IGNORECASE)
    return re.sub("node-js", "nodejs", input, flags=re.IGNORECASE)


CHANGE_FILES_AND_DIRS = True

NOTES_ABSOLUTE_PATH = "file:///Users/davidedellacasa/Public/10000notes/"
ASSETS_ABSOLUTE_PATH = NOTES_ABSOLUTE_PATH + "assets/"


notesPath = sys.argv[1]
checkPath(notesPath)

notesFileNames = getNotesFileNames(notesPath)
newNotesFilesNames = []


# FOR THE TIME BEING THE FILES ARE NOT CHANGED
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

        if  noteFileName_noExtension == mySlugify(noteTitle_substituted):
            print("  FILE NAME IS OK " + mySlugify(noteTitle_substituted))
        else:
            trailingDigits_re = re.compile("([\d ]*)$")
            trailingDigitsResults = trailingDigits_re.search(noteFileName_noExtension_substituted)
            trailingDigits = trailingDigitsResults.group(1)

            newFileName = mySlugify(noteTitle_substituted + trailingDigits)

            # FOR THE TIME BEING THE FILES ARE NOT CHANGED
            #notesFileNames = getNotesFileNames(notesPath)

            newFileNameInPreviousFileNames = (newFileName + ".md") in notesFileNames
            newFileNameInNewFileNames = newFileName in newNotesFilesNames

            if newFileNameInPreviousFileNames or newFileNameInNewFileNames:
                newFileName = ""
                if newFileNameInPreviousFileNames:
                    print("  COLLISION ✗ EVEN WITH TRAILING DIGITS with existing file names")

                if newFileNameInNewFileNames:
                    print("  COLLISION ✗ EVEN WITH TRAILING DIGITS with NEW file names")
            else:
                print("    COLLISION ✓ SORTED BY ADDING TRAILING DIGITS: " + newFileName)
            
            if newFileName != "":
                newNotesFilesNames.append(newFileName)

            if newFileName != "":
                noteFileName_noExtension_bearEscaped = bearEscapeDirectoryName(noteFileName_noExtension)
                NEWnoteFileName_noExtension_bearEscaped = bearEscapeDirectoryName(newFileName)

                with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
                    data = file.read()
                    data_lower = data.lower()
                    file.close()


                    data_new = data.replace("]("+ ASSETS_ABSOLUTE_PATH + noteFileName_noExtension_bearEscaped + "/", "]("+ ASSETS_ABSOLUTE_PATH + NEWnoteFileName_noExtension_bearEscaped + "/")
                    data_new = data_new.replace("](assets/" + noteFileName_noExtension_bearEscaped + "/", "](assets/" + NEWnoteFileName_noExtension_bearEscaped + "/")

                    if data_new != data:
                        #print(data_new)
                        if CHANGE_FILES_AND_DIRS:
                            with codecs.open(noteFilePath, 'w', encoding='utf-8') as fileW:
                                print(noteFilePath)
                                fileW.write(data_new)
                                fileW.close()

                command = 'mv ' + quotePathForShell(notesPath + "assets/" + noteFileName_noExtension) + " " + quotePathForShell(notesPath + "assets/" + newFileName)
                print("          " + command)
                if CHANGE_FILES_AND_DIRS:
                    call(command, shell=True)

                command = 'mv ' + quotePathForShell(notesPath + noteFileName) + " " + quotePathForShell(notesPath + newFileName + ".md")
                print("          " + command)
                if CHANGE_FILES_AND_DIRS:
                    call(command, shell=True)

                #raw_input("Press Enter to continue...")




        if slugFromNoteFileName_noExtension_substituted_stem == slugFromNoteTitle_substituted_stem:
            print("  " + mySlugify(noteFileName_noExtension_substituted))
        else:
            print("  ### " + noteFileName_noExtension)
            print("  ###   " + mySlugify(noteFileName_noExtension_substituted))
            print("  ###   " + mySlugify(noteTitle_substituted))

    except Exception, e:
        print("ERROR: " + str(e) )
