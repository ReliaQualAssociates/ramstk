#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       TestEnvironment.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
This is the test class for testing the Environment class.
"""

# We add this to ensure the imports within the rtk packages will work.
import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from usage import dtmEnvironment
from dao import DAO
from dao import RTKEnvironment

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestEnvironmentDataModel(unittest.TestCase):
    """
    Class for testing the Environment model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Environment model class.
        """

        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {
            'host': 'localhost',
            'socket': 3306,
            'database': '/tmp/TestDB.rtk',
            'user': '',
            'password': ''
        }

        self.Configuration.DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG', '/tmp/RTK_debug.log')
        self.Configuration.USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO', '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)

        self.DUT = dtmEnvironment(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestEnvironmentModel) __init__() should create an Environment data model.
        """

        self.assertTrue(isinstance(self.DUT, dtmEnvironment))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))
        self.assertEqual(self.DUT.last_id, None)

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """
        (TestEnvironmentModel): select_all() should return a Tree() object populated with RTKEnvironment instances on success.
        """

        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKEnvironment))

    @attr(all=True, unit=True)
    def test01b_select_all_non_existent_id(self):
        """
        (TestEnvironmentModel): select_all() should return an empty Tree() when passed an Environment ID that doesn't exist.
        """

        _tree = self.DUT.select_all(100)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertEqual(len(_tree.all_nodes()), 1)

    @attr(all=True, unit=True)
    def test02a_select(self):
        """
        (TestEnvironmentModel): select() should return an instance of the RTKEnvironment data model on success.
        """

        self.DUT.select_all(1)
        _environment = self.DUT.select(1)

        self.assertTrue(isinstance(_environment, RTKEnvironment))
        self.assertEqual(_environment.environment_id, 1)
        self.assertEqual(_environment.name, 'Test Environmental Condition')

    @attr(all=True, unit=True)
    def test02b_retrieve_non_existent_id(self):
        """
        (TestEnvironmentModel): select() should return None when passed an Environment ID that doesn't exist.
        """

        self.DUT.select_all(1)
        self.assertEqual(self.DUT.select(100), None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """(TestEnvironmentModel): insert() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(phase_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')

        self.DUT.delete(self.DUT.last_id)

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """(TestEnvironmentModel): delete() should return a zero error code on success."""
        self.DUT.select_all(1)
        self.DUT.insert(phase_id=1)

        _error_code, _msg = self.DUT.delete(self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """
        (TestEnvironmentModel): delete() should return a non-zero error code when passed a Environment ID that doesn't exist.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(100)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                         'Environment ID 100.')

    @attr(all=True, unit=True)
    def test_05a_update(self):
        """
        (TestEnvironmentModel): update() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _environment = self.DUT.tree.get_node(1).data
        _environment.description = 'Test Mission Description'

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test_05b_update_non_existent_id(self):
        """
        (TestEnvironmentModel): update() should return a non-zero error code when passed a Environment ID that doesn't exist.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'Environment ID 100.')

    @attr(all=True, unit=True)
    def test_06a_update_all(self):
        """
        (TestEnvironmentModel): update_all() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')
