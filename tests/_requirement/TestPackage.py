#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests._fmea.TestFMEAPackage.sh is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Requirement package."""

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
    os.path.abspath(os.path.join(os.path.dirname(__file__))) + '/../', )

from test_setup import _create_program_database  # pylint: disable=E0401
from _dao import TestRTKRequirement, TestRTKStakeholder  # pylint: disable=E0401
# pylint: disable=E0401
from _requirement import TestRequirementDataModel, \
    TestRequirementDataController
# pylint: disable=E0401
from _stakeholder import TestStakeholderDataModel, \
    TestStakeholderDataController


def test_function_package(suites):
    """
    Comprehensive test suite for the Function package.

    This test suite pulls in all the tests necessary to fully test the
    components needed to provide the Function module functionality; that is, it
    runs the following tests, in this order:

        Requirement database table
        Stakeholder database table
        Requirement data model
        Stakeholder data model
        Requirement data controller
        Stakeholder data controller
    """
    all_tests = ()

    plugin_mgr = PluginManager(plugins=[AttributeSelector(), Coverage()])

    for _suite in suites:
        all_tests = itertools.chain(all_tests,
                                    TestLoader().loadTestsFromTestCase(_suite))

    suite = nose.suite.ContextSuite(all_tests)

    args = [
        '', '-v', '-a unit=True', '--with-coverage', '--cover-branches',
        '--cover-xml', '--cover-package=dao.RTKRequirement',
        '--cover-package=dao.RTKStakeholder', '--cover-package=requirement',
        '--cover-package=stakeholder'
    ]
    nose.runmodule(argv=args, suite=suite, plugins=plugin_mgr)

    return None


if __name__ == '__main__':

    # pylint: disable=invalid-name
    _db_suites = [TestRTKRequirement, TestRTKStakeholder]

    _model_suites = [TestRequirementDataModel, TestStakeholderDataModel]

    _controller_suites = [
        TestRequirementDataController, TestStakeholderDataController
    ]

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

    # if os.path.isfile('/tmp/TestCommonDB.rtk'):
    #     os.remove('/tmp/TestCommonDB.rtk')
