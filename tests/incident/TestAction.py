#!/usr/bin/env python -O
"""
This is the test class for testing Incident Action module algorithms and
models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.verification.TestAction.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr
import numpy as np

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from incident.action.Action import Model, Action


class TestIncidentActionModel(unittest.TestCase):
    """
    Class for testing the IncidentAction data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the IncidentAction class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestIncidentAction) __init__ should return an IncidentAction model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.incident_id, None)
        self.assertEqual(self.DUT.action_id, None)
        self.assertEqual(self.DUT.prescribed_action, '')
        self.assertEqual(self.DUT.action_taken, '')
        self.assertEqual(self.DUT.action_owner, 0)
        self.assertEqual(self.DUT.due_date, 0)
        self.assertEqual(self.DUT.status, 0)
        self.assertEqual(self.DUT.approved_by, 0)
        self.assertEqual(self.DUT.approved_date, 0)
        self.assertEqual(self.DUT.approved, False)
        self.assertEqual(self.DUT.closed_by, 0)
        self.assertEqual(self.DUT.closed_date, 0)
        self.assertEqual(self.DUT.closed, False)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestIncidentAction) set_attributes should return a 0 error code on success
        """

        _values = (0, 1, 'Prescribed Action', 'Action Taken', 1, 0, 3, 1,
                   0, False, 2, 0, False)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestIncidentAction) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (None, 1, 'Prescribed Action', 'Action Taken', 1, 0, 3,
                   2, 0, False, 2, 0, False)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestIncidentAction) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 1, 'Prescribed Action', 'Action Taken',
                   1, 0, 3, 0, False, 2, 0, False)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestIncidentAction) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (None, None, '', '', 0, 0, 0, 0, 0, False,
                          0, 0, False))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestIncidentAction) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 1, 'Prescribed Action', 'Action Taken', 1, 0, 3,
                   2, 0, False, 2, 0, False)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)


class TestIncidentActionController(unittest.TestCase):
    """
    Class for testing the Incident Action data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Incident Action class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Action()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        (TestIncidentAction) __init__ should create a Incident Action data controller
        """

        self.assertTrue(isinstance(self.DUT, Action))
        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicActions, {})

    @attr(all=True, integration=True)
    def test_request_actions(self):
        """
        (TestIncidentAction) request_actions should return 0 on success
        """

        self.assertEqual(self.DUT.request_actions(self._dao, 1)[1], 0)

    @attr(all=True, integration=True)
    def test_add_action(self):
        """
        (TestIncidentAction) add_action should return 0 on success
        """

        self.assertEqual(self.DUT.request_actions(self._dao, 1)[1], 0)
        self.assertEqual(self.DUT.add_action(1)[1], 0)

    @attr(all=True, integration=True)
    def test_save_action(self):
        """
        (TestIncidentAction) save_action returns 0 on success
        """

        _values = (0, 1, 'Prescribed Action', 'Action Taken', 1, 0, 3, 2,
                   0, False, 2, 0, False)

        self.assertEqual(self.DUT.request_actions(self._dao, 1)[1], 0)
        _action = self.DUT.dicActions[min(self.DUT.dicActions.keys())]
        _action.set_attributes(_values)

        (_results,
         _error_code) = self.DUT.save_action(min(self.DUT.dicActions.keys()))

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_all_actions(self):
        """
        (TestIncidentAction) save_all_actions returns 0 on success
        """

        self.assertEqual(self.DUT.request_actions(self._dao, 1)[1], 0)
        self.assertFalse(self.DUT.save_all_actions())
