#!/bin/sh

_file=$1

_yapf=`which yapf`
_pylint=`which pylint`
_pycodestyle=`which pycodestyle`
_pydocstyle=`which pydocstyle`

NC='\033[0m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
PURPLE='\033[0;35m'
RED='\033[0;31m'

echo -e "${RED}Executing yapf on $_file:\n"
$_yapf -i $_file

echo -e "${BLUE}Executing pylint on $_file:\n"
$_pylint $_file

echo -e "${PURPLE}Executing pycodestyle on $_file:\n"
$_pycodestyle -v --max-line-length=80 --statistics $_file

echo -e "${GREEN}Executing pydocstyle on $_file:${NC}\n"
$_pydocstyle --convention=pep257 $_file

exit 0
