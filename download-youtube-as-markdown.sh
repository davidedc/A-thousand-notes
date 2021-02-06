thefilename="note-youtube-$RANDOM$RANDOM"
echo $thefilename
pushd downloaded
pandoc -f html $1 --extract-media ./assets/$thefilename  -t markdown_strict  -o $thefilename.md
popd