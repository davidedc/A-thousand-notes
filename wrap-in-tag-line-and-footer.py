# coding=utf-8

from helper_routines import creation_date
from helper_routines import modification_date
from helper_routines import access_date
from helper_routines import checkPath
from helper_routines import getNotesFileNames
from helper_routines import stripEmptyTailLines
from helper_routines import wrapNoteInTagLineAndFooter

import sys
import os
import codecs
from datetime import datetime
import math


import argparse
import time


parser = argparse.ArgumentParser(description="My parser")
parser.add_argument('path')
args = parser.parse_args()

noteFilePath = args.path
checkPath(noteFilePath)


wrapNoteInTagLineAndFooter(True, noteFilePath)
