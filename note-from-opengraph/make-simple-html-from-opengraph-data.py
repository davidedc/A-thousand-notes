# Example:
# node note-from-opengraph.js "https://www.youtube.com/watch?v=DjeN1Ea8uns&feature=share" | python make-simple-html-from-opengraph-data.py
#
# The reason we generate intermediate html (and we don't generate directly
# the markdown from the JSON) is that pandoc downloads the preview image
# as well and links it appropriately, which is nice.

import json, sys

obj = json.load(sys.stdin)

print('<!DOCTYPE html>')
print('<html>')

print('<head>')
print('  <title>Youtube - ' + obj['ogTitle'] + '</title>')
print('</head>')

print('<body>')

print('<h1>Youtube - '+ obj['ogTitle'] +'</h1>')
print('<br>')
print('<br>')

print('<img src="' + obj['ogImage']['url'] + '">')
print('<br>')
print('<br>')

print(obj['ogDescription'])
print('<br>')
print('<br>')

print(obj['ogUrl'])


print('</body>')
print('</html>')

