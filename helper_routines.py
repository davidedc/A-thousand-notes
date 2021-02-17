# coding=utf-8

import unicodedata
import re
import os
import sys
import glob
import ntpath

from os import listdir
from os.path import isfile, join

import codecs
from subprocess import call

import platform
import locale

import math
from datetime import datetime

def quotePathForShell(thePath):
    return '"' + thePath.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`') + '"'

def stripEmptyTailLines(lines):
    while lines[-1].strip() == "":
      del lines[-1]

def getNotesFileNames(notesPath):
    fse = sys.getfilesystemencoding()
    theList = [unicode(ntpath.basename(x), fse) for x in glob.glob(os.path.normpath(notesPath) + "/*.md")]

    # this is just to give AN order to the list (instead of undefined or random)
    # note that "note-2.md" comes before "note.md"
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') # vary depending on your lang/locale
    return sorted(theList,cmp=locale.strcoll)


def getFileNames(path):
    #fse = sys.getfilesystemencoding()
    #return [ntpath.basename(x) for x in glob.glob(os.path.normpath(path) + "/*")]
    theList =  [f for f in listdir(path) if isfile(join(path, f))]

    # this is just to give AN order to the list (instead of undefined or random)
    # note that "note-2.md" comes before "note.md"
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') # vary depending on your lang/locale
    return sorted(theList,cmp=locale.strcoll)

def getAttachmentsDirectoryNames(notesPath):
    fse = sys.getfilesystemencoding()
    theList = [unicode(ntpath.basename(os.path.normpath(x)), fse) for x in glob.glob(os.path.normpath(notesPath) + "/*/")]

    # this is just to give AN order to the list (instead of undefined or random)
    # note that "note-2.md" comes before "note.md"
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') # vary depending on your lang/locale
    return sorted(theList,cmp=locale.strcoll)

def checkPath(notesPath):
    if not os.path.exists(notesPath):
        exit("no such path")


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def modification_date(path_to_file):
    return os.path.getmtime(path_to_file)

def access_date(path_to_file):
    return os.path.getatime(path_to_file)


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

escapements = [
    ["%", "%25"],
    [" ", "%20"],
    ['"',"%22"],
    [u"|","%7C"],
    #[u"?","%3F"],

    #[u"'","%27"],


    [u"’","%E2%80%99"],
    [u"–","%E2%80%93"],
    [u"—","%E2%80%94"],
    [u"“","%E2%80%9C"],
    [u"”","%E2%80%9D"],

    [u"ō","o%CC%84"],
    [u"ö","%C3%B6"], # LATIN SMALL LETTER O WITH DIAERESIS
    [u"é","%C3%A9"], # LATIN SMALL LETTER E WITH ACUTE
    [u"™","%E2%84%A2"],
    [u"<","%3C"],
    [u">","%3E"],
    [u"#","%23"],
    [u"…","%E2%80%A6"],
    [u"ü","%C3%BC"],
    [u"ù","%C3%B9"], # LATIN SMALL LETTER U WITH GRAVE
    [u"[","%5B"],
    [u"]","%5D"],
    [u"í","%C3%AD"],
    [u"•","%E2%80%A2"],
    [u"à","%C3%A0"],
    [u"å","%C3%A5"],
    [u"è","%C3%A8"],
    [u"ó","%C3%B3"],
    [u"＃","%EF%BC%83"],
    [u"^","%5E"],
    [u"‘","%E2%80%98"],
    [u"ï","%C3%AF"],
    [u"ñ","%C3%B1"],

    [u"á","%C3%A1"],
    [u"⋆","%E2%8B%86"],
    [u"🤓","%F0%9F%A4%93"],
    [u"ë","%C3%AB"],
    [u"Š","%C5%A0"],

    [u"‒","%E2%80%92"],
    [u"★","%E2%98%85"],
    [u"λ","%CE%BB"],
    [u"ç","%C3%A7"],
    [u"″","%E2%80%B3"],
    [u"ý","%C3%BD"],
    [u"π","%CF%80"],
    [u"É","%C3%89"],
    [u"œ","%C5%93"],
    [u"ä","%C3%A4"],
    [u"ü","%C3%BC"],
    [u"ł","%C5%82"],
    [u"Č","%C4%8C"],
    [u"ć","%C4%87"],
    [u"Ř","%C5%98"],
    [u"í","%C3%AD"],
    [u"ì","%C3%AC"],
    [u"ý","%C3%BD"],
    [u"ò","%C3%B2"],
    [u"›","%E2%80%BA"],
    [u"Ö","%C3%96"],
    [u"⁓","%E2%81%93"],


    [u"¡","%C2%A1"], # INVERTED EXCLAMATION MARK
    [u"¢","%C2%A2"], # CENT SIGN
    [u"£","%C2%A3"], # POUND SIGN
    [u"¤","%C2%A4"], # CURRENCY SIGN
    [u"¥","%C2%A5"], # YEN SIGN
    [u"¦","%C2%A6"], # BROKEN BAR
    [u"§","%C2%A7"], # SECTION SIGN
    [u"¨","%C2%A8"], # DIAERESIS
    [u"©","%C2%A9"], # COPYRIGHT SIGN
    [u"ª","%C2%AA"], # FEMININE ORDINAL INDICATOR
    [u"«","%C2%AB"], # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    [u"¬","%C2%AC"], # NOT SIGN
    [u"®","%C2%AE"], # REGISTERED SIGN
    [u"¯","%C2%AF"], # MACRON
    [u"°","%C2%B0"], # DEGREE SIGN
    [u"±","%C2%B1"], # PLUS-MINUS SIGN
    [u"²","%C2%B2"], # SUPERSCRIPT TWO
    [u"³","%C2%B3"], # SUPERSCRIPT THREE
    [u"´","%C2%B4"], # ACUTE ACCENT
    [u"µ","%C2%B5"], # MICRO SIGN
    [u"¶","%C2%B6"], # PILCROW SIGN
    [u"·","%C2%B7"], # MIDDLE DOT
    [u"¸","%C2%B8"], # CEDILLA
    [u"¹","%C2%B9"], # SUPERSCRIPT ONE
    [u"º","%C2%BA"], # MASCULINE ORDINAL INDICATOR
    [u"»","%C2%BB"], # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    [u"¼","%C2%BC"], # VULGAR FRACTION ONE QUARTER
    [u"½","%C2%BD"], # VULGAR FRACTION ONE HALF
    [u"¾","%C2%BE"], # VULGAR FRACTION THREE QUARTERS
    [u"¿","%C2%BF"], # INVERTED QUESTION MARK
    [u"À","%C3%80"], # LATIN CAPITAL LETTER A WITH GRAVE
    [u"Á","%C3%81"], # LATIN CAPITAL LETTER A WITH ACUTE
    [u"Â","%C3%82"], # LATIN CAPITAL LETTER A WITH CIRCUMFLEX
    [u"Ã","%C3%83"], # LATIN CAPITAL LETTER A WITH TILDE
    [u"Ä","%C3%84"], # LATIN CAPITAL LETTER A WITH DIAERESIS
    [u"Å","%C3%85"], # LATIN CAPITAL LETTER A WITH RING ABOVE
    [u"Æ","%C3%86"], # LATIN CAPITAL LETTER AE
    [u"Ç","%C3%87"], # LATIN CAPITAL LETTER C WITH CEDILLA
    [u"È","%C3%88"], # LATIN CAPITAL LETTER E WITH GRAVE
    [u"É","%C3%89"], # LATIN CAPITAL LETTER E WITH ACUTE
    [u"Ê","%C3%8A"], # LATIN CAPITAL LETTER E WITH CIRCUMFLEX
    [u"Ë","%C3%8B"], # LATIN CAPITAL LETTER E WITH DIAERESIS
    [u"Ì","%C3%8C"], # LATIN CAPITAL LETTER I WITH GRAVE
    [u"Í","%C3%8D"], # LATIN CAPITAL LETTER I WITH ACUTE
    [u"Î","%C3%8E"], # LATIN CAPITAL LETTER I WITH CIRCUMFLEX
    [u"Ï","%C3%8F"], # LATIN CAPITAL LETTER I WITH DIAERESIS
    [u"Ð","%C3%90"], # LATIN CAPITAL LETTER ETH
    [u"Ñ","%C3%91"], # LATIN CAPITAL LETTER N WITH TILDE
    [u"Ò","%C3%92"], # LATIN CAPITAL LETTER O WITH GRAVE
    [u"Ó","%C3%93"], # LATIN CAPITAL LETTER O WITH ACUTE
    [u"Ô","%C3%94"], # LATIN CAPITAL LETTER O WITH CIRCUMFLEX
    [u"Õ","%C3%95"], # LATIN CAPITAL LETTER O WITH TILDE
    [u"Ö","%C3%96"], # LATIN CAPITAL LETTER O WITH DIAERESIS
    [u"×","%C3%97"], # MULTIPLICATION SIGN
    [u"Ø","%C3%98"], # LATIN CAPITAL LETTER O WITH STROKE
    [u"Ù","%C3%99"], # LATIN CAPITAL LETTER U WITH GRAVE
    [u"Ú","%C3%9A"], # LATIN CAPITAL LETTER U WITH ACUTE
    [u"Û","%C3%9B"], # LATIN CAPITAL LETTER U WITH CIRCUMFLEX
    [u"Ü","%C3%9C"], # LATIN CAPITAL LETTER U WITH DIAERESIS
    [u"Ý","%C3%9D"], # LATIN CAPITAL LETTER Y WITH ACUTE
    [u"Þ","%C3%9E"], # LATIN CAPITAL LETTER THORN
    [u"ß","%C3%9F"], # LATIN SMALL LETTER SHARP S
    [u"à","%C3%A0"], # LATIN SMALL LETTER A WITH GRAVE
    [u"á","%C3%A1"], # LATIN SMALL LETTER A WITH ACUTE
    [u"â","%C3%A2"], # LATIN SMALL LETTER A WITH CIRCUMFLEX
    [u"ã","%C3%A3"], # LATIN SMALL LETTER A WITH TILDE
    [u"ä","%C3%A4"], # LATIN SMALL LETTER A WITH DIAERESIS
    [u"å","%C3%A5"], # LATIN SMALL LETTER A WITH RING ABOVE
    [u"æ","%C3%A6"], # LATIN SMALL LETTER AE
    [u"ç","%C3%A7"], # LATIN SMALL LETTER C WITH CEDILLA
    [u"è","%C3%A8"], # LATIN SMALL LETTER E WITH GRAVE
    [u"ê","%C3%AA"], # LATIN SMALL LETTER E WITH CIRCUMFLEX
    [u"ë","%C3%AB"], # LATIN SMALL LETTER E WITH DIAERESIS
    [u"ì","%C3%AC"], # LATIN SMALL LETTER I WITH GRAVE
    [u"í","%C3%AD"], # LATIN SMALL LETTER I WITH ACUTE
    [u"î","%C3%AE"], # LATIN SMALL LETTER I WITH CIRCUMFLEX
    [u"ï","%C3%AF"], # LATIN SMALL LETTER I WITH DIAERESIS
    [u"ð","%C3%B0"], # LATIN SMALL LETTER ETH
    [u"ñ","%C3%B1"], # LATIN SMALL LETTER N WITH TILDE
    [u"ò","%C3%B2"], # LATIN SMALL LETTER O WITH GRAVE
    [u"ó","%C3%B3"], # LATIN SMALL LETTER O WITH ACUTE
    [u"ô","%C3%B4"], # LATIN SMALL LETTER O WITH CIRCUMFLEX
    [u"õ","%C3%B5"], # LATIN SMALL LETTER O WITH TILDE
    [u"÷","%C3%B7"], # DIVISION SIGNo
    [u"ø","%C3%B8"], # LATIN SMALL LETTER O WITH STROKE
    [u"ú","%C3%BA"], # LATIN SMALL LETTER U WITH ACUTE
    [u"û","%C3%BB"], # LATIN SMALL LETTER U WITH CIRCUMFLEX
    [u"ü","%C3%BC"], # LATIN SMALL LETTER U WITH DIAERESIS
    [u"ý","%C3%BD"], # LATIN SMALL LETTER Y WITH ACUTE
    [u"þ","%C3%BE"], # LATIN SMALL LETTER THORN
    [u"ÿ","%C3%BF"], # LATIN SMALL LETTER Y WITH DIAERESIS
]


def bearEscapeDirectoryName(directoryName):
    for eachEscapement in escapements:
        directoryName = directoryName.replace(eachEscapement[0], eachEscapement[1])

    return directoryName

def bearUnescapeDirectoryName(input_str):
    for eachEscapement in reversed(escapements):
        input_str = input_str.replace(eachEscapement[1], eachEscapement[0])

    return input_str


def wordSubstitutions(filename):

    filename = re.sub('i\.e\.', 'ie', filename, flags=re.IGNORECASE)
    filename = filename.replace("&", " and ")
    filename = filename.replace("@", " at ")

    filename = re.sub('t-shirt', 'tshirt', filename, flags=re.IGNORECASE)
    filename = re.sub('sci-fi', 'scifi', filename, flags=re.IGNORECASE)

    filename = re.sub("'m", ' am ', filename, flags=re.IGNORECASE)

    filename = re.sub("we're", 'we are', filename, flags=re.IGNORECASE)
    filename = re.sub("you're", 'you are', filename, flags=re.IGNORECASE)
    filename = re.sub("they're", 'they are', filename, flags=re.IGNORECASE)

    # 's --------------------------------
    filename = re.sub("that's", "thats", filename, flags=re.IGNORECASE)
    filename = re.sub("let's ", "lets ", filename, flags=re.IGNORECASE)
    filename = re.sub("it's", "it is", filename, flags=re.IGNORECASE)
    filename = re.sub("he's", "he is", filename, flags=re.IGNORECASE)

    filename = re.sub("what's", "what is", filename, flags=re.IGNORECASE)
    filename = re.sub("where's", "where is", filename, flags=re.IGNORECASE)
    filename = re.sub("who's", "who is", filename, flags=re.IGNORECASE)
    filename = re.sub("when's", "when is", filename, flags=re.IGNORECASE)

    filename = re.sub("'s", " ", filename, flags=re.IGNORECASE)
    # -----------------------------------

    filename = re.sub("can't", " cannot", filename, flags=re.IGNORECASE)
    filename = re.sub("n't", " not", filename, flags=re.IGNORECASE)
    filename = re.sub("'ll", " will", filename, flags=re.IGNORECASE)
    filename = re.sub("'ve", " have", filename, flags=re.IGNORECASE)

    filename = filename.replace("...", " and")
    filename = filename.replace("+", "Plus")

    filename = re.sub("C#", "CSharp", filename, flags=re.IGNORECASE)
    filename = re.sub("javascript", "JS", filename, flags=re.IGNORECASE)

    filename = filename.replace("$", "dollar")

    return filename


# adapted from:
# https://gitlab.com/jplusplus/sanitizeFileName-filename/-/blob/master/sanitizeFileName_filename/sanitizeFileName_filename.py

def sanitizeFileNameRemoveExtension(filename):
    return sanitizeFileName(filename[:-3])


def sanitizeFileName(filename):
    """Return a fairly safe version of the filename.

    We don't limit ourselves to ascii, because we want to keep municipality
    names, etc, but we do want to get rid of anything potentially harmful,
    and make sure we do not exceed Windows filename length limits.
    Hence a less safe blacklist, rather than a whitelist.
    """

    reserved = [
        "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5",
        "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5",
        "LPT6", "LPT7", "LPT8", "LPT9",
    ]  # Reserved words on Windows

    filename = "".join(c for c in filename if c != "\0")


    # remove accents
    filename = unicode(remove_accents(filename))

    # TODO must make some of these substitutions case-insensitive
    filename = wordSubstitutions(filename)

    rx = re.compile(r"[\\\/\:\*\?\"\<\>\|\[\]\(\)\"'\. _,!~;\=#%\^{}`]")
    filename = rx.sub('-', filename)

    filename = re.sub("-and-and", "-and", filename, flags=re.IGNORECASE)

    # Remove all characters below code point 32
    filename = "".join(c for c in filename if 31 < ord(c))

    rx = re.compile(r'-+')
    filename = rx.sub('-', filename)
    #filename = re.sub('\_+','_',filename)

    filename = filename.strip('-')


    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.rstrip(". ")  # Windows does not allow these at end
    filename = filename.strip()
    if all([x == "." for x in filename]):
        filename = "__" + filename
    if filename in reserved:
        filename = "__" + filename
    if len(filename) == 0:
        filename = "__"
    if len(filename) > 255:
        parts = re.split(r"/|\\", filename)[-1].split(".")
        if len(parts) > 1:
            ext = "." + parts.pop()
            filename = filename[:-len(ext)]
        else:
            ext = ""
        if filename == "":
            filename = "__"
        if len(ext) > 254:
            ext = ext[254:]
        maxl = 255 - len(ext)
        filename = filename[:maxl]
        filename = filename + ext
        # Re-check last character (if there was no extension)
        filename = filename.rstrip(". ")
        if len(filename) == 0:
            filename = "__"
    return filename

