#!/usr/bin/sh

curPath=$PWD
testPath=$curPath'/tests'
testList=$testPath'/Test.suites'
excludeList=$testPath'/Excluded.dirs'
logFile=$curPath'/../RTK_test_error.log'

coverage=$(which coverage)
codacy=$(which python-codacy-coverage)
python=$(which python)

echo "BEGIN RTK UNIT TEST EXECUTION ... " > $logFile

# Execute all the unit tests.
while read package file;
do
    printf "EXECUTING UNIT TESTS FOR: $package\n"
    $python $testPath/$file 'all'
    if [ "$?" = "0" ];
    then
        printf "UNIT TESTS FOR $package: SAT\n\n"
        echo "UNIT TESTS FOR $package: SAT" >> $logFile
    else
        printf "UNIT TESTS FOR $package: UNSAT\n\n"
        echo "UNIT TESTS FOR $package: UNSAT" >> $logFile
    fi
done < $testList

# Execute all the integration tests.
#while read package file;
#do
#    printf "EXECUTING INTEGRATION TESTS FOR: $package\n"
#    $nosetest $integrationNoseOpts$package $testPath/$file
#    if [ "$?" = "0" ];
#    then
#        printf "INTEGRATION TESTS FOR $package: SAT\n\n"
#    else
#        printf "INTEGRATION TESTS FOR $package: UNSAT\n\n"
#    fi
#done < $testList

# Create the coverage XML file and upload to codacy.
$coverage xml -o "$curPath/coverage.xml"
$codacy -r "$curPath/coverage.xml"
