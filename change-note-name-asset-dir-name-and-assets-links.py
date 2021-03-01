# coding=utf-8

from helper_routines import checkPath
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




parser = argparse.ArgumentParser(description="My parser")
parser.add_argument('path')
parser.add_argument('-f', '--fix-name-and-assets-links', action='store_true')

parser.add_argument('-o', '--old-name')
parser.add_argument('-n', '--new-name')
parser.add_argument('-v', '--verbose')
parser.add_argument('-p', '--new-path')

args = parser.parse_args()

notesPath = os.path.join(args.path, '') # add trailing slash if it's not there
checkPath(notesPath)

if args.new_path is None:
    args.new_path = args.path

if args.old_name.endswith(".md"):
    args.old_name = args.old_name[:-3]

if args.new_name.endswith(".md"):
    args.new_name = args.new_name[:-3]

changeNoteNameAssetDirNameAndAssetsLinks(args.fix_name_and_assets_links, args.verbose, notesPath, args.old_name, args.new_name, args.new_path)
#raw_input("Press Enter to continue...")

