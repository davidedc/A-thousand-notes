# Example
#   sh download-tweet.sh "https://twitter.com/ntsutae/status/1367089088315068419"

theNoteName="note-tweet-$RANDOM$RANDOM"
node download-via-puppeteer-2.js "https://twitter.com/ntsutae/status/1367089088315068419" $theNoteName | pandoc -f markdown_strict --extract-media ./assets/$theNoteName  -t markdown_strict -o $theNoteName.md