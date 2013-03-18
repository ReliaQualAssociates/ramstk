#!/bin/bash

# Utility script for RelKit developers to update the messages.pot file,
# create, and merge new translation files.

INFILE="file.lst"					# File with list of files to process.
OUTFILE="../locale/messages.pot"		# .pot file for messages.

XGETTEXT=`which xgettext`			# Find xgettext

${XGETTEXT} -k_ -kN_ --language=Python --output=${OUTFILE} --files-from=${INFILE}

exit 0
