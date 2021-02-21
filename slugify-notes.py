# coding=utf-8

from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import wordSubstitutions
from helper_routines import bearEscapeDirectoryName
from helper_routines import quotePathForShell
from helper_routines import sanitizeFileName
from helper_routines import changeNoteNameAssetDirNameAndAssetsLinks
from helper_routines import mySlugify

import sys
import codecs
import re
import string


import argparse
from argparse import RawTextHelpFormatter

import os


parser = argparse.ArgumentParser(description="slugifies note file names starting from the note title.\n\nExamples:\npython slugify-notes.py ../../../Public/10000notes/\npython slugify-notes.py -f ../../../Public/10000notes/", formatter_class=RawTextHelpFormatter)
parser.add_argument('path', help="notes' path")
parser.add_argument('-f', '--fix-name-and-assets-links', help="fix the name, the assets directory and the asset links", action='store_true')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

notesPath = os.path.join(args.path, '') # add trailing slash if it's not there
checkPath(notesPath)

NOTES_ABSOLUTE_PATH = "file://" + os.path.abspath(notesPath) + "/"
ASSETS_ABSOLUTE_PATH = NOTES_ABSOLUTE_PATH + "assets/"

notesFileNames = getNotesFileNames(notesPath)
# this is so that "note.md" comes before "note-2.md"
# so we examine the files (and the namings) always in the
# same logical order, starting with the files that heave the
# least "collision trailing number" in the filename
notesFileNames = sorted(notesFileNames, key=len)
notesFileNames_lower = [x.lower() for x in notesFileNames]

newNotesFilesNames = []

if args.verbose:
    for noteFileName in notesFileNames:
        print(noteFileName)

for noteFileName in notesFileNames:

    noteFileName_noExtension = noteFileName[:-3]
    noteFilePath = notesPath + noteFileName

    try:
        #print(noteFilePath)
        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            file.close()

        noteTitle = lines[1][2:]

        noteFileName_noExtension_substituted = wordSubstitutions(noteFileName_noExtension)
        noteTitle_substituted = wordSubstitutions(noteTitle)


        noteFileName_noExtension_substituted_stem = noteFileName_noExtension_substituted.rstrip().rstrip(string.digits).rstrip()
        noteTitle_substituted_stem = noteTitle_substituted.rstrip().rstrip(string.digits).rstrip()

        slugFromNoteFileName_noExtension_substituted_stem = mySlugify(noteFileName_noExtension_substituted_stem)
        slugFromNoteTitle_substituted_stem = mySlugify(noteTitle_substituted_stem)

        if  noteFileName_noExtension.lower() == mySlugify(noteTitle_substituted).lower():
            if args.verbose:
                print(noteFileName_noExtension + " ...FILE NAME IS OK " + mySlugify(noteTitle_substituted))
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
                if args.verbose:
                    print(noteFileName_noExtension + " ...PLAIN CONVERSION FROM TITLE IS OK: " + noteTitle_substituted_slugified)
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
                    if args.verbose:
                        print(noteFileName_noExtension + " ...FILE NAME IS OK: " + newFileName)
                else:
                    if noteTitle_substituted_slugified_withTrailingDigits_InPreviousFileNames:
                        print(noteFileName_noExtension + " ... ✗ collision with existing file names " + newFileName)

                if noteTitle_substituted_slugified_withTrailingDigits_InNewFileNames:
                    print(noteFileName_noExtension + " ... ✗ collision with NEW file names " + newFileName)
                newFileName = ""
            else:
                if  noteFileName_noExtension.lower() == newFileName.lower():
                    if args.verbose:
                        print(noteFileName_noExtension + " ...COLLISION ✓ GOES AWAY WITH TRAILING DIGITS: " + newFileName)
                    newFileName = ""
                else:
                    if args.verbose:
                        print(noteFileName_noExtension + " ...COLLISION ✓ CAN BE SORTED BY ADDING TRAILING DIGITS: " + newFileName)
            
            if newFileName != "":
                newNotesFilesNames.append(newFileName.lower())

            if newFileName != "":
                changeNoteNameAssetDirNameAndAssetsLinks(args.fix_name_and_assets_links, args.verbose, notesPath, noteFileName_noExtension, newFileName, notesPath)
                #raw_input("Press Enter to continue...")




        if args.verbose:
            if slugFromNoteFileName_noExtension_substituted_stem == slugFromNoteTitle_substituted_stem:
                print("  " + mySlugify(noteFileName_noExtension_substituted))
            else:
                print("  ### " + noteFileName_noExtension)
                print("  ###   " + mySlugify(noteFileName_noExtension_substituted))
                print("  ###   " + mySlugify(noteTitle_substituted_slugified))

    except Exception, e:
        print("ERROR: " + str(e) )
