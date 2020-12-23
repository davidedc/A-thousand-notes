# coding=utf-8

from helper_routines import checkPath

import sys
import os
import glob
import ntpath
import codecs
import urllib

notesPath = sys.argv[1]
checkPath(notesPath)

fse = sys.getfilesystemencoding()

listOfDirectories = [unicode(ntpath.basename(os.path.normpath(x)), fse) for x in glob.glob(os.path.normpath(notesPath) + "/*/")]


#print listOfDirectories

listOfFiles = [notesPath + "/" + unicode(ntpath.basename(x), fse) for x in glob.glob(os.path.normpath(notesPath) + "/*.md")]

counter = 1

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

for eachDirectory in listOfDirectories:
    if counter < 1795:
        counter = counter + 1
        continue

    if eachDirectory.find("MOONGIFT") != -1:
        counter = counter + 1
        continue

    originalDirectoryName = eachDirectory

    # directoryAsFoundInMd = unicode("![](" + urllib.quote(eachDirectory.encode('utf8')))
    eachDirectory = eachDirectory.replace("%", "%25")
    eachDirectory = eachDirectory.replace(" ", "%20")
    eachDirectory = eachDirectory.replace('"',"%22")
    eachDirectory = eachDirectory.replace(u"|","%7C")
    #eachDirectory = eachDirectory.replace(u"'","%27")


    eachDirectory = eachDirectory.replace(u"’","%E2%80%99")
    eachDirectory = eachDirectory.replace(u"–","%E2%80%93")
    eachDirectory = eachDirectory.replace(u"—","%E2%80%94")
    eachDirectory = eachDirectory.replace(u"“","%E2%80%9C")
    eachDirectory = eachDirectory.replace(u"”","%E2%80%9D")

    eachDirectory = eachDirectory.replace(u"ō","o%CC%84")
    eachDirectory = eachDirectory.replace(u"ö","%C3%B6") # LATIN SMALL LETTER O WITH DIAERESIS
    eachDirectory = eachDirectory.replace(u"é","%C3%A9") # LATIN SMALL LETTER E WITH ACUTE
    eachDirectory = eachDirectory.replace(u"™","%E2%84%A2")
    eachDirectory = eachDirectory.replace(u"<","%3C")
    eachDirectory = eachDirectory.replace(u">","%3E")
    eachDirectory = eachDirectory.replace(u"#","%23")
    eachDirectory = eachDirectory.replace(u"…","%E2%80%A6")
    eachDirectory = eachDirectory.replace(u"ü","%C3%BC")
    eachDirectory = eachDirectory.replace(u"[","%5B")
    eachDirectory = eachDirectory.replace(u"]","%5D")
    eachDirectory = eachDirectory.replace(u"í","%C3%AD")
    eachDirectory = eachDirectory.replace(u"•","%E2%80%A2")
    eachDirectory = eachDirectory.replace(u"à","%C3%A0")
    eachDirectory = eachDirectory.replace(u"å","%C3%A5")
    eachDirectory = eachDirectory.replace(u"è","%C3%A8")
    eachDirectory = eachDirectory.replace(u"ó","%C3%B3")
    eachDirectory = eachDirectory.replace(u"＃","%EF%BC%83")
    eachDirectory = eachDirectory.replace(u"^","%5E")
    eachDirectory = eachDirectory.replace(u"‘","%E2%80%98")
    eachDirectory = eachDirectory.replace(u"ï","%C3%AF")
    eachDirectory = eachDirectory.replace(u"ñ","%C3%B1")

    eachDirectory = eachDirectory.replace(u"á","%C3%A1")
    eachDirectory = eachDirectory.replace(u"⋆","%E2%8B%86")
    eachDirectory = eachDirectory.replace(u"🤓","%F0%9F%A4%93")
    eachDirectory = eachDirectory.replace(u"ë","%C3%AB")
    eachDirectory = eachDirectory.replace(u"Š","%C5%A0")

    eachDirectory = eachDirectory.replace(u"‒","%E2%80%92")
    eachDirectory = eachDirectory.replace(u"★","%E2%98%85")
    eachDirectory = eachDirectory.replace(u"λ","%CE%BB")
    eachDirectory = eachDirectory.replace(u"ç","%C3%A7")
    eachDirectory = eachDirectory.replace(u"″","%E2%80%B3")
    eachDirectory = eachDirectory.replace(u"ý","%C3%BD")
    eachDirectory = eachDirectory.replace(u"π","%CF%80")
    eachDirectory = eachDirectory.replace(u"É","%C3%89")
    eachDirectory = eachDirectory.replace(u"œ","%C5%93")
    eachDirectory = eachDirectory.replace(u"ä","%C3%A4")
    eachDirectory = eachDirectory.replace(u"ü","%C3%BC")
    eachDirectory = eachDirectory.replace(u"ł","%C5%82")
    eachDirectory = eachDirectory.replace(u"Č","%C4%8C")
    eachDirectory = eachDirectory.replace(u"ć","%C4%87")
    eachDirectory = eachDirectory.replace(u"Ř","%C5%98")
    eachDirectory = eachDirectory.replace(u"í","%C3%AD")
    eachDirectory = eachDirectory.replace(u"ì","%C3%AC")
    eachDirectory = eachDirectory.replace(u"ý","%C3%BD")
    eachDirectory = eachDirectory.replace(u"ò","%C3%B2")
    eachDirectory = eachDirectory.replace(u"›","%E2%80%BA")
    eachDirectory = eachDirectory.replace(u"Ö","%C3%96")
    eachDirectory = eachDirectory.replace(u"⁓","%E2%81%93")





    eachDirectory = eachDirectory.replace(u"¡","%C2%A1") # INVERTED EXCLAMATION MARK
    eachDirectory = eachDirectory.replace(u"¢","%C2%A2") # CENT SIGN
    eachDirectory = eachDirectory.replace(u"£","%C2%A3") # POUND SIGN
    eachDirectory = eachDirectory.replace(u"¤","%C2%A4") # CURRENCY SIGN
    eachDirectory = eachDirectory.replace(u"¥","%C2%A5") # YEN SIGN
    eachDirectory = eachDirectory.replace(u"¦","%C2%A6") # BROKEN BAR
    eachDirectory = eachDirectory.replace(u"§","%C2%A7") # SECTION SIGN
    eachDirectory = eachDirectory.replace(u"¨","%C2%A8") # DIAERESIS
    eachDirectory = eachDirectory.replace(u"©","%C2%A9") # COPYRIGHT SIGN
    eachDirectory = eachDirectory.replace(u"ª","%C2%AA") # FEMININE ORDINAL INDICATOR
    eachDirectory = eachDirectory.replace(u"«","%C2%AB") # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    eachDirectory = eachDirectory.replace(u"¬","%C2%AC") # NOT SIGN
    eachDirectory = eachDirectory.replace(u"®","%C2%AE") # REGISTERED SIGN
    eachDirectory = eachDirectory.replace(u"¯","%C2%AF") # MACRON
    eachDirectory = eachDirectory.replace(u"°","%C2%B0") # DEGREE SIGN
    eachDirectory = eachDirectory.replace(u"±","%C2%B1") # PLUS-MINUS SIGN
    eachDirectory = eachDirectory.replace(u"²","%C2%B2") # SUPERSCRIPT TWO
    eachDirectory = eachDirectory.replace(u"³","%C2%B3") # SUPERSCRIPT THREE
    eachDirectory = eachDirectory.replace(u"´","%C2%B4") # ACUTE ACCENT
    eachDirectory = eachDirectory.replace(u"µ","%C2%B5") # MICRO SIGN
    eachDirectory = eachDirectory.replace(u"¶","%C2%B6") # PILCROW SIGN
    eachDirectory = eachDirectory.replace(u"·","%C2%B7") # MIDDLE DOT
    eachDirectory = eachDirectory.replace(u"¸","%C2%B8") # CEDILLA
    eachDirectory = eachDirectory.replace(u"¹","%C2%B9") # SUPERSCRIPT ONE
    eachDirectory = eachDirectory.replace(u"º","%C2%BA") # MASCULINE ORDINAL INDICATOR
    eachDirectory = eachDirectory.replace(u"»","%C2%BB") # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    eachDirectory = eachDirectory.replace(u"¼","%C2%BC") # VULGAR FRACTION ONE QUARTER
    eachDirectory = eachDirectory.replace(u"½","%C2%BD") # VULGAR FRACTION ONE HALF
    eachDirectory = eachDirectory.replace(u"¾","%C2%BE") # VULGAR FRACTION THREE QUARTERS
    eachDirectory = eachDirectory.replace(u"¿","%C2%BF") # INVERTED QUESTION MARK
    eachDirectory = eachDirectory.replace(u"À","%C3%80") # LATIN CAPITAL LETTER A WITH GRAVE
    eachDirectory = eachDirectory.replace(u"Á","%C3%81") # LATIN CAPITAL LETTER A WITH ACUTE
    eachDirectory = eachDirectory.replace(u"Â","%C3%82") # LATIN CAPITAL LETTER A WITH CIRCUMFLEX
    eachDirectory = eachDirectory.replace(u"Ã","%C3%83") # LATIN CAPITAL LETTER A WITH TILDE
    eachDirectory = eachDirectory.replace(u"Ä","%C3%84") # LATIN CAPITAL LETTER A WITH DIAERESIS
    eachDirectory = eachDirectory.replace(u"Å","%C3%85") # LATIN CAPITAL LETTER A WITH RING ABOVE
    eachDirectory = eachDirectory.replace(u"Æ","%C3%86") # LATIN CAPITAL LETTER AE
    eachDirectory = eachDirectory.replace(u"Ç","%C3%87") # LATIN CAPITAL LETTER C WITH CEDILLA
    eachDirectory = eachDirectory.replace(u"È","%C3%88") # LATIN CAPITAL LETTER E WITH GRAVE
    eachDirectory = eachDirectory.replace(u"É","%C3%89") # LATIN CAPITAL LETTER E WITH ACUTE
    eachDirectory = eachDirectory.replace(u"Ê","%C3%8A") # LATIN CAPITAL LETTER E WITH CIRCUMFLEX
    eachDirectory = eachDirectory.replace(u"Ë","%C3%8B") # LATIN CAPITAL LETTER E WITH DIAERESIS
    eachDirectory = eachDirectory.replace(u"Ì","%C3%8C") # LATIN CAPITAL LETTER I WITH GRAVE
    eachDirectory = eachDirectory.replace(u"Í","%C3%8D") # LATIN CAPITAL LETTER I WITH ACUTE
    eachDirectory = eachDirectory.replace(u"Î","%C3%8E") # LATIN CAPITAL LETTER I WITH CIRCUMFLEX
    eachDirectory = eachDirectory.replace(u"Ï","%C3%8F") # LATIN CAPITAL LETTER I WITH DIAERESIS
    eachDirectory = eachDirectory.replace(u"Ð","%C3%90") # LATIN CAPITAL LETTER ETH
    eachDirectory = eachDirectory.replace(u"Ñ","%C3%91") # LATIN CAPITAL LETTER N WITH TILDE
    eachDirectory = eachDirectory.replace(u"Ò","%C3%92") # LATIN CAPITAL LETTER O WITH GRAVE
    eachDirectory = eachDirectory.replace(u"Ó","%C3%93") # LATIN CAPITAL LETTER O WITH ACUTE
    eachDirectory = eachDirectory.replace(u"Ô","%C3%94") # LATIN CAPITAL LETTER O WITH CIRCUMFLEX
    eachDirectory = eachDirectory.replace(u"Õ","%C3%95") # LATIN CAPITAL LETTER O WITH TILDE
    eachDirectory = eachDirectory.replace(u"Ö","%C3%96") # LATIN CAPITAL LETTER O WITH DIAERESIS
    eachDirectory = eachDirectory.replace(u"×","%C3%97") # MULTIPLICATION SIGN
    eachDirectory = eachDirectory.replace(u"Ø","%C3%98") # LATIN CAPITAL LETTER O WITH STROKE
    eachDirectory = eachDirectory.replace(u"Ù","%C3%99") # LATIN CAPITAL LETTER U WITH GRAVE
    eachDirectory = eachDirectory.replace(u"Ú","%C3%9A") # LATIN CAPITAL LETTER U WITH ACUTE
    eachDirectory = eachDirectory.replace(u"Û","%C3%9B") # LATIN CAPITAL LETTER U WITH CIRCUMFLEX
    eachDirectory = eachDirectory.replace(u"Ü","%C3%9C") # LATIN CAPITAL LETTER U WITH DIAERESIS
    eachDirectory = eachDirectory.replace(u"Ý","%C3%9D") # LATIN CAPITAL LETTER Y WITH ACUTE
    eachDirectory = eachDirectory.replace(u"Þ","%C3%9E") # LATIN CAPITAL LETTER THORN
    eachDirectory = eachDirectory.replace(u"ß","%C3%9F") # LATIN SMALL LETTER SHARP S
    eachDirectory = eachDirectory.replace(u"à","%C3%A0") # LATIN SMALL LETTER A WITH GRAVE
    eachDirectory = eachDirectory.replace(u"á","%C3%A1") # LATIN SMALL LETTER A WITH ACUTE
    eachDirectory = eachDirectory.replace(u"â","%C3%A2") # LATIN SMALL LETTER A WITH CIRCUMFLEX
    eachDirectory = eachDirectory.replace(u"ã","%C3%A3") # LATIN SMALL LETTER A WITH TILDE
    eachDirectory = eachDirectory.replace(u"ä","%C3%A4") # LATIN SMALL LETTER A WITH DIAERESIS
    eachDirectory = eachDirectory.replace(u"å","%C3%A5") # LATIN SMALL LETTER A WITH RING ABOVE
    eachDirectory = eachDirectory.replace(u"æ","%C3%A6") # LATIN SMALL LETTER AE
    eachDirectory = eachDirectory.replace(u"ç","%C3%A7") # LATIN SMALL LETTER C WITH CEDILLA
    eachDirectory = eachDirectory.replace(u"è","%C3%A8") # LATIN SMALL LETTER E WITH GRAVE
    eachDirectory = eachDirectory.replace(u"ê","%C3%AA") # LATIN SMALL LETTER E WITH CIRCUMFLEX
    eachDirectory = eachDirectory.replace(u"ë","%C3%AB") # LATIN SMALL LETTER E WITH DIAERESIS
    eachDirectory = eachDirectory.replace(u"ì","%C3%AC") # LATIN SMALL LETTER I WITH GRAVE
    eachDirectory = eachDirectory.replace(u"í","%C3%AD") # LATIN SMALL LETTER I WITH ACUTE
    eachDirectory = eachDirectory.replace(u"î","%C3%AE") # LATIN SMALL LETTER I WITH CIRCUMFLEX
    eachDirectory = eachDirectory.replace(u"ï","%C3%AF") # LATIN SMALL LETTER I WITH DIAERESIS
    eachDirectory = eachDirectory.replace(u"ð","%C3%B0") # LATIN SMALL LETTER ETH
    eachDirectory = eachDirectory.replace(u"ñ","%C3%B1") # LATIN SMALL LETTER N WITH TILDE
    eachDirectory = eachDirectory.replace(u"ò","%C3%B2") # LATIN SMALL LETTER O WITH GRAVE
    eachDirectory = eachDirectory.replace(u"ó","%C3%B3") # LATIN SMALL LETTER O WITH ACUTE
    eachDirectory = eachDirectory.replace(u"ô","%C3%B4") # LATIN SMALL LETTER O WITH CIRCUMFLEX
    eachDirectory = eachDirectory.replace(u"õ","%C3%B5") # LATIN SMALL LETTER O WITH TILDE
    eachDirectory = eachDirectory.replace(u"÷","%C3%B7") # DIVISION SIGNo
    eachDirectory = eachDirectory.replace(u"ø","%C3%B8") # LATIN SMALL LETTER O WITH STROKE
    eachDirectory = eachDirectory.replace(u"ù","%C3%B9") # LATIN SMALL LETTER U WITH GRAVE
    eachDirectory = eachDirectory.replace(u"ú","%C3%BA") # LATIN SMALL LETTER U WITH ACUTE
    eachDirectory = eachDirectory.replace(u"û","%C3%BB") # LATIN SMALL LETTER U WITH CIRCUMFLEX
    eachDirectory = eachDirectory.replace(u"ü","%C3%BC") # LATIN SMALL LETTER U WITH DIAERESIS
    eachDirectory = eachDirectory.replace(u"ý","%C3%BD") # LATIN SMALL LETTER Y WITH ACUTE
    eachDirectory = eachDirectory.replace(u"þ","%C3%BE") # LATIN SMALL LETTER THORN
    eachDirectory = eachDirectory.replace(u"ÿ","%C3%BF") # LATIN SMALL LETTER Y WITH DIAERESIS

    directoryAsFoundInMd = unicode("![](" + eachDirectory + "/")

    tryingToFindTheMdFile = notesPath + "/" + originalDirectoryName + ".md"
    try:
        with codecs.open(tryingToFindTheMdFile, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
            if data.find(unicode("![")) == -1:
                print("")
                #print(directoryAsFoundInMd)
                #print("counter: " + str(counter))
                #print("####### the file " + tryingToFindTheMdFile +" exists but does not contain ANY link")
            elif data.find(directoryAsFoundInMd) == -1:
                print(directoryAsFoundInMd)
                print("counter: " + str(counter))
                print("####### the file " + tryingToFindTheMdFile +" exists - some escaping is wrong")
    except:
        print("")
        #print(directoryAsFoundInMd)
        #print("counter: " + str(counter))
        #print("####### the file " + tryingToFindTheMdFile +" does not exist")

    """
    howManyFilesPointToDir = 0
    for eachFile in listOfFiles:
        with codecs.open(eachFile, encoding='utf-8') as file:
            data = file.read()
            file.close()

            if data.find(directoryAsFoundInMd) != -1:
                howManyFilesPointToDir = howManyFilesPointToDir + 1
            else:
                if howManyFilesPointToDir > 0:
                    break

    if howManyFilesPointToDir == 0:
        tryingToFindTheMdFile = notesPath + "/" + originalDirectoryName + ".md"
        print(directoryAsFoundInMd)
        print("counter: " + str(counter) + " " + eachFile)
        try:
            with codecs.open(tryingToFindTheMdFile, encoding='utf-8') as file:
                data = file.read()
                file.close()
                if data.find(unicode("![")) == -1:
                    print("####### the file " + tryingToFindTheMdFile +" exists but does not contain ANY link")
                else:
                    print("####### the file " + tryingToFindTheMdFile +" exists - some escaping is wrong")
        except:
            print("####### the file " + tryingToFindTheMdFile +" does not exist")
    """


    counter = counter + 1
