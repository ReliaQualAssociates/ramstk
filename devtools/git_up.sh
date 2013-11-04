#!/bin/sh

MESSAGE="$1"

GIT=`which git`
FILES=`find $HOME/MyProjects/RTK/ -name '*.py' -o -name '*.xml' -o -name '*.sql' -o -name '*.sh'`

for f in $FILES;
do
    $GIT add $f
done

$GIT commit -m "$MESSAGE"
$GIT push

exit 0
