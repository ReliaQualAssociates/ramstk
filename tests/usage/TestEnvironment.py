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

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from usage.Environment import Model, Environment
from dao import DAO
from dao import RTKEnvironment

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestEnvironmentModel(unittest.TestCase):
    """
    Class for testing the Environment model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Environment model class.
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
        self.dao.db_add([RTKEnvironment(), ], self.session)
        self.dao.db_add([RTKEnvironment(), ], self.session)

        self.DUT = Model(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestEnvironmentModel) __init__() should create an Environment data model.
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))
        self.assertEqual(self.DUT._last_id, None)

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
        self.assertEqual(_environment.name, 'Condition Name')

    @attr(all=True, unit=True)
    def test02b_retrieve_non_existent_id(self):
        """
        (TestEnvironmentModel): select() should return None when passed an Environment ID that doesn't exist.
        """

        self.DUT.select_all(1)
        self.assertEqual(self.DUT.select(100), None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """
        (TestEnvironmentModel): insert() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                               'the RTK Program database.')

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """
        (TestEnvironmentModel): delete() should return a zero error code on success.
        """

        self.DUT.select_all(1)
        self.DUT.insert(1)

        _error_code, _msg = self.DUT.delete(self.DUT._last_id)

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

        self.assertEqual(_error_code, 1000)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to delete non-existent '
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

        self.assertEqual(_error_code, 2136)
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


class Test01EnvironmentController(unittest.TestCase):
    """
    Class for testing the Environment Data Controller class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Environment Data Controller.
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
        self.dao.db_add([RTKEnvironment(), ], self.session)
        self.dao.db_add([RTKEnvironment(), ], self.session)

        self.DUT = Environment(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """
        (TestEnvironmentController) __init__ should return a Mission Data Controller
        """

        self.assertTrue(isinstance(self.DUT, Environment))
        self.assertTrue(isinstance(self.DUT._dtm_environment, Model))

    @attr(all=True, unit=False)
    def test01_request_select_all(self):
        """
        (TestEnvironmentController) request_select_all() should return a Tree of RTKEnvironment models.
        """

        _tree = self.DUT.request_select_all(1)

        self.assertTrue(isinstance(_tree.get_node(1).data, RTKEnvironment))

    @attr(all=True, unit=False)
    def test02a_request_select(self):
        """
        (TestEnvironmentController) request_select() should return an RTKv model.
        """

        self.DUT.request_select_all(1)

        self.assertTrue(isinstance(self.DUT.request_select(1), RTKEnvironment))

    @attr(all=True, unit=False)
    def test02b_request_non_existent_id(self):
        """
        (TestEnvironmentController) request_select() should return None when requesting a Mission that doesn't exist.
        """

        self.assertEqual(self.DUT.request_select(100), None)

    @attr(all=True, unit=False)
    def test03a_request_insert(self):
        """
        (TestEnvironmentController) request_insert() should return False on success.
        """

        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_insert(1))

    @attr(all=True, unit=False)
    def test04a_request_delete(self):
        """
        (TestEnvironmentController) request_delete() should return False on success.
        """

        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_delete(2))

    @attr(all=True, unit=False)
    def test04a_request_delete_non_existent_id(self):
        """
        (TestEnvironmentController) request_delete() should return True when attempting to delete a non-existent Mission.
        """

        self.DUT.request_select_all(1)
        self.assertTrue(self.DUT.request_delete(100))

    @attr(all=True, unit=False)
    def test05a_request_update(self):
        """
        (TestEnvironmentController) request_update() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update(1))

    @attr(all=True, unit=False)
    def test05b_request_update_non_existent_id(self):
        """
        (TestEnvironmentController) request_update() should return True when attempting to save a non-existent Mission.
        """

        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_update(100))

    @attr(all=True, unit=False)
    def test06a_request_update_all(self):
        """
        (TestEnvironmentController) request_update_all() should return False on success.
        """

        self.DUT.request_select_all(1)

        _error_code, _msg = self.DUT.request_update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')
