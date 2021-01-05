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
import string


notesPath = sys.argv[1]
checkPath(notesPath)

NOTES_ABSOLUTE_PATH = "file:///Users/davidedellacasa/Public/10000notes/"

notesFileNames = getNotesFileNames(notesPath)
attachmentsDirectoryNames = getAttachmentsDirectoryNames(notesPath)

FIX_ASSETS_REFERENCES = True

"""
for eachDirectory in attachmentsDirectoryNames:
    originalDirectoryPath = notesPath + eachDirectory

    assetsFiles = getFileNames(originalDirectoryPath)

    print("    checking we can access assets directory: " + eachDirectory)

    if len(assetsFiles) == 0:
        print("      WARNING: NO ASSETS (directory can be deleted?) " + originalDirectoryPath)
"""

for eachDirectory in attachmentsDirectoryNames:

    #if eachDirectory.lower().find("Transaction listing monthly".lower()) == -1:
    #    #print("skipping " + eachDirectory)
    #    continue

    originalDirectoryPath = notesPath + eachDirectory

    eachDirectoryStem = eachDirectory.rstrip().rstrip(string.digits).rstrip()


    # plainReferencesToDirectory = unicode("![](" + urllib.quote(eachDirectory.encode('utf8')))
    eachDirectory_bearEscaped = bearEscapeDirectoryName(eachDirectory)
    eachDirectory_bearEscaped_lower = eachDirectory_bearEscaped.lower()

    plainReferencesToDirectory = unicode("![](" + eachDirectory_bearEscaped + "/")
    plainReferencesToDirectory_lower = plainReferencesToDirectory.lower()

    referencesToDirectoryCount = 0
    notesPointingToDir = []

    for noteFileName in notesFileNames:

        if noteFileName.lower().find(eachDirectoryStem.lower()) == -1:
            continue

        noteFilePath = notesPath + "/" + noteFileName

        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
            data = file.read()
            data_lower = data.lower()
            file.close()


            if data_lower.find(plainReferencesToDirectory_lower) != -1:
                notesPointingToDir.append(noteFileName)
                referencesToDirectoryCount = referencesToDirectoryCount + 1

            complexMarkdownOccurrences_re = re.compile('\\[[^\\]]*\\]\\(' + re.escape(NOTES_ABSOLUTE_PATH.lower() + eachDirectory_bearEscaped_lower + "/"))
            #print(complexMarkdownOccurrences_re.pattern)
            #print(data_lower)
            if re.search(complexMarkdownOccurrences_re, data_lower):
                #print(" " + eachDirectory + " found (also) in form [something](directory) in note " + noteFileName)
                if noteFileName not in notesPointingToDir:
                    notesPointingToDir.append(noteFileName)
                    referencesToDirectoryCount = referencesToDirectoryCount + 1



    if referencesToDirectoryCount == 0:
        print("ERROR: " + str(referencesToDirectoryCount) + " notes referencing directory " + eachDirectory)

    elif referencesToDirectoryCount > 1:
        print("ERROR: " + str(referencesToDirectoryCount) + " notes referencing directory " + eachDirectory + " :")
        for noteFileName in notesPointingToDir:
            print("  " + noteFileName)

    elif referencesToDirectoryCount == 1:
        assetsFiles = getFileNames(originalDirectoryPath)

        #print("    checking all assets:")

        if len(assetsFiles) == 0:
            print("      WARNING: NO ASSETS (directory can be deleted?) " + originalDirectoryPath)

        for assetFile in assetsFiles:
            #print("      " + assetFile)

            if assetFile == ".DS_Store":
                continue

            if not assetFile.endswith(".html"):
                continue


            assetFile_lower = assetFile.lower()
            assetFile_bearEscaped = bearEscapeDirectoryName(assetFile)
            assetFile_bearEscaped = assetFile_bearEscaped.replace(u"?","%3F")
            assetFile_bearEscaped_lower = assetFile_bearEscaped.lower()


            howManyFilesPointToAsset = 0
            notesPointingToAsset = []

            for noteFileName in notesFileNames:

                if noteFileName.lower().find(eachDirectoryStem.lower()) == -1:
                    continue

                noteFilePath = notesPath + "/" + noteFileName

                with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
                    data = file.read()
                    data_lower = data.lower()
                    file.close()


                    # ---------------------------------------------------------
                    plainReferencesToAsset = unicode("![](" + eachDirectory_bearEscaped + "/" + assetFile_bearEscaped + ")")
                    if data.lower().find(plainReferencesToAsset.lower()) != -1:
                        notesPointingToAsset.append(noteFileName)
                        howManyFilesPointToAsset = howManyFilesPointToAsset + 1

                    # ---------------------------------------------------------
                    complexMarkdownOccurrences_re = re.compile(re.escape('\\[[^\\]]*\\]\\(' + NOTES_ABSOLUTE_PATH.lower() + eachDirectory_bearEscaped_lower + "/" + assetFile_bearEscaped_lower))
                    #print(complexMarkdownOccurrences_re.pattern)
                    #print(data_lower)
                    if re.search(complexMarkdownOccurrences_re, data_lower):
                        print(" " + assetFile + " found (also) in form [something](directory) in note " + noteFileName)
                        if noteFileName not in notesPointingToAsset:
                            notesPointingToAsset.append(noteFileName)
                            howManyFilesPointToAsset = howManyFilesPointToAsset + 1


                    # ---------------------------------------------------------
                    markdownLinkToDirectory_re = re.compile(re.escape("[" + assetFile_lower + "](" + NOTES_ABSOLUTE_PATH.lower() + eachDirectory_bearEscaped_lower + "/)" ))
                    #print(markdownLinkToDirectory_re.pattern)
                    #print(data_lower)
                    if re.search(markdownLinkToDirectory_re, data_lower):
                        if noteFileName not in notesPointingToAsset:
                            notesPointingToAsset.append(noteFileName)
                            howManyFilesPointToAsset = howManyFilesPointToAsset + 1


                    # ---------------------------------------------------------
                    # TODO THESE REFERENCES HERE WILL HAVE TO BE FIXED
                    htmlLinkToFileOccurrences_re = re.compile(re.escape("<a href='" + assetFile_bearEscaped_lower + "'>" + assetFile_lower + "</a>" ))
                    #print(htmlLinkToFileOccurrences_re.pattern)
                    #print(data_lower)
                    if re.search(htmlLinkToFileOccurrences_re, data_lower):
                        #print("html ref " + eachDirectory + "/" + assetFile + " in " + noteFileName)
                        if noteFileName not in notesPointingToAsset:
                            notesPointingToAsset.append(noteFileName)
                            howManyFilesPointToAsset = howManyFilesPointToAsset + 1



            if howManyFilesPointToAsset == 0:
                print("      ERROR: counter: " + str(howManyFilesPointToAsset) + " for asset " + eachDirectory + "/" + assetFile)

                if FIX_ASSETS_REFERENCES:

                    try:
                        #print(noteFilePath)
                        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
                            data = file.read()
                            file.close()


                            """
                            assetFile_butWebp = assetFile[:-4] + ".webp"
                            assetFile_butWebp_lower = assetFile_butWebp.lower()
                            assetFile_butWebp_bearEscaped = bearEscapeDirectoryName(assetFile_butWebp)
                            assetFile_butWebp_bearEscaped = assetFile_butWebp_bearEscaped.replace(u"?","%3F")
                            assetFile_butWebp_bearEscaped_lower = assetFile_butWebp_bearEscaped.lower()


                            # example:
                            # <a href='main-qimg-d704ccd59944418e7f3c5e5810caf505.webp'>main-qimg-d704ccd59944418e7f3c5e5810caf505.webp</a>
                            htmlLinkToFileOccurrences_re = re.compile(re.escape("<a href='" + assetFile_butWebp_bearEscaped_lower + "'>" + assetFile_butWebp_lower + "</a>" ), re.IGNORECASE)
                            assetLinkAsItShouldBe = "![]("+ eachDirectory_bearEscaped + "/" + assetFile_bearEscaped +")"
                            #insensitive_re = re.compile(re.escape(plainReferencesToAsset), re.IGNORECASE)
                            data_new = re.sub(htmlLinkToFileOccurrences_re, assetLinkAsItShouldBe, data)

                            if data_new != data:
                                with codecs.open(noteFilePath, 'w', encoding='utf-8') as fileW:
                                    print("          changing links in " + noteFilePath)
                                    fileW.write(data_new)
                                    fileW.close()
                                    #raw_input("Press Enter to continue...")
                            """



                            """
                            assetFile_butWebp = assetFile[:-4] + ".octet-stream"
                            assetFile_butWebp_lower = assetFile_butWebp.lower()
                            assetFile_butWebp_bearEscaped = bearEscapeDirectoryName(assetFile_butWebp)
                            assetFile_butWebp_bearEscaped = assetFile_butWebp_bearEscaped.replace(u"?","%3F")
                            assetFile_butWebp_bearEscaped_lower = assetFile_butWebp_bearEscaped.lower()


                            htmlLinkToFileOccurrences_re = re.compile(re.escape("<a href='" + assetFile_butWebp_bearEscaped_lower + "'>" + assetFile_butWebp_lower + "</a>" ), re.IGNORECASE)
                            assetLinkAsItShouldBe = "![]("+ eachDirectory_bearEscaped + "/" + assetFile_bearEscaped +")"
                            #insensitive_re = re.compile(re.escape(plainReferencesToAsset), re.IGNORECASE)
                            data_new = re.sub(htmlLinkToFileOccurrences_re, assetLinkAsItShouldBe, data)

                            if data_new != data:
                                with codecs.open(noteFilePath, 'w', encoding='utf-8') as fileW:
                                    print("          changing links in " + noteFilePath)
                                    fileW.write(data_new)
                                    fileW.close()
                                    #raw_input("Press Enter to continue...")
                            """

                            # example:
                            #<a href='image_23%2033.octet-stream'>image_23 33.octet-stream</a>
                            #[image_23 33.html](file:///Users/davidedellacasa/Public/10000notes/duct%20tape%20typography%20-%20Google%20Search/image_23%2033.html)

                            assetFile_butWebp = assetFile[:-5] + ".octet-stream"
                            assetFile_butWebp_lower = assetFile_butWebp.lower()
                            assetFile_butWebp_bearEscaped = bearEscapeDirectoryName(assetFile_butWebp)
                            assetFile_butWebp_bearEscaped = assetFile_butWebp_bearEscaped.replace(u"?","%3F")
                            assetFile_butWebp_bearEscaped_lower = assetFile_butWebp_bearEscaped.lower()


                            htmlLinkToFileOccurrences_re = re.compile(re.escape("<a href='" + assetFile_butWebp_bearEscaped_lower + "'>" + assetFile_butWebp_lower + "</a>" ), re.IGNORECASE)
                            assetLinkAsItShouldBe = "["+ assetFile +"]("+ NOTES_ABSOLUTE_PATH + eachDirectory_bearEscaped + "/" + assetFile_bearEscaped +")"
                            #insensitive_re = re.compile(re.escape(plainReferencesToAsset), re.IGNORECASE)
                            data_new = re.sub(htmlLinkToFileOccurrences_re, assetLinkAsItShouldBe, data)

                            if data_new != data:
                                with codecs.open(noteFilePath, 'w', encoding='utf-8') as fileW:
                                    print("          changing links in " + noteFilePath)
                                    fileW.write(data_new)
                                    fileW.close()
                                    #raw_input("Press Enter to continue...")


                    except Exception, e:
                        print("ERROR: " + str(e) )
            elif howManyFilesPointToAsset == 1:
                """
                if FIX_ASSETS_REFERENCES:

                    try:
                        #print(noteFilePath)
                        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
                            data = file.read()
                            file.close()

                            htmlLinkToFileOccurrences_re = re.compile(re.escape("<a href='" + assetFile_bearEscaped_lower + "'>" + assetFile_lower + "</a>" ), re.IGNORECASE)
                            assetLinkAsItShouldBe = "![]("+ eachDirectory_bearEscaped + "/" + assetFile_bearEscaped +")"
                            #insensitive_re = re.compile(re.escape(plainReferencesToAsset), re.IGNORECASE)
                            data_new = re.sub(htmlLinkToFileOccurrences_re, assetLinkAsItShouldBe, data)

                            with codecs.open(noteFilePath, 'w', encoding='utf-8') as fileW:
                                print("          changing links in " + noteFilePath)
                                fileW.write(data_new)
                                fileW.close()
                                #raw_input("Press Enter to continue...")


                    except Exception, e:
                        print("ERROR: " + str(e) )
                """


            elif howManyFilesPointToAsset > 1:
                print("      ERROR: counter: " + str(howManyFilesPointToAsset) + " for asset " + eachDirectory + "/" + assetFile)
                for noteFilePointingToAssetName in notesPointingToAsset:
                    print("        " + noteFilePointingToAssetName)


