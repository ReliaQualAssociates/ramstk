#!/usr/bin/sh

export CODACY_PROJECT_TOKEN=9ef97176f7504721a0f3ec251bf51c19

curPath=$PWD
projPath=$HOME'/drive_d/projects/RTK'
testPath=$curPath'/tests'
testList=$testPath'/unit/Unit.tests'
excludeList=$testPath'/Excluded.dirs'
logFile=$curPath'/../RTK_test_error.log'

noseOpts="-c $curPath/setup.cfg --exclude-dir-file=$excludedList"
unitNoseOpts="$noseOpts --attr=unit=True --cover-package="
integrationNoseOpts="$noseOpts --attr=integration=True --cover-package="

nosetest=$(which nosetests)
coverage=$(which coverage)
codacy=$(which python-codacy-coverage)

echo "BEGIN RTK UNIT TEST EXECUTION ... " > $logFile

# Execute all the unit tests.
while read package file;
do
    printf "EXECUTING UNIT TESTS FOR: $package\n"
    $nosetest $unitNoseOpts$package $testPath/$file
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
$coverage xml -o "$curPath/tests/coverage.xml"
$codacy -r "$curPath/tests/coverage.xml"

unset CODACY_PROJECT_TOKEN
