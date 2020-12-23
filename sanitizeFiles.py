from helper_routines import checkPath
from helper_routines import sanitizeFileName
from helper_routines import getNotesFileNames

import sys
import os

notesPath = sys.argv[1]
checkPath(notesPath)

notesFileNames = getNotesFileNames(notesPath)


for noteFileName in notesFileNames:
    noteFileName_Sanitized = sanitizeFileName(noteFileName)
    if noteFileName_Sanitized != noteFileName:
        #print(noteFileName + " -> " + noteFileName_Sanitized)
        print(noteFileName_Sanitized)

    '''
    # USE THIS TO CHECK any remaining unexpected chars
    if not re.match(r'^[A-Za-z0-9-]+$', noteFileName_Sanitized):
        print(noteFileName_Sanitized)
    '''

    '''
    if re.match(r'.*-s-', noteFileName_Sanitized):
        print(noteFileName_Sanitized)

    if re.match(r'.*-re-', noteFileName_Sanitized):
        print(noteFileName_Sanitized)

    if re.match(r'.*-ve-', noteFileName_Sanitized):
        print(noteFileName_Sanitized)

    if re.match(r'.*-ll-', noteFileName_Sanitized):
        print(noteFileName_Sanitized)

    if re.match(r'.*-t-', noteFileName_Sanitized):
        print(noteFileName_Sanitized)
    '''
