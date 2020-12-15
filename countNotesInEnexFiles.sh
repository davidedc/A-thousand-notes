#!/bin/zsh

# example sh ./countNotesInEnexFiles.sh ../../../Public/
grep -o "<note>"  $1/*.enex | wc -l