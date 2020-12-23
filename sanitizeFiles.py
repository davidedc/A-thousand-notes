from helper_routines import checkPath
import sys
import os
import glob
import ntpath

notesPath = sys.argv[1]
checkPath(notesPath)

fse = sys.getfilesystemencoding()
listOfFiles = [unicode(ntpath.basename(x), fse) for x in glob.glob(os.path.normpath(notesPath) + "/*.md")]


for eachFile in listOfFiles:
    sanitized = helper_routines.sanitize(eachFile)
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
