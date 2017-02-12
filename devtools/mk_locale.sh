#!/bin/bash

# Utility script for RTK developers to update the messages.pot file,
# create, and merge new translation files.

INFILE="/home/andrew/projects/RTK/devtools/file.lst"    # File with list of files to process.
OUTFILE="/home/andrew/projects/RTK/po/rtk.pot"		    # *.pot file for messages.

XGETTEXT=`which xgettext`			                    # Find xgettext

${XGETTEXT} -k_ -kN_ --language=Python --output=${OUTFILE} --files-from=${INFILE}

exit 0
