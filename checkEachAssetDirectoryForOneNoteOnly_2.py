# coding=utf-8

from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import getFileNames
from helper_routines import getAttachmentsDirectoryNames
from helper_routines import bearEscapeDirectoryName
from helper_routines import quotePathForShell

import sys
import codecs
#import urllib

from subprocess import call
import re

notesPath = sys.argv[1]
checkPath(notesPath)

notesFileNames = getNotesFileNames(notesPath)
attachmentsDirectoryNames = getAttachmentsDirectoryNames(notesPath)

FIX_DIRECTORIES = True

for eachDirectory in attachmentsDirectoryNames:

    #if eachDirectory.lower().find("untitled note".lower()) == -1:
    #    #print("skipping " + eachDirectory)
    #    continue

    originalDirectoryName = eachDirectory
    originalDirectoryPath = notesPath + originalDirectoryName

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

            if data.lower().find(directoryAsFoundInMd.lower()) != -1:
                notesPointingToDir.append(noteFileName)
                howManyFilesPointToDir = howManyFilesPointToDir + 1

    if howManyFilesPointToDir == 0:
        print(str(howManyFilesPointToDir) + " notes referencing directory " + originalDirectoryName)
    elif howManyFilesPointToDir > 1:
        print(str(howManyFilesPointToDir) + " notes referencing directory " + originalDirectoryName)
        for noteFileName in notesPointingToDir:
            print("  " + noteFileName)
        assetsFiles = getFileNames(originalDirectoryPath)

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

                    if data.lower().find(assetAsFoundInMd.lower()) != -1:
                        notesPointingToAsset.append(noteFileName)
                        howManyFilesPointToAsset = howManyFilesPointToAsset + 1

            if howManyFilesPointToAsset == 0:
                print("      ERROR: counter: " + str(howManyFilesPointToAsset) + " " + assetFile)
            elif howManyFilesPointToAsset == 1:
                noteFileName = re.sub('\.md$', '', notesPointingToAsset[0])
                print(u"      ✓ " + unicode(assetFile) + u" in " + unicode(noteFileName))

                if FIX_DIRECTORIES:
                    newDirPath = notesPath + noteFileName
                    noteFilePath = newDirPath + ".md"

                    command = 'mkdir -p ' + quotePathForShell(newDirPath + "/")
                    print("          " + command)
                    call(command, shell=True)

                    command = 'mv ' + quotePathForShell(originalDirectoryPath + "/" + assetFile) + " " + quotePathForShell(newDirPath + "/" + assetFile)
                    print("          " + command)
                    call(command, shell=True)

                    try:
                        #print(noteFilePath)
                        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
                            data = file.read()
                            file.close()

                            assetLinkAsItShouldBe = unicode("![](" + bearEscapeDirectoryName(noteFileName) + "/" + bearEscapeDirectoryName(assetFile) + ")")


                            #insensitive_re = re.compile(re.escape(assetAsFoundInMd), re.IGNORECASE)
                            data = re.sub(re.escape(assetAsFoundInMd), assetLinkAsItShouldBe, data, flags=re.IGNORECASE)

                            with codecs.open(noteFilePath, 'w', encoding='utf-8') as fileW:
                                print("          changing links in " + noteFilePath)
                                fileW.write(data)
                                fileW.close()
                                #raw_input("Press Enter to continue...")
                    except Exception, e:
                        print("ERROR: " + str(e) )


            elif howManyFilesPointToAsset > 1:
                print("      ERROR: counter: " + str(howManyFilesPointToAsset) + " " + assetFile)
                for noteFilePointingToAssetName in notesPointingToAsset:
                    print("        " + noteFilePointingToAssetName)


