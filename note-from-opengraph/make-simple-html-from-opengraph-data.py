# example:
# node note-from-opengraph.js "https://www.youtube.com/watch?v=DjeN1Ea8uns&feature=share" | python make-simple-html-from-opengraph-data.py

import json, sys

obj = json.load(sys.stdin)

print('<html>')
print('<img src="' + obj['ogImage']['url'] + '">')
print('</html>')
