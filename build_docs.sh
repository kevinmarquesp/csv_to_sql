#!/usr/bin/env bash

MODULE="csv_to_sql/"
README="README.md"
REGEX='^ *<!-- *{{ *PYDOC_MARKDOWN *}} *--> *$'

cp "${README}" "${README}.temp"

awk "1; /${REGEX}/ { exit; }" "${README}.temp" > "${README}"
rm "${README}.temp"

pydoc-markdown -p "${SRC}" -I $(pwd) |
	sed '/^ *# *.*$/d;/^<a *.*$/d;/./,$!d' >> "${README}"
