# -*- coding: utf-8 -*-
#
#       rtk.tests.fmea.TestCause.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Cause class."""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from analyses.fmea import dtmCause
from dao import DAO
from dao import RTKCause

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "weibullguy" Rowland'


class TestCauseDataModel(unittest.TestCase):
    """Class for testing the Cause model class."""

    def setUp(self):
        """Set up the test fixture for the Cause model class."""
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

        self.DUT = dtmCause(self.dao)

    @attr(all=True, unit=True)
    def test00_cause_create(self):
        """(TestCauseModel) __init__ should return instance of Cause data model."""
        self.assertTrue(isinstance(self.DUT, dtmCause))
        self.assertEqual(self.DUT.last_id, None)

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """(TestCauseModel): select_all() should return a Tree() object populated with RTKCause instances on success."""
        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKCause))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """(TestCauseModel): select() should return an instance of the RTKCause data model on success."""
        self.DUT.select_all(1)
        _cause = self.DUT.select(1)

        self.assertTrue(isinstance(_cause, RTKCause))
        self.assertEqual(_cause.cause_id, 1)
        self.assertEqual(_cause.description, 'Test Failure Cause #1')

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """(TestCauseModel): select() should return None when a non-existent Cause ID is requested."""
        _cause = self.DUT.select(100)

        self.assertEqual(_cause, None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """(TestCauseModel): insert() should return a zero error code on success when inserting a hardware failure Cause."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(mechanism_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                               'the RTK Program database.')

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """(TestCauseModel): delete() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                               'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """(TestCauseModel): delete() should return a non-zero error code when passed a Cause ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                               'Cause ID 300.')

    @attr(all=True, unit=True)
    def test_05a_update(self):
        """(TestCauseModel): update() should return a zero error code on success."""
        self.DUT.select_all(1)

        _cause = self.DUT.tree.get_node(1).data
        _cause.description = 'Test Failure Cause #1'

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test_05b_update_non_existent_id(self):
        """(TestCauseModel): update() should return a non-zero error code when passed a Cause ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                               'Cause ID 100.')

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """(TestCauseModel): update_all() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')