# Print iterations progress, from:
# https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
def printProgress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def changeNoteNameAssetDirNameAndAssetsLinks(actuallyChange, verbose, notesPath, fromName, toName, destinationPath):

    noteFilePath = notesPath + fromName + ".md"

    assetsAbsolutePath = "file://" + os.path.abspath(notesPath) + "/" + "assets/"
    absoluteDestinationPath = "file://" + os.path.abspath(destinationPath) + "/" + "assets/"

    fromName_bearEscaped = bearEscapeDirectoryName(fromName)
    toName_bearEscaped = bearEscapeDirectoryName(toName)


    with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:
        data = file.read()
        data_lower = data.lower()
        file.close()


        data_new = data.replace("]("+ assetsAbsolutePath + fromName_bearEscaped + "/", "]("+ absoluteDestinationPath + toName_bearEscaped + "/")
        data_new = data_new.replace("](assets/" + fromName_bearEscaped + "/", "](assets/" + toName_bearEscaped + "/")

        if data_new != data:
            #print(data_new)
            if actuallyChange:
                with codecs.open(noteFilePath, 'w', encoding='utf-8') as fileW:
                    print(noteFilePath)
                    fileW.write(data_new)
                    fileW.close()

    if fromName != toName:
        print(fromName + " needs name changed to " + toName)

        command = ' [ -d '+ quotePathForShell(notesPath + "assets/" + fromName) +' ] && mv ' + quotePathForShell(notesPath + "assets/" + fromName) + " " + quotePathForShell(notesPath + "assets/" + toName)
        if verbose:
            print("          " + command)
        if actuallyChange:
            call(command, shell=True)

        if len(toName) > len(fromName):
            print('LONGER mv ' + quotePathForShell(notesPath + fromName + ".md") + " " + quotePathForShell(notesPath + toName + ".md"))

        command = 'mv ' + quotePathForShell(notesPath + fromName + ".md") + " " + quotePathForShell(notesPath + toName + ".md")
        if verbose:
            print("          " + command)
        if actuallyChange:
            call(command, shell=True)


