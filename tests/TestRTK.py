#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.TestRTK.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This is the test class for testing the RTK module algorithms and models.
"""

import sys
import os
from os.path import dirname, isfile
sys.path.insert(0, dirname(dirname(__file__)) + "/rtk")

import logging

from treelib import Tree

import unittest
from nose.plugins.attrib import attr

from Configuration import Configuration
from RTK import Model, RTK, _initialize_loggers
from dao.DAO import DAO
from gui.gtk.mwi.ListBook import ListView
from gui.gtk.mwi.ModuleBook import ModuleView
from gui.gtk.mwi.WorkBook import WorkView

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestRTKFunctions(unittest.TestCase):
    """
    Class for testing the RTK functions.
    """

    def setUp(self):
        """
        Setup the test fixture for the RTK functions.
        """

        self.Configuration = Configuration()

    @attr(all=True, unit=True)
    def test00a_initialize_logger(self):
        """
        (TestRTKFunctions) _initialize_loggers should return a tuple of logging.Logger instances
        """

        self.Configuration.RTK_LOG_DIR = '/tmp'

        (self.Configuration.RTK_DEBUG_LOG,
         self.Configuration.RTK_USER_LOG,
         self.Configuration.RTK_IMPORT_LOG) = \
            _initialize_loggers(self.Configuration)

        self.assertTrue(isinstance(self.Configuration.RTK_DEBUG_LOG,
                                   logging.Logger))
        self.assertTrue(isinstance(self.Configuration.RTK_USER_LOG,
                                   logging.Logger))
        self.assertTrue(isinstance(self.Configuration.RTK_IMPORT_LOG,
                                   logging.Logger))
        self.assertTrue(isfile('/tmp/RTK_debug.log'))
        self.assertTrue(isfile('/tmp/RTK_user.log'))
        self.assertTrue(isfile('/tmp/RTK_import.log'))


class TestRTKModel(unittest.TestCase):
    """
    Class for testing the RTK data model.
    """

    def setUp(self):
        """
        Setup test fixture for the RTK Model class.
        """

        self.Configuration = Configuration()

        self.Configuration.RTK_SITE_DIR = \
            dirname(dirname(__file__)) + '/config'
        self.Configuration.RTK_HOME_DIR = '/tmp/RTK'
        self.Configuration.set_site_variables()
        self.Configuration.set_user_variables()
        self.Configuration.create_user_configuration()

        self.Configuration.RTK_COM_BACKEND = 'sqlite'
        self.Configuration.RTK_COM_INFO = {'host'    : 'localhost',
                                           'socket'  : 3306,
                                           'database': '/tmp/TestCommonDB.rtk',
                                           'user'    : '',
                                           'password': ''}
        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {'host'    : 'localhost',
                                            'socket'  : 3306,
                                            'database': '/tmp/TestDB.rtk',
                                            'user'    : '',
                                            'password': ''}

        self.site_dao = DAO()
        _database = self.Configuration.RTK_COM_BACKEND + ':///' + \
                    self.Configuration.RTK_COM_INFO['database']
        self.site_dao.db_connect(_database)
        self.program_dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.program_dao.db_connect(_database)

        self.DUT = Model(self.site_dao, self.program_dao)

    @attr(all=True, unit=True)
    def test00_initialize_RTK(self):
        """
        (TestRTKModel) __init__() should create an instance of the RTK.Model object
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.site_dao, DAO))
        self.assertTrue(isinstance(self.DUT.program_dao, DAO))
        self.assertEqual(self.DUT.program_session, None)

    @attr(all=True, integration=True, unit=False)
    def test04a_create_new_program(self):
        """
        (TestRTKModel) create_program() should return a zero error code on success
        """

        configuration = Configuration()
        configuration.RTK_BACKEND = 'sqlite'
        configuration.RTK_PROG_INFO = {'host' : 'localhost',
                                       'socket' : 3306,
                                       'database' : '/tmp/BigAssTestDB.rtk',
                                       'type' : 'sqlite',
                                       'user' : '',
                                       'password' : ''}
        _database = configuration.RTK_BACKEND + ':///' + \
                    configuration.RTK_PROG_INFO['database']
        _error_code, _msg = self.DUT.create_program(_database)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Creating RTK Program database ' \
                               'sqlite:////tmp/BigAssTestDB.rtk.')

        if os.path.isfile('/tmp/BigAssTestDB.rtk'):
            os.remove('/tmp/BigAssTestDB.rtk')

    @attr(all=True, unit=True)
    def test04b_create_new_program_failed(self):
        """
        (TestRTKModel) create_program() should return a non-zero error code on failure
        """

        configuration = Configuration()
        configuration.RTK_BACKEND = 'sqlite'
        configuration.RTK_PROG_INFO = {'host' : 'localhost',
                                       'socket' : 3306,
                                       'database' : 'tmp/BigAssTestDB.rtk',
                                       'type' : 'sqlite',
                                       'user' : '',
                                       'password' : ''}
        _database = configuration.RTK_BACKEND + ':///' + \
                    configuration.RTK_PROG_INFO['database']
        _error_code, _msg = self.DUT.create_program(_database)

        self.assertEqual(_error_code, 1001)
        self.assertEqual(_msg, 'RTK ERROR: Failed to create RTK Program ' \
                               'database sqlite:///tmp/BigAssTestDB.rtk.')

    @attr(all=True, unit=True)
    def test06a_open_program(self):
        """
        (TestRTKModel) open_program() should return a zero error code on success
        """

        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        _error_code, _msg = self.DUT.open_program(_database)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Opening RTK Program database ' \
                               'sqlite:////tmp/TestDB.rtk.')

    @attr(all=True, unit=True)
    def test07a_load_globals(self):
        """
        (TestRTKModel) load_globals() should return False on success
        """

        self.assertFalse(self.DUT.load_globals(self.Configuration))

        self.assertTrue(isinstance(self.DUT.tree, Tree))

        self.assertEqual(self.Configuration.RTK_ACTION_CATEGORY, {})
        self.assertEqual(self.Configuration.RTK_INCIDENT_CATEGORY,
                         {34: (u'HW', u'Hardware', u'incident', 1),
                          35: (u'SW', u'Software', u'incident', 1),
                          36: (u'PROC', u'Process', u'incident', 1)})
        self.assertEqual(self.Configuration.RTK_SEVERITY,
                         {10: (u'INS', u'Insignificant', u'risk', 1),
                          11: (u'SLT', u'Slight', u'risk', 2),
                          12: (u'LOW', u'Low', u'risk', 3),
                          13: (u'MED', u'Medium', u'risk', 4),
                          14: (u'HI', u'High', u'risk', 5),
                          15: (u'MAJ', u'Major', u'risk', 6)})

        self.assertEqual(self.Configuration.RTK_ACTIVE_ENVIRONMENTS, {})
        self.assertEqual(self.Configuration.RTK_DORMANT_ENVIRONMENTS, {})
        self.assertEqual(self.Configuration.RTK_SW_DEV_ENVIRONMENTS, {})

        self.assertEqual(self.Configuration.RTK_AFFINITY_GROUPS, {})
        self.assertEqual(self.Configuration.RTK_WORKGROUPS[1],
                         (u'Engineering, Systems', u'workgroup'))

        self.assertEqual(self.Configuration.RTK_FAILURE_PROBABILITY, {})
        self.assertEqual(self.Configuration.RTK_SW_LEVELS, {})

        self.assertEqual(self.Configuration.RTK_DETECTION_METHODS, {})
        self.assertEqual(self.Configuration.RTK_SW_TEST_METHODS, {})

        self.assertEqual(self.Configuration.RTK_ALLOCATION_MODELS, {})
        self.assertEqual(self.Configuration.RTK_DAMAGE_MODELS, {})
        self.assertEqual(self.Configuration.RTK_HR_MODEL, {})

        self.assertEqual(self.Configuration.RTK_LIFECYCLE, {})
        self.assertEqual(self.Configuration.RTK_SW_DEV_PHASES, {})

        self.assertEqual(self.Configuration.RTK_RPN_DETECTION, {})
        self.assertEqual(self.Configuration.RTK_RPN_SEVERITY, {})
        self.assertEqual(self.Configuration.RTK_RPN_OCCURRENCE, {})

        self.assertEqual(self.Configuration.RTK_ACTION_STATUS, {})
        self.assertEqual(self.Configuration.RTK_INCIDENT_STATUS, {})

        self.assertEqual(self.Configuration.RTK_CONTROL_TYPES,
                         [u'Prevention', u'Detection'])
        self.assertEqual(self.Configuration.RTK_COST_TYPE, {})
        self.assertEqual(self.Configuration.RTK_HR_TYPE, {})
        self.assertEqual(self.Configuration.RTK_INCIDENT_TYPE, {})
        self.assertEqual(self.Configuration.RTK_MTTR_TYPE, {})
        self.assertEqual(self.Configuration.RTK_REQUIREMENT_TYPE,
                         {1: (u'Type Code', u'Test Type of Requirement',
                              u'requirement')})
        self.assertEqual(self.Configuration.RTK_VALIDATION_TYPE, {})

        self.assertEqual(self.Configuration.RTK_SW_APPLICATION,
                         {1: (u'Application Description', 1.0, 1.0)})
        self.assertEqual(self.Configuration.RTK_CATEGORIES, {})
        self.assertEqual(self.Configuration.RTK_CRITICALITY,
                         {1: (u'Criticality Name', u'Criticality Description',
                              u'', 0)})
        self.assertEqual(self.Configuration.RTK_FAILURE_MODES, {})
        self.assertEqual(self.Configuration.RTK_HAZARDS,
                         {1: (u'Hazard Category', u'Hazard Subcategory')})
        self.assertEqual(self.Configuration.RTK_MANUFACTURERS,
                         {1: (u'Distribution Description', u'unknown',
                              u'CAGE Code')})
        self.assertEqual(self.Configuration.RTK_MEASUREMENT_UNITS, {})
        self.assertEqual(self.Configuration.RTK_OPERATING_PARAMETERS, {})
        self.assertEqual(self.Configuration.RTK_S_DIST,
                         {1: (u'Distribution Description', u'unknown')})
        self.assertEqual(self.Configuration.RTK_STAKEHOLDERS,
                         {1: (u'Stakeholder',)})
        self.assertEqual(self.Configuration.RTK_SUBCATEGORIES, {})
        self.assertEqual(self.Configuration.RTK_USERS[1],
                         (u'Last Name', u'First Name', u'EMail', u'867.5309',
                          u'0'))

    @attr(all=True, unit=True)
    def test08a_validate_license(self):
        """
        (TestRTKModel) validate_license() should return a zero error code on success
        """

        _error_code,\
        _msg = self.DUT.validate_license('9490059723f3a743fb961d092d3283422f4f2d13')

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Validating RTK License.')

    @attr(all=True, unit=True)
    def test08b_validate_license_wrong_key(self):
        """
        (TestRTKModel) validate_license() should return a 1 error code when the license key is wrong
        """

        _error_code, _msg = self.DUT.validate_license('')

        self.assertEqual(_error_code, 1)
        self.assertEqual(_msg,
                         'RTK ERROR: Invalid license (Invalid key).  Your '
                         'license key is incorrect.  Closing the RTK '
                         'application.')


