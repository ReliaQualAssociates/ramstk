#!/bin/sh

NOSETESTS=`which nosetests`
CLOC="/home/andrew/.local/bin/cloc"
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

# Get command line arguments.
while [ $# -gt 0 ];
do
	case "$1" in

        -a|--all)
            ALL=1
            UNIT=1
            INTEGRATION=1
            ;;
		-u|--unit)
			UNIT=1
			DIRECTORY=$2
			;;
        -i|--integration)
			INTEGRATION=1
			DIRECTORY=$2
			;;
	esac
	shift
done

if [ "x$DIRECTORY" == "x" ];
then
	DIRECTORY="allocation dao datamodels failure_definition fmea function
    hardware hazard incident pof requirement revision similar_item
    software stakeholder statistics survival testing usage validation"
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

chown -R andrew.users /home/andrew/projects/RTK/tests/_test_results

exit 0
