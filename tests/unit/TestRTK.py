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

import unittest
from nose.plugins.attrib import attr

import logging

import Configuration
from RTK import _read_site_configuration, _read_program_configuration, \
                _initialize_loggers, RTK

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestUtilities(unittest.TestCase):
    """
    Class for testing the RTK Utilities.
    """

    def setUp(self):
        """
        Setup the test fixture for the RTK class.
        """

        Configuration.LOG_DIR = '/tmp'
        self.DUT = RTK()

    @attr(all=True, unit=True)
    def test00_read_site_configuration(self):
        """
        (TestRTK) _read_site_configuration should return False on success
        """

        self.assertFalse(_read_site_configuration())
        if os.name == 'posix':
            self.assertEqual(Configuration.OS, 'Linux')
            self.assertEqual(Configuration.SITE_DIR,
                             '/home/andrew/.config/RTK')
        elif os.name == 'nt':
            self.assertEqual(Configuration.OS, 'Windows')
            self.assertEqual(Configuration.SITE_DIR, '/usr/share/RTK')

        self.assertEqual(Configuration.COM_BACKEND, 'sqlite3')
        self.assertEqual(Configuration.RTK_COM_INFO[0], 'frodo')
        self.assertEqual(Configuration.RTK_COM_INFO[1], '3306')
        self.assertEqual(Configuration.RTK_COM_INFO[2], 'relkitcom')
        self.assertEqual(Configuration.RTK_COM_INFO[3], 'relkitcom')
        self.assertEqual(Configuration.RTK_COM_INFO[4], 'relkitcom')

    @attr(all=True, unit=True)
    def test01_read_program_configuration(self):
        """
        (TestRTK) _read_program_configuration should return False on success
        """

        self.assertFalse(_read_program_configuration())
        if os.name == 'posix':
            self.assertEqual(Configuration.SITE_DIR,
                             '/home/andrew/.config/RTK')
        elif os.name == 'nt':
            self.assertEqual(Configuration.SITE_DIR, '/usr/share/RTK')

        self.assertEqual(Configuration.BACKEND, 'sqlite3')
        self.assertEqual(Configuration.RTK_PROG_INFO[0], 'localhost')
        self.assertEqual(Configuration.RTK_PROG_INFO[1], '3306')
        self.assertEqual(Configuration.RTK_PROG_INFO[2], '')
        self.assertEqual(Configuration.RTK_PROG_INFO[3], '')
        self.assertEqual(Configuration.RTK_PROG_INFO[4], '')

        self.assertEqual(Configuration.FRMULT, 1000000.0)
        self.assertEqual(Configuration.PLACES, '6')
        self.assertEqual(Configuration.RTK_MODE_SOURCE, '2')
        self.assertEqual(Configuration.TABPOS[0], 'top')
        self.assertEqual(Configuration.TABPOS[1], 'top')
        self.assertEqual(Configuration.TABPOS[2], 'left')

        self.assertEqual(Configuration.CONF_DIR, '/home/andrew/.config/RTK/')
        self.assertEqual(Configuration.DATA_DIR,
                         '/home/andrew/.config/RTK/data/')
        self.assertEqual(Configuration.ICON_DIR,
                         '/home/andrew/.config/RTK/icons/')
        self.assertEqual(Configuration.LOG_DIR,
                         '/home/andrew/.config/RTK/logs/')
        self.assertEqual(Configuration.PROG_DIR,
                         '/home/andrew/analyses.git/RTK')

        self.assertEqual(Configuration.RTK_FORMAT_FILE[0],
                         '/home/andrew/.config/RTK/revision_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[1],
                         '/home/andrew/.config/RTK/function_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[2],
                         '/home/andrew/.config/RTK/requirement_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[3],
                         '/home/andrew/.config/RTK/hardware_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[4],
                         '/home/andrew/.config/RTK/validation_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[5],
                         '/home/andrew/.config/RTK/rg_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[6],
                         '/home/andrew/.config/RTK/fraca_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[7],
                         '/home/andrew/.config/RTK/part_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[8],
                         '/home/andrew/.config/RTK/sia_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[9],
                         '/home/andrew/.config/RTK/fmeca_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[10],
                         '/home/andrew/.config/RTK/stakeholder_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[11],
                         '/home/andrew/.config/RTK/testing_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[12],
                         '/home/andrew/.config/RTK/mechanism_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[13],
                         '/home/andrew/.config/RTK/rgincident_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[14],
                         '/home/andrew/.config/RTK/incident_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[15],
                         '/home/andrew/.config/RTK/software_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[16],
                         '/home/andrew/.config/RTK/dataset_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[17],
                         '/home/andrew/.config/RTK/risk_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[18],
                         '/home/andrew/.config/RTK/ffmeca_format.xml')
        self.assertEqual(Configuration.RTK_FORMAT_FILE[19],
                         '/home/andrew/.config/RTK/sfmeca_format.xml')

        self.assertEqual(Configuration.RTK_COLORS[0], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS[1], '#000')
        self.assertEqual(Configuration.RTK_COLORS[2], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS[3], '#000')
        self.assertEqual(Configuration.RTK_COLORS[4], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS[5], '#000000')
        self.assertEqual(Configuration.RTK_COLORS[6], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS[7], '#000000')
        self.assertEqual(Configuration.RTK_COLORS[8], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS[9], '#000000')
        self.assertEqual(Configuration.RTK_COLORS[10], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS[11], '#000000')
        self.assertEqual(Configuration.RTK_COLORS[12], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS[13], '#000000')
        self.assertEqual(Configuration.RTK_COLORS[14], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS[15], '#000000')
        self.assertEqual(Configuration.RTK_COLORS[16], '#FF0000')
        self.assertEqual(Configuration.RTK_COLORS[17], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS[18], '#00FF00')
        self.assertEqual(Configuration.RTK_COLORS[19], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS[20], '#A52A2A')
        self.assertEqual(Configuration.RTK_COLORS[21], '#FFFFFF')
        self.assertEqual(Configuration.RTK_COLORS[22], '#000000')

    @attr(all=True, unit=True)
    def test02_initialize_logger(self):
        """
        (TestRTK) _initialize_loggers should return a tuple of logging.Logger instances
        """

        Configuration.LOG_DIR = '/tmp'

        (_debug_log,
         _user_log,
         _import_log) = _initialize_loggers()

        self.assertTrue(isinstance(_debug_log, logging.Logger))
        self.assertTrue(isinstance(_user_log, logging.Logger))
        self.assertTrue(isinstance(_import_log, logging.Logger))
        self.assertTrue(isfile('/tmp/RTK_error.log'))
        self.assertTrue(isfile('/tmp/RTK_user.log'))
        self.assertTrue(isfile('/tmp/RTK_import.log'))

    @attr(all=True, unit=True)
    def test03_initialize_RTK(self):
        """
        (TestRTK) __init__ should create an instance of the rtk.RTK object
        """

        self.assertTrue(isinstance(self.DUT, RTK))

    @attr(all=True, unit=False)
    def test04_create_new_project(self):
        """
        (TestRTK) create_project should return False on success
        """

        Configuration.RTK_PROG_INFO = ['localhost', 3306, 'BigAssTestDB.rtk',
                                       '', '']
        self.assertFalse(self.DUT.create_project())

    @attr(all=True, unit=False)
    def test05_open_project(self):
        """
        (TestRTK) open_project should return False on success
        """

        Configuration.RTK_PROG_INFO = ['localhost', 3306, 'BigAssTestDB.rtk',
                                       '', '']
        self.assertFalse(self.DUT.open_project())
