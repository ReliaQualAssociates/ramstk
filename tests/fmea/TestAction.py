# -*- coding: utf-8 -*-
#
#       rtk.tests.fmea.TestAction.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
This is the test class for testing the Action class.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

from datetime import date, timedelta

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from analyses.fmea.Action import Model, Action
from dao import DAO
from dao import RTKAction

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2015 Andrew "weibullguy" Rowland'


class Test00ActionModel(unittest.TestCase):
    """
    Class for testing the Action model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Action model class.
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
        self.dao.db_add([RTKAction(), ], self.session)
        self.dao.db_add([RTKAction(), ], self.session)

        self.DUT = Model(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestActionModel) __init__ should return instance of Action data model
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertEqual(self.DUT.last_id, None)

    @attr(all=True, unit=True)
    def test01a_select_all_functional(self):
        """
        (TestActionModel): select_all() should return a Tree() object populated with RTKAction instances on success.
        """

        _tree = self.DUT.select_all(1, True)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKAction))

    @attr(all=True, unit=True)
    def test01b_select_all_hardware(self):
        """
        (TestActionModel): select_all() should return a Tree() object populated with RTKAction instances on success.
        """

        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKAction))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """
        (TestActionModel): select() should return an instance of the RTKAction data model on success.
        """

        self.DUT.select_all(1)
        _action = self.DUT.select(1)

        self.assertTrue(isinstance(_action, RTKAction))
        self.assertEqual(_action.action_id, 1)
        self.assertEqual(_action.action_due_date,
                         date.today() + timedelta(days=30))

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """
        (TestActionModel): select() should return None when a non-existent Action ID is requested.
        """

        _action = self.DUT.select(100)

        self.assertEqual(_action, None)

    @attr(all=True, unit=True)
    def test03a_insert_functional_mode(self):
        """
        (TestActionModel): insert() should return False on success when inserting a functional FMEA action.
        """

        self.DUT.select_all(1, True)

        _error_code, _msg = self.DUT.insert(mode_id=1, cause_id=-1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                               'the RTK Program database.')

    @attr(all=True, unit=True)
    def test03b_insert_hardware_mode(self):
        """
        (TestActionModel): insert() should return False on success when inserting a hardware FMEA action.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(mode_id=-1, cause_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                               'the RTK Program database.')

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """
        (TestActionModel): delete() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                               'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """
        (TestActionModel): delete() should return a non-zero error code when passed a Mode ID that doesn't exist.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to delete non-existent '
                               'Action ID 300.')

    @attr(all=True, unit=True)
    def test_05a_update(self):
        """
        (TestActionModel): update() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _action = self.DUT.tree.get_node(1).data
        _action.action_recommended = 'Do this stuff and do it now!!'

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test_05b_update_non_existent_id(self):
        """
        (TestActionModel): update() should return a non-zero error code when passed an Action ID that doesn't exist.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                               'Action ID 100.')

    @attr(all=True, unit=True)
    def test_06a_update_all(self):
        """
        (TestActionModel): update_all() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')


class Test01ActionController(unittest.TestCase):
    """
    Class for testing the FMEA Action data controller.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Action model class.
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
        self.dao.db_add([RTKAction(), ], self.session)
        self.dao.db_add([RTKAction(), ], self.session)

        self.DUT = Action(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """
        (TestActionController) __init__ should return a Action Data Controller
        """

        self.assertTrue(isinstance(self.DUT, Action))
        self.assertTrue(isinstance(self.DUT._dtm_action, Model))

    @attr(all=True, unit=True)
    def test01a_request_select_all_functional(self):
        """
        (TestActionController) request_select_all() should return a Tree of RTKAction models.
        """

        _tree = self.DUT.request_select_all(1, True)

        self.assertTrue(isinstance(_tree.get_node(1).data, RTKAction))

    @attr(all=True, unit=True)
    def test01b_request_select_all_hardware(self):
        """
        (TestActionController) request_select_all() should return a Tree of RTKAction models.
        """

        _tree = self.DUT.request_select_all(1)

        self.assertTrue(isinstance(_tree.get_node(1).data, RTKAction))

    @attr(all=True, unit=True)
    def test02a_request_select(self):
        """
        (TestActionController) request_select() should return an RTKAction model.
        """

        self.DUT.request_select_all(1)

        _action = self.DUT.request_select(1)

        self.assertTrue(isinstance(_action, RTKAction))

    @attr(all=True, unit=True)
    def test02b_request_select_non_existent_id(self):
        """
        (TestActionController) request_select() should return None when requesting a Action that doesn't exist.
        """

        _action = self.DUT.request_select(100)

        self.assertEqual(_action, None)

    @attr(all=True, unit=True)
    def test03a_request_insert(self):
        """
        (TestActionController) request_insert() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_insert(mode_id=1,
                                                 cause_id=-1))

    @attr(all=True, unit=True)
    def test04a_request_delete(self):
        """
        (TestActionController) request_delete() should return False on success.
        """

        self.DUT.request_select_all(1)
        self.DUT.request_insert(mode_id=1, cause_id=-1)

        self.assertFalse(self.DUT.request_delete(self.DUT._dtm_action.last_id))

    @attr(all=True, unit=True)
    def test04a_request_delete_non_existent_id(self):
        """
        (TestActionController) request_delete() should return True when attempting to delete a non-existent Action.
        """

        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_delete(100))

    @attr(all=True, unit=True)
    def test05a_request_update(self):
        """
        (TestActionController) request_update() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update(1))

    @attr(all=True, unit=True)
    def test05b_request_update_non_existent_id(self):
        """
        (TestActionController) request_update() should return True when attempting to save a non-existent Action.
        """

        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_update(100))

    @attr(all=True, unit=True)
    def test06a_request_update_all(self):
        """
        (TestActionController) request_update_all() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update_all())
