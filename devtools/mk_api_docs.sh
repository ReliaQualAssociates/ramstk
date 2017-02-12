#!/bin/bash

TYPE=$1
BASEDIR='/home/andrew/projects/RTK'
LOGFILE=$BASEDIR/docs/epydoc$TYPE.log

case $TYPE in

	html | HTML)
		echo "Creating html api documentation for RTK."
		epydoc --config $BASEDIR/devtools/confightml > $LOGFILE
		;;
	pdf | PDF)
		echo "Creating pdf api documentation for RTK."
		epydoc --config $BASEDIR/devtools/configpdf > $LOGFILE
		;;
	*)
		echo "Pass an output format to this script."
		echo "Either html or pdf."
		exit 1
		;;
esac

echo "Completed generating $TYPE RTK api documentation."

#echo "Uploading api documentation to RTK website."
#rsync -aiv * weibullguy,reliafree@web.sourceforge.net:/home/project-web/reliafree/htdocs/apidocs/
#echo "Completed uploading api documentation to RTK website."

exit 0
