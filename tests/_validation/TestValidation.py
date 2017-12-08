#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._validation.TestValidation.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Validation module algorithms and models."""

import sys
from os.path import dirname

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk", )

# pylint: disable=E0401,wrong-import-position
import Utilities as Utilities
from Configuration import Configuration
from dao import DAO
from dao import RTKValidation
from validation import dtmValidation, dtcValidation

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "weibullguy" Rowland'


class TestValidationDataModel(unittest.TestCase):
    """Class for testing the Validation data model class."""

    def setUp(self):
        """Set up the test fixture for the Validation class."""
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

        self.DUT = dtmValidation(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """(TestValidationDataModel) __init__ should return a Validation model."""
        self.assertTrue(isinstance(self.DUT, dtmValidation))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))

    @attr(all=True, unit=True)
    def test01_select_all(self):
        """(TestValidationDataModel) select_all() should return a Tree() object populated with RTKValidation instances on success."""
        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKValidation))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """(TestValidationDataModel) select() should return an instance of the RTKValidation data model on success."""
        self.DUT.select_all(1)
        _validation = self.DUT.select(1)

        self.assertTrue(isinstance(_validation, RTKValidation))
        self.assertEqual(_validation.validation_id, 1)

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """(TestValidationDataModel) select() should return None when a non-existent Validation ID is requested."""
        _validation = self.DUT.select(100)

        self.assertEqual(_validation, None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """(TestValidationDataModel) insert() should return False on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(revision_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 2)

        self.DUT.delete(self.DUT.last_id)

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """(TestValidationDataModel) delete() should return a zero error code on success."""
        self.DUT.select_all(1)
        self.DUT.insert(revision_id=1)

        _error_code, _msg = self.DUT.delete(self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """(TestValidationDataModel) delete() should return a non-zero error code when passed a Validation ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                         'Validation ID 300.')

    @attr(all=True, unit=True)
    def test05a_update(self):
        """(TestValidationDataModel) update() should return a zero error code on success."""
        self.DUT.select_all(1)

        _validation = self.DUT.tree.get_node(self.DUT.last_id).data
        _validation.availability_logistics = 0.9832

        _error_code, _msg = self.DUT.update(self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test05b_update_non_existent_id(self):
        """(TestValidationDataModel) update() should return a non-zero error code when passed a Validation ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'Validation ID 100.')

    @attr(all=True, unit=True)
    def test05c_update_status(self):
        """(TestValidationDataModel) update_status() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_status(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Adding one or more items to the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """(TestValidationDataModel) update_all() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test07a_calculate_task_time(self):
        """(TestValidationDataModel) calculate_task_time() returns False on successfully calculating tasks times."""
        self.DUT.select_all(1)
        _validation = self.DUT.select(1)
        _validation.time_minimum = 25.2
        _validation.time_average = 36.8
        _validation.time_maximum = 44.1
        _validation.confidence = 0.95

        self.assertFalse(self.DUT.calculate_time(1))
        self.assertAlmostEqual(_validation.time_mean, 36.08333333)
        self.assertAlmostEqual(_validation.time_variance, 9.9225)

    @attr(all=True, unit=True)
    def test07b_calculate_task_cost(self):
        """(TestValidationDataModel) calculate_task_cost() returns False on successfully calculating tasks costs."""
        self.DUT.select_all(1)
        _validation = self.DUT.select(1)
        _validation.cost_minimum = 252.00
        _validation.cost_average = 368.00
        _validation.cost_maximum = 441.00
        _validation.confidence = 0.95

        self.assertFalse(self.DUT.calculate_costs(1))
        self.assertAlmostEqual(_validation.cost_mean, 360.83333333)
        self.assertAlmostEqual(_validation.cost_variance, 992.25)


class TestValidationDataController(unittest.TestCase):
    """Class for testing the Validation data controller class."""

    def setUp(self):
        """Set up the test fixture for the Validation class."""
        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {
            'host': 'localhost',
            'socket': 3306,
            'database': '/tmp/TestDB.rtk',
            'user': '',
            'password': ''
        }

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

        self.dao.RTK_SESSION.configure(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)

        self.DUT = dtcValidation(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """(TestValidationDataController) __init__ should return a Validation Data Controller."""
        self.assertTrue(isinstance(self.DUT, dtcValidation))
        # pylint: disable=protected-access
        self.assertTrue(isinstance(self.DUT._dtm_data_model, dtmValidation))

    @attr(all=True, unit=True)
    def test01_request_select_all(self):
        """(TestValidationDataController) request_select_all() should return a Tree of RTKValidation models."""
        _tree = self.DUT.request_select_all(1)

        self.assertTrue(isinstance(_tree.get_node(1).data, RTKValidation))

    @attr(all=True, unit=True)
    def test02a_request_select(self):
        """(TestValidationDataController) request_select() should return an RTKValidation model."""
        self.DUT.request_select_all(1)

        self.assertTrue(isinstance(self.DUT.request_select(1), RTKValidation))

    @attr(all=True, unit=True)
    def test02b_request_non_existent_id(self):
        """(TestValidationDataController) request_select() should return None when requesting a Validation that doesn't exist."""
        self.assertEqual(self.DUT.request_select(100), None)

    @attr(all=True, unit=True)
    def test03a_request_insert(self):
        """(TestValidationDataController) request_insert() should return False on success."""
        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_insert(revision_id=1))

    @attr(all=True, unit=True)
    def test04a_request_delete(self):
        """(TestValidationDataController) request_delete() should return False on success."""
        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_delete(2))

    @attr(all=True, unit=True)
    def test04a_request_delete_non_existent_id(self):
        """(TestValidationDataController) request_delete() should return True when attempting to delete a non-existent Validation."""
        self.DUT.request_select_all(1)
        self.assertTrue(self.DUT.request_delete(100))

    @attr(all=True, unit=True)
    def test05a_request_update(self):
        """(TestValidationDataController) request_update() should return False on success."""
        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update(1))

    @attr(all=True, unit=True)
    def test05b_request_update_non_existent_id(self):
        """(TestValidationDataController) request_update() should return True when attempting to save a non-existent Validation."""
        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_update(100))

    @attr(all=True, unit=True)
    def test06a_request_update_all(self):
        """(TestValidationDataController) request_update_all() should return False on success."""
        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update_all())

    @attr(all=True, unit=True)
    def test07a_request_calculate(self):
        """(TestValidationDataController) request_calculate() should return False on success."""
        self.DUT.request_select_all(1)
        _validation = self.DUT.request_select(1)
        _validation.cost_minimum = 252.00
        _validation.cost_average = 368.00
        _validation.cost_maximum = 441.00
        _validation.time_minimum = 25.2
        _validation.time_average = 36.8
        _validation.time_maximum = 44.1
        _validation.confidence = 0.95

        self.assertFalse(self.DUT.request_calculate(1))
        self.assertAlmostEqual(_validation.time_mean, 36.08333333)
        self.assertAlmostEqual(_validation.time_variance, 9.9225)
        self.assertAlmostEqual(_validation.cost_mean, 360.83333333)
        self.assertAlmostEqual(_validation.cost_variance, 992.25)
