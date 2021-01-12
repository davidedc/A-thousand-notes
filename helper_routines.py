# coding=utf-8

import unicodedata
import re
import os
import sys
import glob
import ntpath

from os import listdir
from os.path import isfile, join


def quotePathForShell(thePath):
    return '"' + thePath.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`') + '"'

def stripEmptyTailLines(lines):
    while lines[-1].strip() == "":
      del lines[-1]

def getNotesFileNames(notesPath):
    fse = sys.getfilesystemencoding()
    return [unicode(ntpath.basename(x), fse) for x in glob.glob(os.path.normpath(notesPath) + "/*.md")]

def getFileNames(path):
    #fse = sys.getfilesystemencoding()
    #return [ntpath.basename(x) for x in glob.glob(os.path.normpath(path) + "/*")]
    return [f for f in listdir(path) if isfile(join(path, f))]


def getAttachmentsDirectoryNames(notesPath):
    fse = sys.getfilesystemencoding()
    return [unicode(ntpath.basename(os.path.normpath(x)), fse) for x in glob.glob(os.path.normpath(notesPath) + "/*/")]

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


def bearEscapeDirectoryName(directoryName):
    directoryName = directoryName.replace("%", "%25")
    directoryName = directoryName.replace(" ", "%20")
    directoryName = directoryName.replace('"',"%22")
    directoryName = directoryName.replace(u"|","%7C")
    #directoryName = directoryName.replace(u"?","%3F")

    #directoryName = directoryName.replace(u"'","%27")


    directoryName = directoryName.replace(u"’","%E2%80%99")
    directoryName = directoryName.replace(u"–","%E2%80%93")
    directoryName = directoryName.replace(u"—","%E2%80%94")
    directoryName = directoryName.replace(u"“","%E2%80%9C")
    directoryName = directoryName.replace(u"”","%E2%80%9D")

    directoryName = directoryName.replace(u"ō","o%CC%84")
    directoryName = directoryName.replace(u"ö","%C3%B6") # LATIN SMALL LETTER O WITH DIAERESIS
    directoryName = directoryName.replace(u"é","%C3%A9") # LATIN SMALL LETTER E WITH ACUTE
    directoryName = directoryName.replace(u"™","%E2%84%A2")
    directoryName = directoryName.replace(u"<","%3C")
    directoryName = directoryName.replace(u">","%3E")
    directoryName = directoryName.replace(u"#","%23")
    directoryName = directoryName.replace(u"…","%E2%80%A6")
    directoryName = directoryName.replace(u"ü","%C3%BC")
    directoryName = directoryName.replace(u"ù","%C3%B9") # LATIN SMALL LETTER U WITH GRAVE
    directoryName = directoryName.replace(u"[","%5B")
    directoryName = directoryName.replace(u"]","%5D")
    directoryName = directoryName.replace(u"í","%C3%AD")
    directoryName = directoryName.replace(u"•","%E2%80%A2")
    directoryName = directoryName.replace(u"à","%C3%A0")
    directoryName = directoryName.replace(u"å","%C3%A5")
    directoryName = directoryName.replace(u"è","%C3%A8")
    directoryName = directoryName.replace(u"ó","%C3%B3")
    directoryName = directoryName.replace(u"＃","%EF%BC%83")
    directoryName = directoryName.replace(u"^","%5E")
    directoryName = directoryName.replace(u"‘","%E2%80%98")
    directoryName = directoryName.replace(u"ï","%C3%AF")
    directoryName = directoryName.replace(u"ñ","%C3%B1")

    directoryName = directoryName.replace(u"á","%C3%A1")
    directoryName = directoryName.replace(u"⋆","%E2%8B%86")
    directoryName = directoryName.replace(u"🤓","%F0%9F%A4%93")
    directoryName = directoryName.replace(u"ë","%C3%AB")
    directoryName = directoryName.replace(u"Š","%C5%A0")

    directoryName = directoryName.replace(u"‒","%E2%80%92")
    directoryName = directoryName.replace(u"★","%E2%98%85")
    directoryName = directoryName.replace(u"λ","%CE%BB")
    directoryName = directoryName.replace(u"ç","%C3%A7")
    directoryName = directoryName.replace(u"″","%E2%80%B3")
    directoryName = directoryName.replace(u"ý","%C3%BD")
    directoryName = directoryName.replace(u"π","%CF%80")
    directoryName = directoryName.replace(u"É","%C3%89")
    directoryName = directoryName.replace(u"œ","%C5%93")
    directoryName = directoryName.replace(u"ä","%C3%A4")
    directoryName = directoryName.replace(u"ü","%C3%BC")
    directoryName = directoryName.replace(u"ł","%C5%82")
    directoryName = directoryName.replace(u"Č","%C4%8C")
    directoryName = directoryName.replace(u"ć","%C4%87")
    directoryName = directoryName.replace(u"Ř","%C5%98")
    directoryName = directoryName.replace(u"í","%C3%AD")
    directoryName = directoryName.replace(u"ì","%C3%AC")
    directoryName = directoryName.replace(u"ý","%C3%BD")
    directoryName = directoryName.replace(u"ò","%C3%B2")
    directoryName = directoryName.replace(u"›","%E2%80%BA")
    directoryName = directoryName.replace(u"Ö","%C3%96")
    directoryName = directoryName.replace(u"⁓","%E2%81%93")


    directoryName = directoryName.replace(u"¡","%C2%A1") # INVERTED EXCLAMATION MARK
    directoryName = directoryName.replace(u"¢","%C2%A2") # CENT SIGN
    directoryName = directoryName.replace(u"£","%C2%A3") # POUND SIGN
    directoryName = directoryName.replace(u"¤","%C2%A4") # CURRENCY SIGN
    directoryName = directoryName.replace(u"¥","%C2%A5") # YEN SIGN
    directoryName = directoryName.replace(u"¦","%C2%A6") # BROKEN BAR
    directoryName = directoryName.replace(u"§","%C2%A7") # SECTION SIGN
    directoryName = directoryName.replace(u"¨","%C2%A8") # DIAERESIS
    directoryName = directoryName.replace(u"©","%C2%A9") # COPYRIGHT SIGN
    directoryName = directoryName.replace(u"ª","%C2%AA") # FEMININE ORDINAL INDICATOR
    directoryName = directoryName.replace(u"«","%C2%AB") # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    directoryName = directoryName.replace(u"¬","%C2%AC") # NOT SIGN
    directoryName = directoryName.replace(u"®","%C2%AE") # REGISTERED SIGN
    directoryName = directoryName.replace(u"¯","%C2%AF") # MACRON
    directoryName = directoryName.replace(u"°","%C2%B0") # DEGREE SIGN
    directoryName = directoryName.replace(u"±","%C2%B1") # PLUS-MINUS SIGN
    directoryName = directoryName.replace(u"²","%C2%B2") # SUPERSCRIPT TWO
    directoryName = directoryName.replace(u"³","%C2%B3") # SUPERSCRIPT THREE
    directoryName = directoryName.replace(u"´","%C2%B4") # ACUTE ACCENT
    directoryName = directoryName.replace(u"µ","%C2%B5") # MICRO SIGN
    directoryName = directoryName.replace(u"¶","%C2%B6") # PILCROW SIGN
    directoryName = directoryName.replace(u"·","%C2%B7") # MIDDLE DOT
    directoryName = directoryName.replace(u"¸","%C2%B8") # CEDILLA
    directoryName = directoryName.replace(u"¹","%C2%B9") # SUPERSCRIPT ONE
    directoryName = directoryName.replace(u"º","%C2%BA") # MASCULINE ORDINAL INDICATOR
    directoryName = directoryName.replace(u"»","%C2%BB") # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    directoryName = directoryName.replace(u"¼","%C2%BC") # VULGAR FRACTION ONE QUARTER
    directoryName = directoryName.replace(u"½","%C2%BD") # VULGAR FRACTION ONE HALF
    directoryName = directoryName.replace(u"¾","%C2%BE") # VULGAR FRACTION THREE QUARTERS
    directoryName = directoryName.replace(u"¿","%C2%BF") # INVERTED QUESTION MARK
    directoryName = directoryName.replace(u"À","%C3%80") # LATIN CAPITAL LETTER A WITH GRAVE
    directoryName = directoryName.replace(u"Á","%C3%81") # LATIN CAPITAL LETTER A WITH ACUTE
    directoryName = directoryName.replace(u"Â","%C3%82") # LATIN CAPITAL LETTER A WITH CIRCUMFLEX
    directoryName = directoryName.replace(u"Ã","%C3%83") # LATIN CAPITAL LETTER A WITH TILDE
    directoryName = directoryName.replace(u"Ä","%C3%84") # LATIN CAPITAL LETTER A WITH DIAERESIS
    directoryName = directoryName.replace(u"Å","%C3%85") # LATIN CAPITAL LETTER A WITH RING ABOVE
    directoryName = directoryName.replace(u"Æ","%C3%86") # LATIN CAPITAL LETTER AE
    directoryName = directoryName.replace(u"Ç","%C3%87") # LATIN CAPITAL LETTER C WITH CEDILLA
    directoryName = directoryName.replace(u"È","%C3%88") # LATIN CAPITAL LETTER E WITH GRAVE
    directoryName = directoryName.replace(u"É","%C3%89") # LATIN CAPITAL LETTER E WITH ACUTE
    directoryName = directoryName.replace(u"Ê","%C3%8A") # LATIN CAPITAL LETTER E WITH CIRCUMFLEX
    directoryName = directoryName.replace(u"Ë","%C3%8B") # LATIN CAPITAL LETTER E WITH DIAERESIS
    directoryName = directoryName.replace(u"Ì","%C3%8C") # LATIN CAPITAL LETTER I WITH GRAVE
    directoryName = directoryName.replace(u"Í","%C3%8D") # LATIN CAPITAL LETTER I WITH ACUTE
    directoryName = directoryName.replace(u"Î","%C3%8E") # LATIN CAPITAL LETTER I WITH CIRCUMFLEX
    directoryName = directoryName.replace(u"Ï","%C3%8F") # LATIN CAPITAL LETTER I WITH DIAERESIS
    directoryName = directoryName.replace(u"Ð","%C3%90") # LATIN CAPITAL LETTER ETH
    directoryName = directoryName.replace(u"Ñ","%C3%91") # LATIN CAPITAL LETTER N WITH TILDE
    directoryName = directoryName.replace(u"Ò","%C3%92") # LATIN CAPITAL LETTER O WITH GRAVE
    directoryName = directoryName.replace(u"Ó","%C3%93") # LATIN CAPITAL LETTER O WITH ACUTE
    directoryName = directoryName.replace(u"Ô","%C3%94") # LATIN CAPITAL LETTER O WITH CIRCUMFLEX
    directoryName = directoryName.replace(u"Õ","%C3%95") # LATIN CAPITAL LETTER O WITH TILDE
    directoryName = directoryName.replace(u"Ö","%C3%96") # LATIN CAPITAL LETTER O WITH DIAERESIS
    directoryName = directoryName.replace(u"×","%C3%97") # MULTIPLICATION SIGN
    directoryName = directoryName.replace(u"Ø","%C3%98") # LATIN CAPITAL LETTER O WITH STROKE
    directoryName = directoryName.replace(u"Ù","%C3%99") # LATIN CAPITAL LETTER U WITH GRAVE
    directoryName = directoryName.replace(u"Ú","%C3%9A") # LATIN CAPITAL LETTER U WITH ACUTE
    directoryName = directoryName.replace(u"Û","%C3%9B") # LATIN CAPITAL LETTER U WITH CIRCUMFLEX
    directoryName = directoryName.replace(u"Ü","%C3%9C") # LATIN CAPITAL LETTER U WITH DIAERESIS
    directoryName = directoryName.replace(u"Ý","%C3%9D") # LATIN CAPITAL LETTER Y WITH ACUTE
    directoryName = directoryName.replace(u"Þ","%C3%9E") # LATIN CAPITAL LETTER THORN
    directoryName = directoryName.replace(u"ß","%C3%9F") # LATIN SMALL LETTER SHARP S
    directoryName = directoryName.replace(u"à","%C3%A0") # LATIN SMALL LETTER A WITH GRAVE
    directoryName = directoryName.replace(u"á","%C3%A1") # LATIN SMALL LETTER A WITH ACUTE
    directoryName = directoryName.replace(u"â","%C3%A2") # LATIN SMALL LETTER A WITH CIRCUMFLEX
    directoryName = directoryName.replace(u"ã","%C3%A3") # LATIN SMALL LETTER A WITH TILDE
    directoryName = directoryName.replace(u"ä","%C3%A4") # LATIN SMALL LETTER A WITH DIAERESIS
    directoryName = directoryName.replace(u"å","%C3%A5") # LATIN SMALL LETTER A WITH RING ABOVE
    directoryName = directoryName.replace(u"æ","%C3%A6") # LATIN SMALL LETTER AE
    directoryName = directoryName.replace(u"ç","%C3%A7") # LATIN SMALL LETTER C WITH CEDILLA
    directoryName = directoryName.replace(u"è","%C3%A8") # LATIN SMALL LETTER E WITH GRAVE
    directoryName = directoryName.replace(u"ê","%C3%AA") # LATIN SMALL LETTER E WITH CIRCUMFLEX
    directoryName = directoryName.replace(u"ë","%C3%AB") # LATIN SMALL LETTER E WITH DIAERESIS
    directoryName = directoryName.replace(u"ì","%C3%AC") # LATIN SMALL LETTER I WITH GRAVE
    directoryName = directoryName.replace(u"í","%C3%AD") # LATIN SMALL LETTER I WITH ACUTE
    directoryName = directoryName.replace(u"î","%C3%AE") # LATIN SMALL LETTER I WITH CIRCUMFLEX
    directoryName = directoryName.replace(u"ï","%C3%AF") # LATIN SMALL LETTER I WITH DIAERESIS
    directoryName = directoryName.replace(u"ð","%C3%B0") # LATIN SMALL LETTER ETH
    directoryName = directoryName.replace(u"ñ","%C3%B1") # LATIN SMALL LETTER N WITH TILDE
    directoryName = directoryName.replace(u"ò","%C3%B2") # LATIN SMALL LETTER O WITH GRAVE
    directoryName = directoryName.replace(u"ó","%C3%B3") # LATIN SMALL LETTER O WITH ACUTE
    directoryName = directoryName.replace(u"ô","%C3%B4") # LATIN SMALL LETTER O WITH CIRCUMFLEX
    directoryName = directoryName.replace(u"õ","%C3%B5") # LATIN SMALL LETTER O WITH TILDE
    directoryName = directoryName.replace(u"÷","%C3%B7") # DIVISION SIGNo
    directoryName = directoryName.replace(u"ø","%C3%B8") # LATIN SMALL LETTER O WITH STROKE
    directoryName = directoryName.replace(u"ú","%C3%BA") # LATIN SMALL LETTER U WITH ACUTE
    directoryName = directoryName.replace(u"û","%C3%BB") # LATIN SMALL LETTER U WITH CIRCUMFLEX
    directoryName = directoryName.replace(u"ü","%C3%BC") # LATIN SMALL LETTER U WITH DIAERESIS
    directoryName = directoryName.replace(u"ý","%C3%BD") # LATIN SMALL LETTER Y WITH ACUTE
    directoryName = directoryName.replace(u"þ","%C3%BE") # LATIN SMALL LETTER THORN
    directoryName = directoryName.replace(u"ÿ","%C3%BF") # LATIN SMALL LETTER Y WITH DIAERESIS

    return directoryName


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

    filename = filename[:-3]

    # remove accents
    filename = unicode(remove_accents(filename))

    # TODO must make some of these substitutions case-insensitive
    filename = wordSubstitutions(filename)

    rx = re.compile(r"[\\\/\:\*\?\"\<\>\|\[\]\(\)\"'\. _,!~;\=#%\^{}`]")
    filename = rx.sub('-', filename)

    filename = re.sub("-and-and", "-and", filename, flags=re.IGNORECASE)

    # Remove all charcters below code point 32
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
