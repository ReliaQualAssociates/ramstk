#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests._fmea.TestFMEAPackage.sh is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
This is the test class for testing the Function package.
"""

import sys
import os
import itertools

import nose
from nose.loader import TestLoader
from nose.plugins.attrib import AttributeSelector
from nose.plugins.cover import Coverage
from nose.plugins.manager import PluginManager

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__))) + '/../',
)

# pylint: disable=wrong-import-postion
from test_setup import _create_program_database
from _dao.TestRTKFunction import TestRTKFunction
from _dao.TestRTKAction import TestRTKAction
from _dao.TestRTKControl import TestRTKControl
from _dao.TestRTKMode import TestRTKMode
from _fmea.TestMode import TestModeDataModel
from _fmea.TestControl import TestControlDataModel
from _fmea.TestAction import TestActionDataModel
from _fmea.TestFMEA import TestFMEADataModel, TestFMEADataController
from _function import TestFunctionDataModel, TestFunctionDataController


def test_function_package(suites):
    """
    Comprehensive test suite for the Function package.

    This test suite pulls in all the tests necessary to fully test the
    components needed to provide the Function module functionality; that is, it
    runs the following tests, in this order:

        Function database table
        Function data model
        Function data controller
        FMEA Mode database table
        FMEA Control database table
        FMEA Action database table
        FMEA Mode data model
        FMEA Control data model
        FMEA Action data model
        FMEA FMEA data model
        FMEA FMEA data controller
    """
    all_tests = ()

    plugin_mgr = PluginManager(plugins=[AttributeSelector(), Coverage()])

    for _suite in suites:
        all_tests = itertools.chain(all_tests,
                                    TestLoader().loadTestsFromTestCase(_suite))

    suite = nose.suite.ContextSuite(all_tests)

    args = [
        '', '-v', '-a unit=True', '--with-coverage', '--cover-branches',
        '--cover-xml', '--cover-package=dao.RTKFunction',
        '--cover-package=dao.RTKMode', '--cover-package=dao.RTKControl',
        '--cover-package=dao.RTKAction', '--cover-package=function',
        '--cover-package=analyses.fmea'
    ]
    nose.runmodule(argv=args, suite=suite, plugins=plugin_mgr)

    return None


if __name__ == '__main__':

    _db_suites = [TestRTKFunction, TestRTKMode, TestRTKControl, TestRTKAction]
    _model_suites = [
        TestModeDataModel, TestControlDataModel, TestActionDataModel,
        TestFMEADataModel, TestFunctionDataModel
    ]
    _controller_suites = [TestFunctionDataController, TestFMEADataController]

    # For the nosetest example.
    if str(sys.argv[1]) == 'db':
        _suites = _db_suites
    elif str(sys.argv[1]) == 'model':
        _suites = _model_suites
    elif str(sys.argv[1]) == 'controller':
        _suites = _controller_suites
    else:
        _suites = _db_suites + _model_suites + _controller_suites

    _create_program_database()
    test_function_package(_suites)

    print "\n" + '\033[34m' + '\033[1m' + \
          "  Removing the RTK Program test database...." + '\033[0m' + "\n"

    if os.path.isfile('/tmp/TestDB.rtk'):
        os.remove('/tmp/TestDB.rtk')
