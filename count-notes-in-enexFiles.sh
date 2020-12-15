#!/bin/zsh

# example sh ./count-notes-in-enexFiles.sh ../../../Public/
grep -o "<note>"  $1/*.enex | wc -l