# coding=utf-8
# Example:
#    TODO


import sys
import codecs
import re
import string


import argparse
from argparse import RawTextHelpFormatter

import ntpath
import os

# enables to import from upper directory
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import wordSubstitutions
from helper_routines import bearEscapeDirectoryName
from helper_routines import quotePathForShell
from helper_routines import sanitizeFileName
from helper_routines import mySlugify


parser = argparse.ArgumentParser(description="TODO", formatter_class=RawTextHelpFormatter)
parser.add_argument('path', help="note's path")
args = parser.parse_args()




with codecs.open(args.path, 'r', encoding='utf-8') as file:
    theMarkdown = file.read()
    file.close()


newMarkdown = re.sub(r'\s*(@[^\]]*)]\(http', r' \1](http', theMarkdown)


with codecs.open(args.path, 'w', encoding='utf-8') as fileW:
    fileW.write(newMarkdown)
    fileW.close()



