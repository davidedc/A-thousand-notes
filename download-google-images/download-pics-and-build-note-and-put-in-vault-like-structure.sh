# Example:
#   sh download-pics-and-build-note-and-put-in-vault-like-structure.sh "Eric Owen Moss" 2
numberOfImages=$2
if [ $# -eq 1 ]
  then
    numberOfImages=10
fi
python3 download-google-images.py "$1" -n $numberOfImages
python create-note-around-images.py "./simple_images/$1"
mv "$1.md" ./downloads/
rm -r "./downloads/assets/$1"
mv "./simple_images/$1" ./downloads/assets/