# coding=utf-8

import sys
import os
import glob
import ntpath
import codecs

fn = sys.argv[1]
if not os.path.exists(fn):
    exit("no such path")

fse = sys.getfilesystemencoding()


#print listOfDirectories

listOfFiles = [unicode(ntpath.basename(x), fse) for x in glob.glob(os.path.normpath(fn) + "/*.md")]

print(listOfFiles)

for eachFile in listOfFiles:
    tryingToFindTheMdFile = fn + "/" + eachFile
    try:
        #print(tryingToFindTheMdFile)
        with codecs.open(tryingToFindTheMdFile, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()

            data = data.replace(u"![](",u"![](assets/")

            with codecs.open(tryingToFindTheMdFile, 'w', encoding='utf-8') as fileW:
                print(tryingToFindTheMdFile)
                fileW.write(data)
                fileW.close()
                #raw_input("Press Enter to continue...")
    except:
        print("EXCEPTION")
