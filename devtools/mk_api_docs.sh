#!/bin/bash

TYPE=$1
LOGFILE=`pwd`/epydoc$TYPE.log

case $TYPE in

	html | HTML)
		echo "Creating html api documentation for RelKit."
		epydoc --config `pwd`/devtools/confightml > $LOGFILE
		;;
	pdf | PDF)
		echo "Creating pdf api documentation for RelKit."
		epydoc --config `pwd`/devtools/configpdf > $LOGFILE
		;;
	*)
		echo "Pass an output format to this script."
		echo "Either html or pdf."
		exit 1
		;;
esac

echo "Completed generating $TYPE RelKit api documentation."

echo "Uploading api documentation to RelKit website."
rsync -aiv * weibullguy,reliafree@web.sourceforge.net:/home/project-web/reliafree/htdocs/apidocs/
echo "Completed uploading api documentation to RelKit website."

exit 0
