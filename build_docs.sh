#!/usr/bin/env sh

SRC="csv_to_sql/"

echo "warning: you need to has the pydoc-markdown library installed for that"
echo "         ---> python3 -m pip install pydoc-markdown"

pydoc-markdown -p "${SRC}" -I $(pwd) |
	sed '/^ *# *.*$/d;/^<a *.*$/d;/./,$!d' > README.md