class TestRTKController(unittest.TestCase):
    """
    Class for testing the RTK data controller.
    """

    def setUp(self):
        """
        Setup test fixture for the RTK data controller class.
        """

        self.DUT = RTK(test=True)

        self.DUT.RTK_CONFIGURATION.RTK_COM_BACKEND = 'sqlite'
        self.DUT.RTK_CONFIGURATION.RTK_COM_INFO = {'host': 'localhost',
                                                   'socket': 3306,
                                                   'database': '/tmp/TestCommonDB.rtk',
                                                   'user': '',
                                                   'password': ''}
        self.DUT.RTK_CONFIGURATION.RTK_BACKEND = 'sqlite'
        self.DUT.RTK_CONFIGURATION.RTK_PROG_INFO = {'host': 'localhost',
                                                    'socket': 3306,
                                                    'database': '/tmp/TestDB.rtk',
                                                    'user': '',
                                                    'password': ''}
        self.DUT.RTK_CONFIGURATION.RTK_DATA_DIR = \
            '/home/arowland/.config/RTK/data'
        self.DUT.RTK_CONFIGURATION.RTK_ICON_DIR = \
            dirname(dirname(__file__)) + "/config/icons"

    @attr(all=True, unit=True)
    def test00_initialize_RTK(self):
        """
        (TestRTKController) __init__() should create an instance of the rtk.RTK object
        """

        self.assertTrue(isinstance(self.DUT, RTK))
        self.assertTrue(isinstance(self.DUT.rtk_model, Model))
        self.assertTrue(isinstance(self.DUT.dic_books['listview'], ListView))
        self.assertTrue(isinstance(self.DUT.dic_books['moduleview'],
                                   ModuleView))
        self.assertTrue(isinstance(self.DUT.dic_books['workview'], WorkView))
        self.assertEqual(self.DUT.dic_controllers['revision'], None)
        self.assertEqual(self.DUT.dic_controllers['function'], None)
        self.assertEqual(self.DUT.dic_controllers['requirement'], None)
        self.assertEqual(self.DUT.dic_controllers['hardware'], None)
        self.assertEqual(self.DUT.dic_controllers['software'], None)
        self.assertEqual(self.DUT.dic_controllers['testing'], None)
        self.assertEqual(self.DUT.dic_controllers['validation'], None)
        self.assertEqual(self.DUT.dic_controllers['incident'], None)
        self.assertEqual(self.DUT.dic_controllers['survival'], None)
        self.assertEqual(self.DUT.dic_controllers['matrices'], None)
        self.assertEqual(self.DUT.dic_controllers['profile'], None)
        self.assertEqual(self.DUT.dic_controllers['definition'], None)
        self.assertEqual(self.DUT.dic_controllers['fmea'], None)
        self.assertEqual(self.DUT.dic_controllers['stakeholder'], None)
        self.assertEqual(self.DUT.dic_controllers['allocation'], None)
        self.assertEqual(self.DUT.dic_controllers['hazard'], None)
        self.assertEqual(self.DUT.dic_controllers['similaritem'], None)
        self.assertEqual(self.DUT.dic_controllers['pof'], None)
        self.assertEqual(self.DUT.dic_controllers['growth'], None)
        self.assertEqual(self.DUT.dic_controllers['action'], None)
        self.assertEqual(self.DUT.dic_controllers['component'], None)

    @attr(all=True, unit=True)
    def test01a_request_load_globals(self):
        """
        (TestRTKController) request_load_globals() should return False on success
        """

        self.DUT.rtk_model.tree = None
        self.DUT.rtk_model.tree = Tree()

        _database = self.DUT.RTK_CONFIGURATION.RTK_COM_BACKEND + ':///' + \
                    self.DUT.RTK_CONFIGURATION.RTK_COM_INFO['database']
        self.DUT.rtk_model.program_dao.db_connect(_database)

        self.assertFalse(self.DUT.request_load_globals())

    @attr(all=True, unit=True)
    def test02a_request_open_program(self):
        """
        (TestRTKController) request_open_program() should return False on success
        """

        self.assertFalse(self.DUT.request_open_program())
        self.assertEqual(self.DUT.RTK_CONFIGURATION.RTK_PREFIX,
                         {'function': [u'FUNCTION', 0],
                          'assembly': [u'ASSEMBLY', 0], 'fmeca': [u'FMECA', 0],
                          'effect'  : [u'EFFECT', 0], 'part': [u'PART', 0],
                          'mode'    : [u'MODE', 0], 'software': [u'MODULE', 0],
                          'cause'   : [u'CAUSE', 0], 'revision': [u'REV', 0]})
        self.assertEqual(self.DUT.RTK_CONFIGURATION.RTK_MODULES,
                         {'function'  : 1, 'fta': 0, 'requirement': 1,
                          'validation': 1, 'survival': 1, 'testing': 1,
                          'rbd'       : 0, 'hardware': 1, 'rcm': 0,
                          'incident'  : 1, 'revision': 1, 'software': 1})

    @attr(all=True, integration=True, unit=False)
    def test03a_request_create_program(self):
        """
        (TestRTKController) request_create_program() should return False on success
        """

        self.assertFalse(self.DUT.request_create_program())

    @attr(all=False, unit=False)
    def test04a_request_close_program(self):
        """
        (TestRTKController) request_close_program() should return False on success
        """

        self.assertFalse(self.DUT.request_close_program())

    @attr(all=True, unit=True)
    def test05a_request_save_program(self):
        """
        (TestRTKController) request_save_program() should return False on success
        """

        self.DUT.request_open_program()

        self.assertFalse(self.DUT.request_save_program())

    @attr(all=True, unit=True)
    def test06a_request_validate_license(self):
        """
        (TestRTKController) request_validate_license() should return False on success
        """

        self.assertFalse(self.DUT.request_validate_license())
