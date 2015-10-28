#!/bin/sh

cd /home/andrew/projects/RTK/tests

for dir in allocation dao datamodels failure_definition fmea function hardware hazard incident pof requirement revision similar_item software stakeholder statistics survival testing usage validation; do
	nosetests --quiet --with-coverage --cover-branches --with-html --html-file="_test_results/${dir}_unit_tests.html" --attr=unit=True ./$dir
	nosetests --quiet --with-coverage --cover-branches --with-html --html-file="_test_results/${dir}_integration_tests.html" --attr=integration=True ./$dir
done

exit 0
