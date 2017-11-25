#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests._fmea.TestFMEAPackage.sh is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Revision package."""

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

# pylint: disable=wrong-import-postion
from test_setup import _create_program_database
from _dao import TestRTKEnvironment, TestRTKFailureDefinition, \
    TestRTKMission, TestRTKMissionPhase, TestRTKRevision
from _failure_definition import TestFailureDefinitionDataModel, \
    TestFailureDefinitionDataController
from _revision import TestRevisionDataModel, TestRevisionDataController
from _usage import TestMissionDataModel, TestMissionPhaseDataModel, \
    TestEnvironmentDataModel, TestUsageProfileDataModel, \
    TestUsageProfileDataController


def test_function_package(suites):
    """
    Comprehensive test suite for the Function package.

    This test suite pulls in all the tests necessary to fully test the
    components needed to provide the Function module functionality; that is, it
    runs the following tests, in this order:

        Revision database table
        Failure Definition database table
        Mission database table
        Mission Phase database table
        Environment database table
        Revision data model
        Failure Definition data model
        Mission data model
        Mission Phase data model
        Environment data model
        Usage Profile data model
        Revision data controller
        Failure Definition data controller
        Usage Profile data controller
    """
    all_tests = ()

    plugin_mgr = PluginManager(plugins=[AttributeSelector(), Coverage()])

    for _suite in suites:
        all_tests = itertools.chain(all_tests,
                                    TestLoader().loadTestsFromTestCase(_suite))

    suite = nose.suite.ContextSuite(all_tests)

    args = [
        '', '-v', '-a unit=True', '--with-coverage', '--cover-branches',
        '--cover-xml', '--cover-package=dao.RTKRevision',
        '--cover-package=dao.RTKFailureDefinition',
        '--cover-package=dao.RTKMission',
        '--cover-package=dao.RTKMissionPhase',
        '--cover-package=dao.RTKEnvironment', '--cover-package=revision',
        '--cover-package=failure_definition', '--cover-package=usage'
    ]
    nose.runmodule(argv=args, suite=suite, plugins=plugin_mgr)

    return None


if __name__ == '__main__':

    _db_suites = [
        TestRTKRevision, TestRTKFailureDefinition, TestRTKMission,
        TestRTKMissionPhase, TestRTKEnvironment
    ]

    _model_suites = [
        TestRevisionDataModel, TestFailureDefinitionDataModel,
        TestMissionDataModel, TestMissionPhaseDataModel,
        TestEnvironmentDataModel
    ]

    _controller_suites = [
        TestRevisionDataController, TestFailureDefinitionDataController,
        TestUsageProfileDataController
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
