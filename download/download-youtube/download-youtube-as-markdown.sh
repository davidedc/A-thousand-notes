# The reason we generate intermediate html (and we don't generate directly
# the markdown from the JSON) is that pandoc downloads the preview image
# as well and links it appropriately, which is nice.

# Example:
#   sh download-youtube-as-markdown.sh "https://www.youtube.com/watch?v=zFZ92jySWe0&t=875s" ../downloads3

thefilename="note-youtube-$RANDOM$RANDOM"
echo $thefilename
pushd downloaded
node ../note-from-opengraph.js $1 | python ../make-simple-html-from-opengraph-data.py | pandoc -f html --extract-media ./assets/$thefilename  -t markdown_strict  -o $thefilename.md
popd

rm -r "$2/assets/$thefilename"
mkdir "$2/assets"
mkdir "$2/assets/$thefilename"

mv "downloaded/$thefilename.md" $2/
mv "downloaded/assets/$thefilename" "$2/assets"
