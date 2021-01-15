#!/bin/sh
# This little script will print the packages and versions installed on your
# system/virtualenv in a format that can simply be copied and pasted into
# a RAMSTK issue report.  Use from the top level RAMSTK directory as follows:
#
#    sh devtools/getenv.sh
#
print_file_version() {
    file=$1

    if [ "x$file" != "x" ];
    then
        version=$(pip show $file | grep Version: | cut -d ':' -f2 | tr -d '[:space:]')
        if [ "x$version" = "x" ];
        then
            version="NOT INSTALLED!"
        fi
        echo "  * "$file==$version
    fi
}

if [ "x$VIRTUAL_ENV" != "x" ];
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
while read -r file;
do
    file=$(echo $file | cut -d '=' -f1 | cut -d '>' -f1 | cut -d '<' -f1)
    print_file_version $file
done < requirements.in
echo ""

# Development modules.
echo "Development requirements:"
while read -r file;
do
    file=$(echo $file | cut -d '=' -f1 | cut -d '>' -f1 | cut -d '<' -f1 | sed '/^#/ d' | sed '/^-r/ d')
    print_file_version $file
done < requirements-dev.in
echo ""

# Testing modules.
echo "Testing requirements:"
while read -r file;
do
    file=$(echo $file | cut -d '=' -f1 | cut -d '>' -f1 | cut -d '<' -f1)
    print_file_version $file
done < requirements-test.in

exit 0
