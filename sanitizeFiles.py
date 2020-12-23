from helper_routines import checkPath
from helper_routines import sanitize
from helper_routines import getListOfFiles

import sys
import os

notesPath = sys.argv[1]
checkPath(notesPath)

listOfFiles = getListOfFiles(notesPath)


for eachFile in listOfFiles:
    sanitized = sanitize(eachFile)
    if sanitized != eachFile:
        #print(eachFile + " -> " + sanitized)
        print(sanitized)

    '''
    # USE THIS TO CHECK any remaining unexpected chars
    if not re.match(r'^[A-Za-z0-9-]+$', sanitized):
        print(sanitized)
    '''

    '''
    if re.match(r'.*-s-', sanitized):
        print(sanitized)

    if re.match(r'.*-re-', sanitized):
        print(sanitized)

    if re.match(r'.*-ve-', sanitized):
        print(sanitized)

    if re.match(r'.*-ll-', sanitized):
        print(sanitized)

    if re.match(r'.*-t-', sanitized):
        print(sanitized)
    '''
