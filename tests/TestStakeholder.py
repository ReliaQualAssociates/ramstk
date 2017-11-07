#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestStakeholder.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
This is the test class for testing Stakeholder module algorithms and models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(__file__)) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from Stakeholder import Model, Stakeholder
from dao import DAO
from dao import RTKStakeholder

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "weibullguy" Rowland'


class Test00StakeholderModel(unittest.TestCase):
    """
    Class for testing the Stakeholder data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Stakeholder class.
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
        self.dao.db_add([RTKStakeholder(), ], self.session)

        self.DUT = Model(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestStakeholderModel) __init__ should return a Stakeholder model
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))
        self.assertEqual(self.DUT._revision_id, None)

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """
        (TestStakeholderModel): select_all() should return a Tree() object populated with RTKStakeholder instances on success.
        """

        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKStakeholder))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """
        (TestStakeholderModel): select() should return an instance of the RTKStakeholder data model on success.
        """

        self.DUT.select_all(1)
        _stakeholder = self.DUT.select(1)

        self.assertTrue(isinstance(_stakeholder, RTKStakeholder))
        self.assertEqual(_stakeholder.stakeholder_id, 1)
        self.assertEqual(_stakeholder.description, '')

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """
        (TestStakeholderModel): select() should return None when a non-existent Stakeholder ID is requested.
        """

        _stakeholder = self.DUT.select(100)

        self.assertEqual(_stakeholder, None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """
        (TestStakeholderModel): insert() should return False on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                               'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 2)

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """
        (TestStakeholderModel): delete() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(2)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                               'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """
        (TestStakeholderModel): delete() should return a non-zero error code when passed a Stakeholder ID that doesn't exist.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to delete non-existent '
                               'Stakeholder ID 300.')

    @attr(all=True, unit=True)
    def test_05a_update(self):
        """
        (TestStakeholderModel): update() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _stakeholder = self.DUT.tree.get_node(1).data
        _stakeholder.description = 'Be very reliable.'

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test_05b_update_non_existent_id(self):
        """
        (TestStakeholderModel): update() should return a non-zero error code when passed a Stakeholder ID that doesn't exist.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                               'Stakeholder ID 100.')

    @attr(all=True, unit=True)
    def test_06a_update_all(self):
        """
        (TestStakeholderModel): update_all() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test07a_calculate_weight(self):
        """
        (TestStakeholder) calculate_weight returns False on success and calculate values are correct
        """

        self.DUT.select_all(1)
        _stakeholder = self.DUT.select(1)

        _stakeholder.planned_rank = 4
        _stakeholder.customer_rank = 2
        _stakeholder.priority = 2
        _stakeholder.user_float_1 = 1.0
        _stakeholder.user_float_2 = 2.0
        _stakeholder.user_float_3 = 3.0
        _stakeholder.user_float_4 = 4.0
        _stakeholder.user_float_5 = 5.0

        self.assertFalse(self.DUT.calculate_weight(1))
        self.assertEqual(_stakeholder.improvement, 1.4)
        self.assertAlmostEqual(_stakeholder.overall_weight, 336.0)


class Test01StakeholderController(unittest.TestCase):
    """
    Class for testing the Stakeholder data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Stakeholder class.
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
        self.dao.db_add([RTKStakeholder(), ], self.session)

        self.DUT = Stakeholder(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """
        (TestStakeholder) __init__ should create a Stakeholder data controller
        """

        self.assertTrue(isinstance(self.DUT, Stakeholder))
        self.assertTrue(isinstance(self.DUT._dtm_stakeholder, Model))

    @attr(all=True, unit=True)
    def test01a_request_select_all(self):
        """
        (TestStakeholderController) request_select_all() should return a Tree of RTKStakeholder models.
        """

        _tree = self.DUT.request_select_all(1)

        self.assertTrue(isinstance(_tree.get_node(1).data, RTKStakeholder))

    @attr(all=True, unit=True)
    def test02a_request_select(self):
        """
        (TestStakeholderController) request_select() should return an RTKStakeholder model.
        """

        self.DUT.request_select_all(1)

        _stakeholder = self.DUT.request_select(1)

        self.assertTrue(isinstance(_stakeholder, RTKStakeholder))

    @attr(all=True, unit=True)
    def test02b_request_select_non_existent_id(self):
        """
        (TestStakeholderController) request_select() should return None when requesting a Stakeholder that doesn't exist.
        """

        self.DUT.request_select_all(1)

        _stakeholder = self.DUT.request_select(100)

        self.assertEqual(_stakeholder, None)

    @attr(all=True, unit=True)
    def test03a_request_insert(self):
        """
        (TestStakeholderController) request_insert() should return False on success.
        """

        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_insert())

    @attr(all=True, unit=True)
    def test04a_request_delete(self):
        """
        (TestStakeholderController) request_delete() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_delete(2))

    @attr(all=True, unit=True)
    def test04b_request_delete_non_existent_id(self):
        """
        (TestStakeholderController) request_delete() should return True when attempting to delete a non-existent Stakeholder.
        """

        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_delete(100))

    @attr(all=True, unit=True)
    def test05a_request_update(self):
        """
        (TestStakeholderController) request_update() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update(1))

    @attr(all=True, unit=True)
    def test05b_request_update_non_existent_id(self):
        """
        (TestStakeholderController) request_update() should return True when attempting to save a non-existent Stakeholder.
        """

        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_update(100))

    @attr(all=True, unit=True)
    def test06a_request_update_all(self):
        """
        (TestStakeholderController) request_update_all() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update_all())

    @attr(all=True, unit=True)
    def test07a_request_calculate_weight(self):
        """
        (TestStakeholderController) request_calculate_weight() should return False on success.
        """

        self.DUT.request_select_all(1)

        _stakeholder = self.DUT.request_select(1)
        _stakeholder.planned_rank = 4
        _stakeholder.customer_rank = 2
        _stakeholder.priority = 2
        _stakeholder.user_float_1 = 1.0
        _stakeholder.user_float_2 = 2.0
        _stakeholder.user_float_3 = 3.0
        _stakeholder.user_float_4 = 4.0
        _stakeholder.user_float_5 = 5.0

        self.assertFalse(self.DUT.request_calculate_weight(1))
        self.assertEqual(_stakeholder.improvement, 1.4)
        self.assertAlmostEqual(_stakeholder.overall_weight, 336.0)
