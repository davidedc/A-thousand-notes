# coding=utf-8

from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import wordSubstitutions
from helper_routines import bearEscapeDirectoryName
from helper_routines import quotePathForShell
from helper_routines import sanitizeFileName
from helper_routines import changeNoteNameAssetDirNameAndAssetsLinks

from slugify import slugify

import sys
import codecs
import re
import string


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

            noteTitle_substituted_slugified = mySlugify(noteTitle_substituted)
            noteTitle_substituted_slugified_InPreviousFileNames = (noteTitle_substituted_slugified + ".md").lower() in notesFileNames_lower
            noteTitle_substituted_slugified_InNewFileNames = noteTitle_substituted_slugified.lower() in newNotesFilesNames

            trailingDigits_re = re.compile("([\d ]*)$")
            trailingDigitsResults = trailingDigits_re.search(noteFileName_noExtension_substituted)
            trailingDigits = trailingDigitsResults.group(1)

            noteTitle_substituted_slugified_withTrailingDigits = mySlugify(noteTitle_substituted + "-" + trailingDigits)
            newFileName = noteTitle_substituted_slugified_withTrailingDigits

            # FOR THE TIME BEING THE FILES ARE NOT CHANGED
            #notesFileNames = getNotesFileNames(notesPath)

            noteTitle_substituted_slugified_withTrailingDigits_InPreviousFileNames = (newFileName + ".md").lower() in notesFileNames_lower
            noteTitle_substituted_slugified_withTrailingDigits_InNewFileNames = newFileName.lower() in newNotesFilesNames


            if (not noteTitle_substituted_slugified_InPreviousFileNames) and (not noteTitle_substituted_slugified_InNewFileNames):
                print("    PLAIN CONVERSION FROM TITLE IS OK: " + noteTitle_substituted_slugified)
                newFileName = noteTitle_substituted_slugified
                #if noteTitle_substituted_slugified == "photo-2":
                #    for ffff in notesFileNames_lower:
                #        print(ffff)
            elif sanitizeFileName(unicode(newFileName, sys.getfilesystemencoding())) != newFileName:
                print(u"  ✗ slugified name is not safe: " + unicode(newFileName) + u" vs. " + unicode(sanitizeFileName(unicode(newFileName, sys.getfilesystemencoding()))))
                #print(u"  ✗     vs. " + unicode(sanitizeFileName(unicode(newFileName, sys.getfilesystemencoding()))))
                newFileName = ""
            elif noteTitle_substituted_slugified_withTrailingDigits_InPreviousFileNames or noteTitle_substituted_slugified_withTrailingDigits_InNewFileNames:
                if noteFileName_noExtension.lower() == noteTitle_substituted_slugified_withTrailingDigits.lower():
                    print("    FILE NAME IS OK: " + newFileName)
                else:
                    if noteTitle_substituted_slugified_withTrailingDigits_InPreviousFileNames:
                        print("  ✗ collision with existing file names " + newFileName)

                if noteTitle_substituted_slugified_withTrailingDigits_InNewFileNames:
                    print("  ✗ collision with NEW file names " + newFileName)
                newFileName = ""
            else:
                if  noteFileName_noExtension.lower() == newFileName.lower():
                    print("    COLLISION ✓ GOES AWAY WITH TRAILING DIGITS: " + newFileName)
                    newFileName = ""
                else:
                    print("    COLLISION ✓ CAN BE SORTED BY ADDING TRAILING DIGITS: " + newFileName)
            
            if newFileName != "":
                newNotesFilesNames.append(newFileName.lower())

            if newFileName != "":
                changeNoteNameAssetDirNameAndAssetsLinks(args.fix_name_and_assets_links, ASSETS_ABSOLUTE_PATH, notesPath, noteFileName_noExtension, newFileName)
                #raw_input("Press Enter to continue...")




        if slugFromNoteFileName_noExtension_substituted_stem == slugFromNoteTitle_substituted_stem:
            print("  " + mySlugify(noteFileName_noExtension_substituted))
        else:
            print("  ### " + noteFileName_noExtension)
            print("  ###   " + mySlugify(noteFileName_noExtension_substituted))
            print("  ###   " + mySlugify(noteTitle_substituted_slugified))

    except Exception, e:
        print("ERROR: " + str(e) )
