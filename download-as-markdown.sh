thefilename="note-$RANDOM$RANDOM"
echo $thefilename
pushd downloaded
readable $1 -l force | sed "s/<figure>//g" | sed "s/<\/figure>//g" | sed "s/<picture/<span/g"  | sed "s/picture>/span>/g" | pandoc -f html  --extract-media ./assets/$thefilename -t markdown | sed "s/{sizes=\"[^}]*//" | sed "s/srcset=\".*}//" | sed "s/<div>//" | sed "s/<\/div>//" | sed "s/:::.*//" > ./$thefilename.md
popd