def wrapNoteInTagLineAndFooter(actuallyChange, noteFilePath):
    try:
        needsTagLine = False
        needsFooter = False
        with codecs.open(noteFilePath, 'r', encoding='utf-8') as file:

            lines = file.read().splitlines()
            file.close()

            stripEmptyTailLines(lines)

            tag_line = lines[0]

            if tag_line.find("tags:") == -1:
              needsTagLine = True
              lines.insert(0, "tags: ")

            #print(noteFilePath + " > " + tag_line)
            theCreationDate = math.floor(creation_date(noteFilePath))
            theModificationDate = math.floor(modification_date(noteFilePath))
            theAccessDate = math.floor(access_date(noteFilePath))

            last_line = lines[-1]
            if last_line.find("created: ") == -1:
                needsFooter = True
                theCreationDate = math.floor(creation_date(noteFilePath))
                theModificationDate = math.floor(modification_date(noteFilePath))
                theAccessDate = math.floor(access_date(noteFilePath))

                lines.append("")
                lines.append("___")
                lines.append("created: "  + str(datetime.utcfromtimestamp(theCreationDate)) + " modified: " + str(datetime.utcfromtimestamp(theModificationDate)))


            if actuallyChange:
                if needsTagLine or needsFooter:
                    with codecs.open(noteFilePath, 'w', encoding='utf-8') as fileW:
                        fileW.write("\n".join(lines))
                        fileW.close()
                        os.utime(noteFilePath,(theAccessDate, theModificationDate))
            else:
                if needsTagLine or needsFooter:
                    print(noteFilePath)

            if needsTagLine or needsFooter:
                return True
            else:
                return False

    except Exception, e:
        print("ERROR: " + str(e) )