#!/bin/bash

python `pwd`/setup.py sdist --format=gztar,bztar
python `pwd`/setup.py sdist upload

exit 0
