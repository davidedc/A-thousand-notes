import glob
import unicodedata
import re
import sys
import os

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

# adapted from:
# https://gitlab.com/jplusplus/sanitize-filename/-/blob/master/sanitize_filename/sanitize_filename.py

def sanitize(filename):
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

    rx = re.compile(r"[\\\/\:\*\?\"\<\>\|\[\]\(\)\"'\. _,]")
    filename = rx.sub('-', filename)

    # Remove all charcters below code point 32
    filename = "".join(c for c in filename if 31 < ord(c))

    rx = re.compile(r'-{2,}')
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

fn = sys.argv[1]
if not os.path.exists(fn):
    exit("no such path")

fse = sys.getfilesystemencoding()
listOfFiles = [unicode(x, fse) for x in glob.glob(os.path.normpath(fn) + "/*.md")]


for eachFile in listOfFiles:
	sanitized = sanitize(eachFile)
	if sanitized != eachFile:
		print(eachFile + " -> " + sanitized)
