### Background

In Q4 2020 Evernote released version 10 of their client. To my dismay, this version wasn't sufficiently performant with as many notes as I had (Evernote probably decided to target a faster-growing segment). Also the client came with limitations on how many notes one could export at one time.

Luckily, Evernote still supported a legacy client, from which I could bulk-export all 28k notes. Using Bear on OSX, I could then import the Evernote export, and export all the notes in markdown.



### Migration cleanup scripts

The resulting markdown (+ assets) notes have some problems:

* notes with the same title have their assets in the same directory
* note file names contain all kind of automation-unfriendly special characters (emojis, ideographic etc.)
* some assets are linked using html instead of markdown

these scripts help in resolving these problems.



### Workflow scripts

A "plain" markdown solution makes it possible  to automate many workflows - this repo contains (or will contain) scripts for these workflows.

For example:

* finding keywords and extracting text "around" their occurrences
* NLP workflows e.g. automatic summarisation, automatic duplicates finding, automatic tagging
* finding spelling mistakes across all notes
* finding deletable content across all notes (e.g. social media sharing headers, chumbox links etc.)
* scripts to (bulk) change/restore the creation/update date/time of the notes