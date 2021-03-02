#!/bin/bash

# Example:
#   sh mv-note.sh ./download-google-images/downloads/fake-vault ./download-google-images/downloads/*.md

destPath="$1"

shift

for var in "$@"
do

	srcPath="$(dirname "${var}")"

    filename="$(basename "${var}")"
    filenameWithoutExtension="${filename%.md}"

    #echo srcPath is "$srcPath"
    #echo filenameWithoutExtension is "$filenameWithoutExtension"

    if [ -d "$srcPath/assets/$filenameWithoutExtension" ] 
    then
        echo python change-note-name-asset-dir-name-and-assets-links.py "$srcPath" -f -o "$filenameWithoutExtension" -n "$filenameWithoutExtension" -p "$destPath"
        python change-note-name-asset-dir-name-and-assets-links.py "$srcPath" -f -o "$filenameWithoutExtension" -n "$filenameWithoutExtension" -p "$destPath"
        mkdir -p "$destPath/assets/"
        mv "$srcPath/assets/$filenameWithoutExtension" "$destPath/assets/"
    fi
    mv "$var" "$destPath"

done
