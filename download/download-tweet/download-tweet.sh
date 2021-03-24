# Example
#   sh download-tweet.sh ../downloads  "https://twitter.com/ntsutae/status/1367089088315068419"

theNoteName="note-tweet-$RANDOM$RANDOM"

# First part of the pipe:
#   goes to a special twitter "publishing" page that presents an iFrame with the tweet
#   takes screenshot of the tweet
#   downloads iFrame and transforms it to Markdown
#   does some cleanup/fixes/additions to the Markdown
#   downloads any videos and converts them to .gif
#
# Second part of the pipe:
#   downloads all the images related to the tweet so it's all local

theMarkdown=$(node download-tweet.js $1 $2 $theNoteName)
pushd $1
pandoc -f markdown_strict --extract-media $1/assets/$theNoteName  -t markdown_strict -o $theNoteName.md <<< "$theMarkdown"
popd
python final-cleanup-tweet-markdown.py "$1/$theNoteName.md"
python ../../wrap-in-tag-line-and-footer.py "$1/$theNoteName.md"
