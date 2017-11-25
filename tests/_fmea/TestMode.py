# -*- coding: utf-8 -*-
#
#       tests._fmea.TestMode.py is part of The RTK Project
#
# All rights reserved.
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
from analyses.fmea import dtmMode
from dao import DAO
from dao import RTKMode

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "weibullguy" Rowland'


class TestModeDataModel(unittest.TestCase):
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

        self.DUT = dtmMode(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestModeModel) __init__ should return instance of Mode data model
        """
        self.assertTrue(isinstance(self.DUT, dtmMode))
        self.assertEqual(self.DUT.last_id, None)

    @attr(all=True, unit=True)
    def test01a_select_all_functional(self):
        """
        (TestModeModel): select_all() should return a Tree() object populated with RTKMode instances on success.
        """
        _tree = self.DUT.select_all(3, functional=True)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKMode))

    @attr(all=True, unit=True)
    def test01b_select_all_hardware(self):
        """
        (TestModeModel): select_all() should return a Tree() object populated with RTKMode instances on success.
        """
        _tree = self.DUT.select_all(3, functional=False)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKMode))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """
        (TestModeModel): select() should return an instance of the RTKMode data model on success.
        """
        self.DUT.select_all(3, functional=False)
        _mode = self.DUT.select(1)

        self.assertTrue(isinstance(_mode, RTKMode))
        self.assertEqual(_mode.mode_id, 1)
        self.assertEqual(_mode.description, 'Test Failure Mode #1')

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """
        (TestModeModel): select() should return None when a non-existent Mode ID is requested.
        """
        self.DUT.select_all(3, functional=False)
        _mode = self.DUT.select(100)

        self.assertEqual(_mode, None)

    @attr(all=True, unit=True)
    def test03a_insert_functional_mode(self):
        """
        (TestModeModel): insert() should return a zero error code on success when inserting a functional failure Mode.
        """
        self.DUT.select_all(3, functional=True)

        _error_code, _msg = self.DUT.insert(function_id=1, hardware_id=-1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                               'the RTK Program database.')

    @attr(all=True, unit=True)
    def test03b_insert_hardware_mode(self):
        """
        (TestModeModel): insert() should return a zero error code on success when inserting a hardware failure Mode.
        """
        self.DUT.select_all(3, functional=False)

        _error_code, _msg = self.DUT.insert(function_id=-1, hardware_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                               'the RTK Program database.')

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """
        (TestModeModel): delete() should return a zero error code on success.
        """
        self.DUT.select_all(3, functional=False)
        self.DUT.insert(function_id=-1, hardware_id=1)

        _error_code, _msg = self.DUT.delete(self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                               'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """
        (TestModeModel): delete() should return a non-zero error code when passed a Mode ID that doesn't exist.
        """
        self.DUT.select_all(3, functional=False)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                               'Mode ID 300.')

    @attr(all=True, unit=True)
    def test_05a_update(self):
        """
        (TestModeModel): update() should return a zero error code on success.
        """
        self.DUT.select_all(3, functional=False)

        _mode = self.DUT.select(1)
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
        self.DUT.select_all(3, functional=False)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                               'Mode ID 100.')

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """
        (TestModeModel): update_all() should return a zero error code on success.
        """
        self.DUT.select_all(3, functional=False)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')
