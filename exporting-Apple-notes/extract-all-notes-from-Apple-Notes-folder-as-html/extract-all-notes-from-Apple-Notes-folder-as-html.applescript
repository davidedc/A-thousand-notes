# from https://gist.github.com/jthigpen/5067358
# takes an Apple Notes folder and extracts all its notes into html in a single TextEdit window
# you can then save as an html, and/or manipulate further.
# There is another more complex script of this kind on github
#   https://github.com/mattrose/AppleNotes2Joplin/blob/main/AppleNotes2Joplin.applescript
# however it doesn't quite work for me.

tell application "TextEdit"
	activate
	make new document
end tell


tell application "Notes"
	if folder "Twitter links" exists then
		set output to ""
		repeat with aNote in notes in folder "Twitter links"
			set noteText to "<!-- ### Start Note ### -->
"
			set noteText to noteText & ("<h1>" & name of aNote as string) & "</h1>
"
			#set noteText to noteText & ("<p>Creation Date: " & creation date of aNote as string) & "</p>"
			#set noteText to noteText & ("<p>Modification Date: " & modification date of aNote as string) & "</p>"
			set noteText to (noteText & body of aNote as string) & "

"
			
			tell application "TextEdit"
				activate
				set oldText to text of document 1
				set text of document 1 to oldText & noteText
			end tell
			
		end repeat
	else
		display dialog "Aww!"
	end if
end tell