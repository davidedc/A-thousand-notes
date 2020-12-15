import unicodedata
import re

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

    # TODO must make some of these substitutions case-insensitive

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

    filename = re.sub("C#", "C sharp", filename, flags=re.IGNORECASE)

    filename = filename.replace("$", "dollar")

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
