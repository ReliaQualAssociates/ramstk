#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import nose

mycwd = os.getcwd()

if __name__ == '__main__':

    # Run all the unit tests.
    unit_tests = open('tests/unit.tests', 'r')
    argv = sys.argv[:]

    argv.insert(1, '')
    argv[0] = '--attr unit=True --with-coverage --cover-branches'

    for test in unit_tests:
        _test_file = ''.join([mycwd, '/tests/unit/', test]).rstrip('\r\n')
        argv[1] = _test_file
        nose.run(argv=argv)

    # Run all the integration tests.
    # FUTURE
