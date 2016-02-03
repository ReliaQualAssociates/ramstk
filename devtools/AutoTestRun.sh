#!/bin/sh

DIRECTORY=${DIRECTORY:-unit}

NOSETESTS=`which nosetests`
CLOC="/home/andrew/.local/bin/cloc"

cd /home/andrew/projects/RTK/tests

unit_test_run() {
	
	DIRECTORY=$1

	$NOSETESTS --quiet --with-coverage --cover-branches --cover-min-percentage=80 --with-html --html-file="_test_results/${DIRECTORY}_unit_tests.html" --attr=unit=True ./${DIRECTORY}

}

integration_test_run() {
	
	DIRECTORY=$1

	$NOSETESTS --quiet --with-coverage --cover-branches --cover-min-percentage=80 --with-html --html-file="_test_results/${DIRECTORY}_integration_tests.html" --attr=integration=True ./$DIRECTORY
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

if [ "x$UNIT" != "x" ];
then

	unit_test_run $DIRECTORY

fi

if [ "x$INTEGRATION" != "x" ];
then
	
    integration_test_run $DIRECTORY

fi

chown -R andrew.users /home/andrew/projects/RTK/tests/_test_results

exit 0
