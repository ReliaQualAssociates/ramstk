#!/bin/sh

DIRECTORY=${DIRECTORY:-unit}

NOSETESTS=`which nosetests`
CLOC="/home/andrew/.local/bin/cloc"

cd /home/andrew/projects/RTK/tests

unit_test_run() {
	
	TESTFILE=$1
    OUTFILE=`echo $TESTFILE | cut -d '.' -f1 | sed 's/Test//'`

	$NOSETESTS --quiet --with-coverage --cover-branches \
        --cover-min-percentage=80 --cover-tests --with-html \
        --html-file="_test_results/${OUTFILE}UnitTests.html" \
        --attr=unit=True unit/${TESTFILE}

}

integration_test_run() {
	
	TESTFILE=$1
    OUTFILE=`echo $TESTFILE | cut -d '.' -f1 | sed 's/Test//'`

	$NOSETESTS --quiet --with-coverage --cover-branches \
    --cover-min-percentage=80 --cover-tests --with-html \
    --html-file="_test_results/${OUTFILE}IntegrationTests.html" \
    --attr=integration=True integration/${TESTFILE}

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
        -c|--config)
            CONFIG=$2
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
    
    while IFS='' read -r file;
    do
	    unit_test_run $file
    done < "${PWD}/${CONFIG}"

fi

if [ "x$INTEGRATION" != "x" ];
then
	
    while IFS='' read -r file;
    do
        integration_test_run $file
    done < "${PWD}/${CONFIG}"

fi

chown -R andrew.users /home/andrew/projects/RTK/tests/_test_results

exit 0
