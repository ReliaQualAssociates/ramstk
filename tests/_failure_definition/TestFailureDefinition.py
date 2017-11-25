#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.failure_definition.TestFailureDefinition.py is part of The
#       RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
This is the test class for testing Failure Definition module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from failure_definition import dtmFailureDefinition, dtcFailureDefinition
from dao import DAO
from dao import RTKFailureDefinition

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestFailureDefinitionDataModel(unittest.TestCase):
    """
    Class for testing the Failure Definition model class.
    """

    def setUp(self):
        """(TestFailureDefinition): Set up the test fixture for the Failure Definition class."""
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

        self.DUT = dtmFailureDefinition(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """(TestFailureDefinitionModel): __init__ should return instance of a FailureDefition data model."""
        self.assertTrue(isinstance(self.DUT, dtmFailureDefinition))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))

    @attr(all=True, unit=True)
    def test01_select_all(self):
        """(TestFailureDefinitionModel): select_all should return a Tree() object populated with RTKFailureDefinitions instances on success."""
        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(
            isinstance(_tree.get_node(1).data, RTKFailureDefinition))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """(TestFailureDefinitionModel): select should return an instance of the RTKFailureDefinition data model on success."""
        self.DUT.select_all(1)
        _definition = self.DUT.select(1)

        self.assertTrue(isinstance(_definition, RTKFailureDefinition))
        self.assertEqual(_definition.definition_id, 1)
        self.assertEqual(_definition.definition, 'Failure Definition')

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """(TestFailureDefinitionModel): select() should return None when a non-existent Definition ID is requested."""
        _definition = self.DUT.select(100)

        self.assertEqual(_definition, None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """(TestFailureDefinitionModel): insert() should return False on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(revision_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 1)

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """(TestFailureDefinitionModel): delete() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(2)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """(TestFailureDefinitionModel): delete() should return a non-zero error code when passed a Revision ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(
            _msg,
            '  RTK ERROR: Attempted to delete non-existent Failure ' \
            'Definition ID 300.'
        )

    @attr(all=True, unit=True)
    def test_05a_update(self):
        """(TestFailureDefinitionModel): update() should return a zero error code on success."""
        self.DUT.select_all(1)

        _definition = self.DUT.tree.get_node(1).data
        _definition.definition = 'Test Failure Definition'

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test_05b_update_non_existent_id(self):
        """(TestFailureDefinition): update() should return a non-zero error code when passed a Failure Definition ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2207)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'Failure Definition ID 100.')

    @attr(all=True, unit=True)
    def test_06a_update_all(self):
        """(TestFailureDefinitionModel): update_all() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')


class TestFailureDefinitionDataController(unittest.TestCase):
    """
    Class for testing the Failure Definition data controller class.
    """

    def setUp(self):
        """(TestFailureDefinitionController) Set up the test fixture for the Failure Definition Data Controller."""
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

        self.DUT = dtcFailureDefinition(
            self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """(TestFailureDefinitionController) __init__ should return a Failure Definition Data Controller."""

        self.assertTrue(isinstance(self.DUT, dtcFailureDefinition))
        self.assertTrue(
            isinstance(self.DUT._dtm_data_model, dtmFailureDefinition))

    @attr(all=True, unit=True)
    def test01_request_select_all(self):
        """(TestFailureDefinitionController) request_select_all() should return a Tree of RTKFailureDefinition models."""
        _tree = self.DUT.request_select_all(1)

        self.assertTrue(
            isinstance(_tree.get_node(1).data, RTKFailureDefinition))

    @attr(all=True, unit=True)
    def test02a_request_select(self):
        """(TestFailureDefinitionController) request_select() should return an RTKFailureDefinition model."""
        self.DUT.request_select_all(1)

        self.assertTrue(
            isinstance(self.DUT.request_select(1), RTKFailureDefinition))

    @attr(all=True, unit=True)
    def test02b_request_non_existent_id(self):
        """(TestFailureDefinitionController) request_select() should return None when requesting a Failure Definition that doesn't exist."""
        self.assertEqual(self.DUT.request_select(100), None)

    @attr(all=True, unit=True)
    def test03a_request_insert(self):
        """(TestFailureDefinitionController) request_insert() should return False on success."""
        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_insert(revision_id=1))

    @attr(all=True, unit=True)
    def test04a_request_delete(self):
        """(TestFailureDefinitionController) request_delete() should return False on success."""
        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_delete(2))

    @attr(all=True, unit=True)
    def test04a_request_delete_non_existent_id(self):
        """(TestFailureDefinitionController) request_delete() should return True when attempting to delete a non-existent Failure Definition."""
        self.DUT.request_select_all(1)
        self.assertTrue(self.DUT.request_delete(100))

    @attr(all=True, unit=True)
    def test05a_request_update(self):
        """(TestFailureDefinitionController) request_update() should return False on success."""
        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update(1))

    @attr(all=True, unit=True)
    def test05b_request_update_non_existent_id(self):
        """(TestFailureDefinitionController) request_update() should return True when attempting to save a non-existent Failure Definition."""
        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_update(100))

    @attr(all=True, unit=True)
    def test06a_request_update_all(self):
        """(TestFailureDefinitionController) request_update_all() should return False on success."""
        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update_all())
