# coding=utf-8

from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import getAttachmentsDirectoryNames
from helper_routines import bearEscapeDirectoryName

import sys
import codecs
#import urllib

notesPath = sys.argv[1]
checkPath(notesPath)

notesFileNames = getNotesFileNames(notesPath)
attachmentsDirectoryNames = getAttachmentsDirectoryNames(notesPath)


# goessnerv2 has a directory but no link
# Small Axe review Steve McQueen’s new film series is one of this year’s best - The Verge
# p60s from Shazam
# The Fifth Sense | i-D
# nothke - itch.io
# Refik Anadol – Media Artist + Director
# Eigendecomposition of a matrix - Wikipedia
# Alan Hart CV
# Contract Borrows Rd - scan
# How to dynamically create and extend classes in fizzylogo v1
# Enhanced Morphs and mirroring across workspaces
# Nushell | A new type of shell.
# DONE Moongift notes need japanese taken out

for eachDirectory in attachmentsDirectoryNames:

    originalDirectoryName = eachDirectory

    # directoryAsFoundInMd = unicode("![](" + urllib.quote(eachDirectory.encode('utf8')))
    eachDirectory = bearEscapeDirectoryName(eachDirectory)

    directoryAsFoundInMd = unicode("![](" + eachDirectory + "/")

    howManyFilesPointToDir = 0
    for noteFileName in notesFileNames:
        noteFilePath = notesPath + "/" + noteFileName
        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()

            if data.find(directoryAsFoundInMd) != -1:
                howManyFilesPointToDir = howManyFilesPointToDir + 1

    print("counter: " + str(howManyFilesPointToDir) + " " + originalDirectoryName)

