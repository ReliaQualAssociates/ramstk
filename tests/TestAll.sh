#!/usr/bin/sh

TESTSUITES='_revision _fmea _function'

# ---------- -------- END OF USER CONFIGURABLE VARIABLES -------- ---------- #
PYTHON=`which python`

function run_test_suites {

    _test=$1
    _return=0

    i=0
    for suite in $TESTSUITES;
    do
        $PYTHON "./$suite/TestPackage.py" $_test
        if [ $? != 0 ];
        then
            RESULTS[$i]="\e[1m\e[31mTEST SUITE ERROR: Test suite $suite failed one or more tests.\e[0m"
            _return=1
            if [ "$BREAK" == "True" ];
            then
                break
            fi
        else
            RESULTS[$i]="\e[1m\e[32mTEST SUITE SUCCESS: Test suite $suite passed all tests.\e[0m"
        fi

        let i++

    done

    return $_return

}

TEST='all'
for i in "$@"
do
    case $i in
        -b|--break)
            BREAK="True"
            shift
            shift
            ;;
        -t=|--test=*)
            TEST="${i#*=}"
            shift
            ;;
        -t|--test)
            TEST=$2
            shift
            shift
            ;;
        *)
            TEST='all'
            ;;
    esac
done

run_test_suites $TEST

echo -e "\n\e[1m\e[107m\e[34m# ----- ----- TEST SUITE RESULTS ----- ----- #\e[0m\n"
for i in "${RESULTS[@]}";
do
    echo -e $i
done

exit 0
