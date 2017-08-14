#!/usr/bin/sh

curPath=$PWD
projPath=$HOME'/drive_d/projects/RTK'
testPath=$curPath'/tests'
testList=$testPath'/unit/Unit.tests'
excludeList=$testPath'/Excluded.dirs'

noseOpts="-c $curPath/setup.cfg --exclude-dir-file=$excludedList"
unitNoseOpts="$noseOpts --attr=unit=True --cover-package="
integrationNoseOpts="$noseOpts --attr=integration=True --cover-package="

nosetest=$(which nosetests)
coverage=$(which coverage)
codacy=$(which python-codacy-coverage)

# Execute all the unit tests.
while read package file;
do
    printf "EXECUTING UNIT TEST FOR: $package\n"
    $nosetest $unitNoseOpts$package $testPath/$file
    if [ "$?" == "0" ];
    then
        printf "UNIT TEST FOR $package: SAT\n\n"
    else
        printf "UNIT TEST FOR $package: UNSAT\n\n"
    fi
done < $testList

# Execute all the integration tests.
while read package file;
do
    printf "EXECUTING INTEGRATION TEST FOR: $package\n"
    $nosetest $integrationNoseOpts$package $testPath/$file
    if [ "$?" == "0" ];
    then
        printf "INTEGRATION TEST FOR $package: SAT\n\n"
    else
        printf "INTEGRATION TEST FOR $package: UNSAT\n\n"
    fi
done < $testList

# Create the coverage XML file and upload to codacy.
$coverage xml -o "$curPath/tests/coverage.xml"
$codacy -r "$curPath/tests/coverage.xml"
