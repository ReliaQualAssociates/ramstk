#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests._hardware.TestPackage.sh is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Hardware package."""

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
from _dao import TestRTKHardware, TestRTKDesignElectric, \
    TestRTKDesignMechanic, TestRTKReliability, TestRTKMilHdbkF, TestRTKNSWC
from _hardware import TestHardwareDataModel, TestDesignElectricDataModel, \
    TestDesignMechanicDataModel, TestMilHdbkFDataModel, TestNSWCDataModel, \
    TestReliabilityDataModel, TestHardwareBoMDataModel, \
    TestHardwareBoMDataController
from _analyses.prediction import TestCapacitorModule, TestConnectionModule, \
    TestICModule, TestSemiconductorModule, TestResistorModule, \
    TestInductorModule, TestSwitchModule


def test_hardware_package(suites):
    """
    Comprehensive test suite for the Hardware package.

    This test suite pulls in all the tests necessary to fully test the
    components needed to provide the Hardware module hardwareality; that is, it
    runs the following tests, in this order:

        Hardware database table
        Electrical design parameters database table
        Mechanical design parameters database table
        MIL-HDBK-217F parameters database table
        NSWC parameters database table
        Reliability database table
        Hardware data model
        Electrical design data model
        Mechanical design data model
        MIL-HDBK-217F data model
        NSWC data model
        Reliability data model
        BoM data model
        BoM data controller
    """
    all_tests = ()

    plugin_mgr = PluginManager(plugins=[AttributeSelector(), Coverage()])

    for _suite in suites:
        all_tests = itertools.chain(all_tests,
                                    TestLoader().loadTestsFromTestCase(_suite))

    suite = nose.suite.ContextSuite(all_tests)

    args = [
        '', '-v', '-a unit=True', '--with-coverage', '--cover-branches',
        '--cover-xml', '--cover-package=dao.RTKHardware',
        '--cover-package=dao.RTKDesignElectric',
        '--cover-package=dao.RTKDesignMechanic',
        '--cover-package=dao.RTKReliability',
        '--cover-package=dao.RTKMilHdbkF', '--cover-package=dao.RTKNSWC',
        '--cover-package=hardware', '--cover-package=analyses.prediction'
    ]
    nose.runmodule(argv=args, suite=suite, plugins=plugin_mgr)

    return None


if __name__ == '__main__':

    _db_suites = [
        TestRTKHardware, TestRTKDesignElectric, TestRTKDesignMechanic,
        TestRTKReliability, TestRTKMilHdbkF, TestRTKNSWC
    ]

    _model_suites = [
        TestHardwareDataModel, TestDesignElectricDataModel,
        TestDesignMechanicDataModel, TestMilHdbkFDataModel, TestNSWCDataModel,
        TestReliabilityDataModel, TestHardwareBoMDataModel
    ]

    _controller_suites = [
        TestHardwareBoMDataController,
    ]

    _calculation_suites = [
        TestICModule, TestSemiconductorModule, TestResistorModule,
        TestCapacitorModule, TestInductorModule, TestSwitchModule,
        TestConnectionModule

    ]

    # For the nosetest example.
    if str(sys.argv[1]) == 'db':
        _suites = _db_suites
    elif str(sys.argv[1]) == 'model':
        _suites = _model_suites
    elif str(sys.argv[1]) == 'controller':
        _suites = _controller_suites
    elif str(sys.argv[1]) == 'calcs':
        _suites = _calculation_suites
    else:
        _suites = _db_suites + _model_suites + _controller_suites + \
            _calculation_suites

    # Don't need the test database to test the calculations.
    if str(sys.argv[1]) != 'calcs':
        _create_program_database()

    test_hardware_package(_suites)

    print "\n" + '\033[34m' + '\033[1m' + \
          "  Removing the RTK Program test database...." + '\033[0m' + "\n"

    if os.path.isfile('/tmp/TestDB.rtk'):
        os.remove('/tmp/TestDB.rtk')

    # if os.path.isfile('/tmp/TestCommonDB.rtk'):
    #     os.remove('/tmp/TestCommonDB.rtk')
