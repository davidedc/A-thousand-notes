# coding=utf-8
#
# As Pandoc downloads all the assets related to the tweet, for some strange reason it mangles the markdown
# of the tweet slightly. This script adjusts those defects.
#
# Example:
#    python final-cleanup-tweet-markdown.py path-of-note


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


parser = argparse.ArgumentParser(description="clean up some defects introduced by pandoc as it downloads the assets related to the tweet", formatter_class=RawTextHelpFormatter)
parser.add_argument('path', help="note's path")
args = parser.parse_args()




with codecs.open(args.path, 'r', encoding='utf-8') as file:
    theMarkdown = file.read()
    file.close()

newMarkdown = theMarkdown

# fix author's link gets broken over two lines
newMarkdown = re.sub(r'\s*(@[^\]]*)]\(http', r' \1](http', newMarkdown)
# fix date of tweet link broken over two lines
newMarkdown = re.sub(r'\n*(20[0-9][0-9])\]\(http', r' \1](http', newMarkdown)



with codecs.open(args.path, 'w', encoding='utf-8') as fileW:
    fileW.write(newMarkdown)
    fileW.close()



