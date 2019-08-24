#!/bin/sh
# This little script will print the packages and versions installed on your
# system/virtualenv in a format that can simply be copied and pasted into
# a RAMSTK issue report.  Use from the top level RAMSTK directory as follows:
#
#    sh docs/GetEnv.sh
#

if [[ "x$VIRTUAL_ENV" != "x" ]];
then
    echo "Using a virtualenv at: "$VIRTUAL_ENV
else
    echo "Not using a virtualenv."
fi
echo""

# RAMSTK version.
version=$(pip show RAMSTK | grep Version: | cut -d ':' -f2 | tr -d '[:space:]')
echo "RAMSTK-"$version
echo ""

# Python version.
$(which python) -V
echo ""

# Runtime modules.
echo "Runtime requirements:"
for file in $(cat requirements.in | cut -d '=' -f1 | cut -d '>' -f1 | cut -d '<' -f1);
do
    version=$(pip show $file | grep Version: | cut -d ':' -f2 | tr -d '[:space:]')
    if [[ "x$version" == "x" ]];
    then
        version="NOT INSTALLED!"
    fi
    echo "  * "$file==$version
done
echo ""

# Development modules.
echo "Development requirements:"
for file in $(cat requirements-dev.in | cut -d '=' -f1 | cut -d '>' -f1 | cut -d '<' -f1 | sed '/^#/ d' | sed '/^-r/ d');
do
    version=$(pip show $file | grep Version: | cut -d ':' -f2 | tr -d '[:space:]')
    if [[ "x$version" == "x" ]];
    then
        version="NOT INSTALLED!"
    fi
    echo "  * "$file==$version
done
echo ""

# Testing modules.
echo "Testing requirements:"
for file in $(cat requirements-test.in | cut -d '=' -f1 | cut -d '>' -f1 | cut -d '<' -f1);
do
    version=$(pip show $file | grep Version: | cut -d ':' -f2 | tr -d '[:space:]')
    if [[ "x$version" == "x" ]];
    then
        version="NOT INSTALLED!"
    fi
    echo "  * "$file==$version
done
