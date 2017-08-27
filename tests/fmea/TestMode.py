#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestMode.py is part of The RTK Project
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
This is the test class for testing the Mode class.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from analyses.fmea.Mode import Model, Mode, OutOfRangeError
from dao import DAO
from dao import RTKMode

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "weibullguy" Rowland'


class Test00ModeModelModel(unittest.TestCase):
    """
    Class for testing the Mode model class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Mode model class.
        """

        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {'host'    : 'localhost',
                                            'socket'  : 3306,
                                            'database': '/tmp/TestDB.rtk',
                                            'user'    : '',
                                            'password': ''}

        self.Configuration.DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG', '/tmp/RTK_debug.log')
        self.Configuration.USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO', '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(bind=self.dao.engine, autoflush=False,
                                       expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)
        self.dao.db_add([RTKMode(), ], self.session)
        self.dao.db_add([RTKMode(), ], self.session)

        self.DUT = Model(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestModeModel) __init__ should return instance of Mode data model
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertEqual(self.DUT.last_id, None)

    @attr(all=True, unit=True)
    def test01a_select_all_functional(self):
        """
        (TestModeModel): select_all() should return a Tree() object populated with RTKMode instances on success.
        """

        _tree = self.DUT.select_all(1, True)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKMode))

    @attr(all=True, unit=True)
    def test01b_select_all_hardware(self):
        """
        (TestModeModel): select_all() should return a Tree() object populated with RTKMode instances on success.
        """

        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKMode))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """
        (TestModeModel): select() should return an instance of the RTKMode data model on success.
        """

        self.DUT.select_all(1)
        _mode = self.DUT.select(1)

        self.assertTrue(isinstance(_mode, RTKMode))
        self.assertEqual(_mode.mode_id, 1)
        self.assertEqual(_mode.description, 'Test Failure Mode #1')

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """
        (TestModeModel): select() should return None when a non-existent Mode ID is requested.
        """

        _mode = self.DUT.select(100)

        self.assertEqual(_mode, None)

    @attr(all=True, unit=True)
    def test03a_insert_functional_mode(self):
        """
        (TestModeModel): insert() should return a zero error code on success when inserting a functional failure Mode.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(function_id=1, hardware_id=-1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                               'the RTK Program database.')

    @attr(all=True, unit=True)
    def test03b_insert_hardware_mode(self):
        """
        (TestModeModel): insert() should return a zero error code on success when inserting a hardware failure Mode.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(function_id=-1, hardware_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                               'the RTK Program database.')

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """
        (TestModeModel): delete() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                               'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """
        (TestModeModel): delete() should return a non-zero error code when passed a Mode ID that doesn't exist.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to delete non-existent '
                               'Mode ID 300.')

    @attr(all=True, unit=True)
    def test_05a_update(self):
        """
        (TestModeModel): update() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _mode = self.DUT.tree.get_node(1).data
        _mode.isolation_method = 'Method to isolate the failure.'

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test_05b_update_non_existent_id(self):
        """
        (TestModeModel): update() should return a non-zero error code when passed a Mode ID that doesn't exist.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                               'Mode ID 100.')

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """
        (TestModeModel): update_all() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test07a_calculate_criticality(self):
        """
        (TestModeModel) calculate_criticality should return False on success
        """

        self.DUT.select_all(1)
        _mode = self.DUT.select(1)
        _mode.mode_ratio = 0.5
        _mode.mode_op_time = 5.8
        _mode.effect_probability = 0.43

        _error_code, _msg = self.DUT.calculate_criticality(1, 0.0000563)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Calculating failure mode 1 '
                               'criticality.')
        self.assertAlmostEqual(_mode.mode_hazard_rate, 2.815e-05)
        self.assertAlmostEqual(_mode.mode_criticality, 7.02061e-05)

    @attr(all=False, unit=True)
    def test07b_calculate_criticality_out_of_range_hazard_rate_input(self):
        """
        (TestModeModel) calculate_criticality raises OutOfRangeError for item_hr <= 0.0
        """

        self.DUT.select_all(1)
        _mode = self.DUT.select(1)
        _mode.mode_ratio = 1.0
        _mode.mode_op_time = 1.0
        _mode.effect_probability = 1.0

        self.assertRaises(OutOfRangeError,
                          self.DUT.calculate_criticality, 1, 0.0)

    @attr(all=False, unit=True)
    def test07c_calculate_criticality_out_of_range_ratio_input(self):
        """
        (TestModeModel) calculate_criticality raises OutOfRangeError for 0.0 > ratio > 1.0
        """

        self.DUT.select_all(1)
        _mode = self.DUT.select(1)
        _mode.mode_ratio = -0.1
        _mode.mode_op_time = 1.0
        _mode.effect_probability = 1.0
        self.assertRaises(OutOfRangeError,
                          self.DUT.calculate_criticality, 1, 1.1)

    @attr(all=False, unit=True)
    def test07d_calculate_criticality_out_of_range_op_time_input(self):
        """
        (TestModeModel) calculate_criticality raises OutOfRangeError for 0.0 > operating time
        """

        self.DUT.select_all(1)
        _mode = self.DUT.select(1)
        _mode.mode_ratio = 0.5
        _mode.mode_op_time = -1.2
        _mode.effect_probability = 1.0
        self.assertRaises(OutOfRangeError,
                          self.DUT.calculate_criticality, 1, 1)

    @attr(all=False, unit=True)
    def test07e_calculate_criticality_out_of_range_eff_prob_input(self):
        """
        (TestModeModel) calculate_criticality raises OutOfRangeError for 0.0 <= effect probability =< 1.0
        """

        self.DUT.select_all(1)
        _mode = self.DUT.select(1)
        _mode.mode_ratio = 11.0
        _mode.mode_op_time = 1.0
        _mode.effect_probability = 2.3
        self.assertRaises(OutOfRangeError,
                          self.DUT.calculate_criticality, 1, 1)

    @attr(all=False, unit=True)
    def test07f_calculate_criticality_out_of_range_mode_hazard_rate(self):
        """
        (TestModeModel) calculate_criticality raises OutOfRangeError for 0 > mode hazard rate
        """

        self.DUT.select_all(1)
        _mode = self.DUT.select(1)
        _mode.mode_ratio = -0.5
        _mode.mode_op_time = 1.0
        _mode.effect_probability = 1.0
        self.assertRaises(OutOfRangeError,
                          self.DUT.calculate_criticality, 1, 1)

    @attr(all=False, unit=True)
    def test08g_calculate_criticality_out_of_range_mode_criticaility(self):
        """
        (TestModeModel) calculate_criticality raises OutOfRangeError for 0 > mode criticality
        """

        self.DUT.select_all(1)
        _mode = self.DUT.select(1)
        _mode.mode_ratio = -0.5
        _mode.mode_op_time = 1.0
        _mode.effect_probability = 1.0
        self.assertRaises(OutOfRangeError,
                          self.DUT.calculate_criticality, 1, 1)


class Test01ModeController(unittest.TestCase):
    """
    Class for testing the Mode Data Controller class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Mode Data Controller.
        """

        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {'host'    : 'localhost',
                                            'socket'  : 3306,
                                            'database': '/tmp/TestDB.rtk',
                                            'user'    : '',
                                            'password': ''}

        self.Configuration.RTK_DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG',
                                    '/tmp/RTK_debug.log')
        self.Configuration.RTK_USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO',
                                    '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(bind=self.dao.engine, autoflush=False,
                                       expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)
        self.dao.db_add([RTKMode(), ], self.session)
        self.dao.db_add([RTKMode(), ], self.session)

        self.DUT = Mode(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """
        (TestModeController) __init__ should return a Mode Data Controller
        """

        self.assertTrue(isinstance(self.DUT, Mode))
        self.assertTrue(isinstance(self.DUT._dtm_mode, Model))

    @attr(all=True, unit=True)
    def test01a_request_select_all_functional(self):
        """
        (TestModeController) request_select_all() should return a Tree of RTKMode models.
        """

        _tree = self.DUT.request_select_all(1, True)

        self.assertTrue(isinstance(_tree.get_node(1).data, RTKMode))

    @attr(all=True, unit=True)
    def test01b_request_select_all_hardware(self):
        """
        (TestModeController) request_select_all() should return a Tree of RTKMode models.
        """

        _tree = self.DUT.request_select_all(1)

        self.assertTrue(isinstance(_tree.get_node(1).data, RTKMode))

    @attr(all=True, unit=True)
    def test02a_request_select(self):
        """
        (TestModeController) request_select() should return an RTKMode model.
        """

        self.DUT.request_select_all(1)

        _mode = self.DUT.request_select(1)

        self.assertTrue(isinstance(_mode, RTKMode))

    @attr(all=True, unit=True)
    def test02b_request_select_non_existent_id(self):
        """
        (TestModeController) request_select() should return None when requesting a Mode that doesn't exist.
        """

        _mode = self.DUT.request_select(100)

        self.assertEqual(_mode, None)

    @attr(all=True, unit=True)
    def test03a_request_insert(self):
        """
        (TestModeController) request_insert() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_insert(function_id=1,
                                                 hardware_id=-1))

    @attr(all=True, unit=True)
    def test04a_request_delete(self):
        """
        (TestModeController) request_delete() should return False on success.
        """

        self.DUT.request_select_all(1)
        self.DUT.request_insert(function_id=1, hardware_id=-1)

        self.assertFalse(self.DUT.request_delete(self.DUT._dtm_mode.last_id))

    @attr(all=True, unit=True)
    def test04a_request_delete_non_existent_id(self):
        """
        (TestModeController) request_delete() should return True when attempting to delete a non-existent Mode.
        """

        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_delete(100))

    @attr(all=True, unit=True)
    def test05a_request_update(self):
        """
        (TestModeController) request_update() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update(1))

    @attr(all=True, unit=True)
    def test05b_request_update_non_existent_id(self):
        """
        (TestModeController) request_update() should return True when attempting to save a non-existent Mode.
        """

        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_update(100))

    @attr(all=True, unit=True)
    def test06a_request_update_all(self):
        """
        (TestModeController) request_update_all() should return False on success.
        """

        self.DUT.request_select_all(1)

        _error_code, _msg = self.DUT.request_update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test07a_request_calculate_criticality(self):
        """
        (TestModeController) request_calculate_criticality() should return False on success.
        """

        self.DUT.request_select_all(1)
        _mode = self.DUT.request_select(1)
        _mode.mode_ratio = 0.5
        _mode.mode_op_time = 5.8
        _mode.effect_probability = 0.43

        self.assertFalse(self.DUT.request_calculate_criticality(1, 0.0000563))
        self.assertAlmostEqual(_mode.mode_hazard_rate, 2.815e-05)
        self.assertAlmostEqual(_mode.mode_criticality, 7.02061e-05)

