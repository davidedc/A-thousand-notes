# Example:
# curl "https://api.microlink.io/?url=https://twitter.com/reactjs/status/912712906407501825" | python make-simple-html-from-opengraph-data2.py
#
# The reason we generate intermediate html (and we don't generate directly
# the markdown from the JSON) is that pandoc downloads the preview image
# as well and links it appropriately, which is nice.

import json, sys

obj = json.load(sys.stdin)

print('<!DOCTYPE html>')
print('<html>')

print('<head>')
print('  <title>Twitter - ' + obj['data']['title'] + '</title>')
print('</head>')

print('<body>')

print('<h1>Twitter - '+ obj['data']['title'] +'</h1>')
print('<br>')
print('<br>')

print('<img src="' + obj['data']['image']['url'] + '">')
print('<br>')
print('<br>')

print(obj['data']['description'])
print('<br>')
print('<br>')

print(obj['data']['url'])


print('</body>')
print('</html>')

