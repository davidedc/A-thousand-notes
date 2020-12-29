# coding=utf-8

from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import getFileNames
from helper_routines import getAttachmentsDirectoryNames
from helper_routines import bearEscapeDirectoryName

import sys
import codecs
#import urllib

notesPath = sys.argv[1]
checkPath(notesPath)

notesFileNames = getNotesFileNames(notesPath)
attachmentsDirectoryNames = getAttachmentsDirectoryNames(notesPath)


for eachDirectory in attachmentsDirectoryNames:

    #if eachDirectory.find("Note") == -1:
    #    continue

    originalDirectoryName = eachDirectory

    # directoryAsFoundInMd = unicode("![](" + urllib.quote(eachDirectory.encode('utf8')))
    eachDirectory = bearEscapeDirectoryName(eachDirectory)

    directoryAsFoundInMd = unicode("![](" + eachDirectory + "/")

    howManyFilesPointToDir = 0
    notesPointingToDir = []
    for noteFileName in notesFileNames:
        noteFilePath = notesPath + "/" + noteFileName

        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()

            if data.find(directoryAsFoundInMd) != -1:
                notesPointingToDir.append(noteFileName)
                howManyFilesPointToDir = howManyFilesPointToDir + 1

    if howManyFilesPointToDir == 0:
        print(str(howManyFilesPointToDir) + " notes referencing directory " + originalDirectoryName)
    elif howManyFilesPointToDir > 1:
        print(str(howManyFilesPointToDir) + " notes referencing directory " + originalDirectoryName)
        for noteFileName in notesPointingToDir:
            print("  " + noteFileName)
        assetsFiles = getFileNames(notesPath + "/" + originalDirectoryName)

        print("    checking all assets:")

        if len(assetsFiles) == 0:
            print("      WARNING: NO ASSETS (directory can be deleted?)")

        for assetFile in assetsFiles:
            #print("      " + assetFile)
            assetAsFoundInMd = unicode("![](" + eachDirectory + "/" + bearEscapeDirectoryName(assetFile) + ")")

            howManyFilesPointToAsset = 0
            notesPointingToAsset = []

            for noteFileName in notesFileNames:
                noteFilePath = notesPath + "/" + noteFileName

                with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
                    data = file.read()
                    file.close()

                    if data.find(assetAsFoundInMd) != -1:
                        notesPointingToAsset.append(noteFileName)
                        howManyFilesPointToAsset = howManyFilesPointToAsset + 1
            if howManyFilesPointToAsset == 0:
                print("      ERROR: counter: " + str(howManyFilesPointToAsset) + " " + assetFile)
            elif howManyFilesPointToAsset == 1:
                print(u"      ✓ " + unicode(assetFile) + u" in " + unicode(notesPointingToAsset[0]))
            elif howManyFilesPointToAsset > 1:
                print("      ERROR: counter: " + str(howManyFilesPointToAsset) + " " + assetFile)
                for noteFilePointingToAssetName in notesPointingToAsset:
                    print("        " + noteFilePointingToAssetName)


