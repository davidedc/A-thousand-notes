# coding=utf-8

from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import wordSubstitutions
from helper_routines import bearEscapeDirectoryName
from helper_routines import quotePathForShell
from helper_routines import sanitizeFileName
from helper_routines import changeNoteNameAssetDirNameAndAssetsLinks


from slugify import slugify

import sys
import codecs
import re
import string

from subprocess import call

import argparse
import os


NOTES_ABSOLUTE_PATH = "file:///Users/davidedellacasa/Public/10000notes/"
ASSETS_ABSOLUTE_PATH = NOTES_ABSOLUTE_PATH + "assets/"


parser = argparse.ArgumentParser(description="My parser")
parser.add_argument('path')
parser.add_argument('-f', '--fix-name-and-assets-links', action='store_true')

parser.add_argument('-o', '--old-name')
parser.add_argument('-n', '--new-name')
parser.add_argument('-v', '--verbose')

args = parser.parse_args()

notesPath = os.path.join(args.path, '') # add trailing slash if it's not there
checkPath(notesPath)

notesFileNames = getNotesFileNames(notesPath)
newNotesFilesNames = []


changeNoteNameAssetDirNameAndAssetsLinks(args.fix_name_and_assets_links, args.verbose, ASSETS_ABSOLUTE_PATH, notesPath, args.old_name, args.new_name)
#raw_input("Press Enter to continue...")

