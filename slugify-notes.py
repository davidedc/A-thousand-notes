# coding=utf-8

from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import wordSubstitutions
from helper_routines import bearEscapeDirectoryName
from helper_routines import quotePathForShell
from helper_routines import sanitizeFileName


from slugify import slugify

import sys
import codecs
import re
import string

from subprocess import call

import argparse

def mySlugify(input):
    input = slugify(input, stopwords=['the','The','a','A','an','An'], lowercase=False)
    input = re.sub("http-www-", "", input, flags=re.IGNORECASE)
    input = re.sub("https-www-", "", input, flags=re.IGNORECASE)
    input = re.sub("www-", "", input, flags=re.IGNORECASE)
    input = re.sub("(-and)+", "-and", input, flags=re.IGNORECASE)
    input = re.sub('sci-fi', 'scifi', input, flags=re.IGNORECASE)
    input = re.sub('t-shirt', 'tshirt', input, flags=re.IGNORECASE)
    return re.sub("node-js", "nodejs", input, flags=re.IGNORECASE)


NOTES_ABSOLUTE_PATH = "file:///Users/davidedellacasa/Public/10000notes/"
ASSETS_ABSOLUTE_PATH = NOTES_ABSOLUTE_PATH + "assets/"


parser = argparse.ArgumentParser(description="My parser")
parser.add_argument('-p','--path')
parser.add_argument('-f', '--fix-name-and-assets-links', action='store_true')
args = parser.parse_args()

notesPath = args.path
checkPath(notesPath)

notesFileNames = getNotesFileNames(notesPath)
newNotesFilesNames = []


# FOR THE TIME BEING THE FILES ARE NOT CHANGED
notesFileNames = getNotesFileNames(notesPath)
notesFileNames_lower = [x.lower() for x in notesFileNames]

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

        if  noteFileName_noExtension.lower() == mySlugify(noteTitle_substituted).lower():
            print("  FILE NAME IS OK " + mySlugify(noteTitle_substituted))
        else:
            trailingDigits_re = re.compile("([\d ]*)$")
            trailingDigitsResults = trailingDigits_re.search(noteFileName_noExtension_substituted)
            trailingDigits = trailingDigitsResults.group(1)

            newFileName = mySlugify(noteTitle_substituted + trailingDigits)

            # FOR THE TIME BEING THE FILES ARE NOT CHANGED
            #notesFileNames = getNotesFileNames(notesPath)

            newFileNameInPreviousFileNames = (newFileName + ".md").lower() in notesFileNames_lower
            newFileNameInNewFileNames = newFileName.lower() in newNotesFilesNames


            if sanitizeFileName(unicode(newFileName, sys.getfilesystemencoding())) != newFileName:
                print(u"  ✗ slugified name is not safe: " + unicode(newFileName) + u" vs. " + unicode(sanitizeFileName(unicode(newFileName, sys.getfilesystemencoding()))))
                #print(u"  ✗     vs. " + unicode(sanitizeFileName(unicode(newFileName, sys.getfilesystemencoding()))))
                newFileName = ""
            elif newFileNameInPreviousFileNames or newFileNameInNewFileNames:
                if newFileNameInPreviousFileNames:
                    print("  ✗ collision with existing file names " + newFileName)

                if newFileNameInNewFileNames:
                    print("  ✗ collision with NEW file names " + newFileName)
                newFileName = ""
            else:
                print("    COLLISION ✓ SORTED BY ADDING TRAILING DIGITS: " + newFileName)
            
            if newFileName != "":
                newNotesFilesNames.append(newFileName.lower())

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
                        if args.fix_name_and_assets_links:
                            with codecs.open(noteFilePath, 'w', encoding='utf-8') as fileW:
                                print(noteFilePath)
                                fileW.write(data_new)
                                fileW.close()

                command = ' [ -d '+ quotePathForShell(notesPath + "assets/" + noteFileName_noExtension) +' ] && mv ' + quotePathForShell(notesPath + "assets/" + noteFileName_noExtension) + " " + quotePathForShell(notesPath + "assets/" + newFileName)
                print("          " + command)
                if args.fix_name_and_assets_links:
                    call(command, shell=True)

                command = 'mv ' + quotePathForShell(notesPath + noteFileName) + " " + quotePathForShell(notesPath + newFileName + ".md")
                print("          " + command)
                if args.fix_name_and_assets_links:
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
