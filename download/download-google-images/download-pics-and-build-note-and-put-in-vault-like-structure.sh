# Example:
#   sh download-pics-and-build-note-and-put-in-vault-like-structure.sh "Eric Owen Moss" ../downloads 2
numberOfImages=$3
if [ $# -eq 2 ]
  then
    numberOfImages=10
fi
python3 download-google-images.py "$1" -n $numberOfImages
python create-note-around-images.py "./simple_images/$1"

rm -r "$2/assets/$1"
mkdir "$2/assets"
mkdir "$2/assets/$1"

mv "$1.md" $2/
mv "./simple_images/$1" "$2/assets"

newName=$(python ../../find-suitable-unused-slugified-name.py "$2/$1.md" -v ../../../../Davide/notes-vault/)
echo $newName

python ../../change-note-name-asset-dir-name-and-assets-links.py $2 -f -o "$1" -n $newName
python ../../wrap-in-tag-line-and-footer.py "$2/$newName.md"