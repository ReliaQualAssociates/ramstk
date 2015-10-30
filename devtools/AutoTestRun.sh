#!/bin/sh

NOSETESTS=`which nosetests`
CLOC=`which cloc`
ALL=0

cd /home/andrew/projects/RTK/tests

unit_test_run() {
	
	DIRECTORY=$1

	$NOSETESTS --quiet --with-coverage --cover-branches --with-html --html-file="_test_results/${DIRECTORY}_unit_tests.html" --attr=unit=True ./${DIRECTORY}

}

integration_test_run() {
	
	DIRECTORY=$1

	$NOSETESTS --quiet --with-coverage --cover-branches --with-html --html-file="_test_results/${DIRECTORY}_integration_tests.html" --attr=integration=True ./$DIRECTORY
}

cloc_run() {

    cd _test_results/

	$CLOC --by-file --xsl=cloc.xsl --report_file=code_count.xml ../../rtk

    cd ../

}

# Get command line arguments.
while [ $# -gt 0 ];
do
	case "$1" in

		-u|--unit)
			UNIT=1
			DIRECTORY=$2
			;;
        -i|--integration)
			INTEGRATION=1
			DIRECTORY=$2
			;;
		-c|--cloc)
			RUNCLOC=1
			;;
	esac
	shift
done

if [ "x$DIRECTORY" == "x" ];
then
	DIRECTORY="allocation dao datamodels failure_definition function hardware incident requirement revision software stakeholder survival testing usage validation"
	ALL=1
fi

if [ "x$UNIT" != "x" ];
then

	if [ "x$ALL" == "x0" ];
	then
	    unit_test_run $DIRECTORY
	else
		for dir in $DIRECTORY; 
		do
			unit_test_run $dir
		done
	fi

fi

if [ "x$INTEGRATION" != "x" ];
then
	
	if [ "x$ALL" == "x0" ];
	then
	    integration_test_run $DIRECTORY
	else
		for dir in $DIRECTORY; 
		do
			integration_test_run $dir
		done
	fi

fi

if [ "x$RUNCLOC" != "x" ];
then
	cloc_run
fi

exit 0
