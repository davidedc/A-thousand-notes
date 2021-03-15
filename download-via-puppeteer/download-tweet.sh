# Example
#   sh download-tweet.sh "https://twitter.com/ntsutae/status/1367089088315068419"

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

node download-via-puppeteer-2.js "https://twitter.com/ntsutae/status/1367089088315068419" $theNoteName | pandoc -f markdown_strict --extract-media ./assets/$theNoteName  -t markdown_strict -o $theNoteName.md