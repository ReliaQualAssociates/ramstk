#!/usr/bin/env python -O
"""
This is the test class for testing the RTK module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       rtk.tests.unit.TestRTK.py is part of The RTK Project
#
# All rights reserved.

import sys
import os
from os.path import dirname, isfile
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import logging


import unittest
from nose.plugins.attrib import attr

import Configuration as Configuration
import Utilities as Utilities
from RTK import _read_site_configuration, _read_program_configuration, \
                _initialize_loggers, Model
from dao.DAO import DAO

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestFunctions(unittest.TestCase):
    """
    Class for testing the RTK functions.
    """

    def setUp(self):
        """
        Setup the test fixture for the RTK functions.
        """

        Configuration.DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/rtk_debug.log')
        Configuration.USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                        '/tmp/rtk_user.log')

    @attr(all=True, unit=True)
    def test00a_read_site_configuration(self):
        """
        (TestRTKFunctions) _read_site_configuration should return a zero error code on success
        """

        _error_code, _msg = _read_site_configuration()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Parsing site configuration file.')

        if os.name == 'posix':
            self.assertEqual(Configuration.RTK_OS, 'Linux')
            self.assertEqual(Configuration.RTK_SITE_DIR,
                             os.environ['HOME'] + '/.config/RTK')
        elif os.name == 'nt':
            self.assertEqual(Configuration.RTK_OS, 'Windows')
            self.assertEqual(Configuration.RTK_SITE_DIR, '/usr/share/RTK')

        self.assertEqual(Configuration.RTK_COM_BACKEND, 'sqlite3')
        self.assertEqual(Configuration.RTK_COM_INFO['host'], '')
        self.assertEqual(Configuration.RTK_COM_INFO['socket'], '3306')
        self.assertEqual(Configuration.RTK_COM_INFO['database'], 'rtkcom')
        self.assertEqual(Configuration.RTK_COM_INFO['user'], 'rtkcom')
        self.assertEqual(Configuration.RTK_COM_INFO['password'], 'rtkcom')

    @attr(all=True, unit=True)
    def test01a_read_program_configuration(self):
        """
        (TestRTKFunctions) _read_program_configuration should return zero error code on success
        """

        _error_code, _msg = _read_program_configuration()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Parsing program configuration file.')

        if os.name == 'posix':
            self.assertEqual(Configuration.RTK_SITE_DIR,
                             os.environ['HOME'] + '/.config/RTK')
        elif os.name == 'nt':
            self.assertEqual(Configuration.RTK_SITE_DIR, '/usr/share/RTK')

        self.assertEqual(Configuration.RTK_BACKEND, 'sqlite3')
        self.assertEqual(Configuration.RTK_PROG_INFO['host'], '')
        self.assertEqual(Configuration.RTK_PROG_INFO['socket'], '3306')
        self.assertEqual(Configuration.RTK_PROG_INFO['database'], '')
        self.assertEqual(Configuration.RTK_PROG_INFO['user'], '')
        self.assertEqual(Configuration.RTK_PROG_INFO['password'], '')

        self.assertEqual(Configuration.RTK_HR_MULTIPLIER, 1000000.0)
        self.assertEqual(Configuration.RTK_DEC_PLACES, '6')
        self.assertEqual(Configuration.RTK_MODE_SOURCE, '1')
        self.assertEqual(Configuration.RTK_TABPOS['listbook'], 'bottom')
        self.assertEqual(Configuration.RTK_TABPOS['modulebook'], 'top')
        self.assertEqual(Configuration.RTK_TABPOS['workbook'], 'bottom')

        self.assertEqual(Configuration.CONF_DIR,
                         os.environ['HOME'] + '/.config/RTK/')
        self.assertEqual(Configuration.DATA_DIR,
                         os.environ['HOME'] + '/.config/RTK/data/')
        self.assertEqual(Configuration.ICON_DIR,
                         os.environ['HOME'] + '/.config/RTK/icons/')
        self.assertEqual(Configuration.LOG_DIR,
                         os.environ['HOME'] + '/.config/RTK/logs/')
        self.assertEqual(Configuration.PROG_DIR,
                         os.environ['HOME'] + '/drive_d/analyses.git/RTK')

        self.assertEqual(Configuration.RTK_FORMAT_FILE['revision'],
                         Configuration.CONF_DIR + 'revision_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE['function'],
                         Configuration.CONF_DIR + 'function_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE['requirement'],
                         Configuration.CONF_DIR + 'requirement_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE['hardware'],
                         Configuration.CONF_DIR + 'hardware_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE['software'],
                         Configuration.CONF_DIR + 'software_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE['incident'],
                         Configuration.CONF_DIR + 'incident_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE['validation'],
                         Configuration.CONF_DIR + 'validation_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE['test'],
                         Configuration.CONF_DIR + 'testing_format.xml')

        self.assertEqual(Configuration.RTK_FORMAT_FILE['stakeholder'],
                         Configuration.CONF_DIR + 'stakeholder_format.xml')

        self.assertEqual(Configuration.RTK_FORMAT_FILE['part'],
                         Configuration.CONF_DIR + 'part_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE['sia'],
                         Configuration.CONF_DIR + 'sia_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE['fmeca'],
                         Configuration.CONF_DIR + 'fmeca_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE['ffmeca'],
                         Configuration.CONF_DIR + 'ffmeca_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE['sfmeca'],
                         Configuration.CONF_DIR + 'sfmeca_format.xml')

        self.assertEqual(Configuration.RTK_FORMAT_FILE['rgincident'],
                         Configuration.CONF_DIR + 'rgincident_format.xml')

        self.assertEqual(Configuration.RTK_FORMAT_FILE['dataset'],
                         Configuration.CONF_DIR + 'dataset_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE['risk'],
                         Configuration.CONF_DIR + 'risk_format.xml')

        self.assertEqual(Configuration.RTK_COLORS['revisionbg'], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS['functionbg'], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS['requirementbg'], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS['hardwarebg'], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS['softwarebg'], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS['incidentbg'], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS['validationbg'], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS['testbg'], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS['survivalbg'], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS['partbg'], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS['overstressbg'], '#FF0000')
        self.assertEqual(Configuration.RTK_COLORS['taggedbg'], '#00FF00')
        self.assertEqual(Configuration.RTK_COLORS['revisionfg'], '#000000')
        self.assertEqual(Configuration.RTK_COLORS['functionfg'], '#0000FF')
        self.assertEqual(Configuration.RTK_COLORS['requirementfg'], '#000000')
        self.assertEqual(Configuration.RTK_COLORS['hardwarefg'], '#000000')
        self.assertEqual(Configuration.RTK_COLORS['softwarefg'], '#000000')
        self.assertEqual(Configuration.RTK_COLORS['incidentfg'], '#000000')
        self.assertEqual(Configuration.RTK_COLORS['validationfg'], '#00FF00')
        self.assertEqual(Configuration.RTK_COLORS['testfg'], '#000000')
        self.assertEqual(Configuration.RTK_COLORS['survivalfg'], '#000000')
        self.assertEqual(Configuration.RTK_COLORS['partfg'], '#000000')
        self.assertEqual(Configuration.RTK_COLORS['overstressfg'], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS['taggedfg'], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS['nofrmodelfg'], '#A52A2A')

    @attr(all=True, unit=True)
    def test02a_initialize_logger(self):
        """
        (TestRTKFunctions) _initialize_loggers should return a tuple of logging.Logger instances
        """

        Configuration.RTK_LOG_DIR = '/tmp'

        (_debug_log,
         _user_log,
         _import_log) = _initialize_loggers()

        self.assertTrue(isinstance(_debug_log, logging.Logger))
        self.assertTrue(isinstance(_user_log, logging.Logger))
        self.assertTrue(isinstance(_import_log, logging.Logger))
        self.assertTrue(isfile('/tmp/RTK_error.log'))
        self.assertTrue(isfile('/tmp/RTK_user.log'))
        self.assertTrue(isfile('/tmp/RTK_import.log'))


class TestRTKModel(unittest.TestCase):
    """
    Class for testing the RTK data model.
    """

    def setUp(self):
        """
        Setup test fixture for the RTK class.
        """

        self.site_dao = DAO('')
        self.site_dao.db_connect('sqlite:////tmp/TestCommonDB.rtk')
        self.program_dao = DAO('')
        self.program_dao.db_connect('sqlite:////tmp/TestDB.rtk')

        self.DUT = Model(self.site_dao, self.program_dao)

    @attr(all=True, unit=False)
    def test00_initialize_RTK(self):
        """
        (TestRTKModel) __init__ should create an instance of the rtk.RTK object
        """

        self.assertTrue(isinstance(self.DUT, RTK))

    @attr(all=True, unit=False)
    def test04_create_new_project(self):
        """
        (TestRTKModel) create_project should return False on success
        """

        Configuration.RTK_PROG_INFO = ['localhost', 3306, 'BigAssTestDB.rtk',
                                       '', '']
        self.assertFalse(self.DUT.create_project())

    @attr(all=True, unit=False)
    def test05_open_project(self):
        """
        (TestRTKModel) open_project should return False on success
        """

        Configuration.RTK_PROG_INFO = ['localhost', 3306, 'BigAssTestDB.rtk',
                                       '', '']
        self.assertFalse(self.DUT.open_project())

