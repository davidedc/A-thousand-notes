#!/bin/zsh

# example sh ./count-md-files-in-dir.sh ../../../Public/
ls $1 | grep "\.md$" |  wc -l