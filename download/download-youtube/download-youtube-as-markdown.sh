# The reason we generate intermediate html (and we don't generate directly
# the markdown from the JSON) is that pandoc downloads the preview image
# as well and links it appropriately, which is nice.

thefilename="note-youtube-$RANDOM$RANDOM"
echo $thefilename
pushd downloaded
node ../note-from-opengraph.js $1 | python ../make-simple-html-from-opengraph-data.py | pandoc -f html --extract-media ./assets/$thefilename  -t markdown_strict  -o $thefilename.md
popd

