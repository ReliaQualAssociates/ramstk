#!/usr/bin/env python -O
"""
This is the test class for testing Validation module algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.verification.TestValidation.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr
import numpy as np

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from validation.Validation import Model, Validation


class TestValidationModel(unittest.TestCase):
    """
    Class for testing the Validation data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Validation class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestValidation) __init__ should return a Validation model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, 0)
        self.assertEqual(self.DUT.validation_id, 0)
        self.assertEqual(self.DUT.task_description, '')
        self.assertEqual(self.DUT.task_type, 0)
        self.assertEqual(self.DUT.task_specification, '')
        self.assertEqual(self.DUT.measurement_unit, 0)
        self.assertEqual(self.DUT.min_acceptable, 0.0)
        self.assertEqual(self.DUT.mean_acceptable, 0.0)
        self.assertEqual(self.DUT.max_acceptable, 0.0)
        self.assertEqual(self.DUT.variance_acceptable, 0.0)
        self.assertEqual(self.DUT.start_date, 719163)
        self.assertEqual(self.DUT.end_date, 719163)
        self.assertEqual(self.DUT.status, 0.0)
        self.assertEqual(self.DUT.minimum_time, 0.0)
        self.assertEqual(self.DUT.average_time, 0.0)
        self.assertEqual(self.DUT.maximum_time, 0.0)
        self.assertEqual(self.DUT.mean_time, 0.0)
        self.assertEqual(self.DUT.time_variance, 0.0)
        self.assertEqual(self.DUT.minimum_cost, 0.0)
        self.assertEqual(self.DUT.average_cost, 0.0)
        self.assertEqual(self.DUT.maximum_cost, 0.0)
        self.assertEqual(self.DUT.mean_cost, 0.0)
        self.assertEqual(self.DUT.cost_variance, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestValidation) set_attributes should return a 0 error code on success
        """

        _values = (0, 0, 'Description', 0, 'Specification', 0, 0.0, 0.0,
                   0.0, 0.0, 719163, 719163, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 95.0)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestValidation) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, 0, 'Description', 0, 'Specification', 0, 0.0, 0.0,
                   0.0, 0.0, 719163, 'Date', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 95.0)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestValidation) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 0, 'Description', 0, 'Specification', 0, 0.0, 0.0,
                   0.0, 0.0, 719163, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 95.0)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestValidation) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (0, 0, '', 0, '', 0, 0.0, 0.0, 0.0, 0.0, 719163,
                          719163, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 95.0))

    @attr(all=True, unit=True)
    def test_calculate_task_time(self):
        """
        (TestValidation) calculate returns False on successfully calculating tasks times
        """

        self.DUT.minimum_time = 25.2
        self.DUT.average_time = 36.8
        self.DUT.maximum_time = 44.1

        self.assertFalse(self.DUT.calculate())
        self.assertAlmostEqual(self.DUT.mean_time, 36.08333333)
        self.assertAlmostEqual(self.DUT.time_variance, 9.9225)

    @attr(all=True, unit=True)
    def test_calculate_task_cost(self):
        """
        (TestValidation) calculate returns False on successfully calculating tasks costs
        """

        self.DUT.minimum_cost = 252.00
        self.DUT.average_cost = 368.00
        self.DUT.maximum_cost = 441.00
        self.DUT.confidence = 0.95

        self.assertFalse(self.DUT.calculate())
        self.assertAlmostEqual(self.DUT.mean_cost, 360.83333333)
        self.assertAlmostEqual(self.DUT.cost_variance, 992.25)


class TestValidationController(unittest.TestCase):
    """
    Class for testing the Validation data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Validation class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Validation()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        (TestValidation) __init__ should create a Validation data controller
        """

        self.assertTrue(isinstance(self.DUT, Validation))
        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicTasks, {})
        self.assertEqual(self.DUT.dicStatus, {})

    @attr(all=True, integration=True)
    def test_request_tasks(self):
        """
        (TestValidation) request_tasks should return 0 on success
        """

        self.assertEqual(self.DUT.request_tasks(self._dao, 0)[1], 0)

    @attr(all=True, integration=True)
    def test_add_task(self):
        """
        (TestValidation) add_task should return 0 on success
        """

        self.assertEqual(self.DUT.request_tasks(self._dao, 0)[1], 0)
        self.assertEqual(self.DUT.add_task(0)[1], 0)

    @attr(all=True, integration=True)
    def test_delete_task(self):
        """
        (TestValidation) delete_task returns 0 on success
        """

        self.assertEqual(self.DUT.request_tasks(self._dao, 0)[1], 0)
        (_results, _error_code) = self.DUT.delete_task(self.DUT._last_id)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_task(self):
        """
        (TestValidation) save_task returns 0 on success
        """

        _values = (0, 0, 'Description', 0, 'Specification', 0, 0.0, 0.0,
                   0.0, 0.0, 719163, 738163, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 90.0)

        self.assertEqual(self.DUT.request_tasks(self._dao, 0)[1], 0)
        _task = self.DUT.dicTasks[min(self.DUT.dicTasks.keys())]
        _task.set_attributes(_values)

        (_results, _error_code) = self.DUT.save_task(min(self.DUT.dicTasks.keys()))

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_all_tasks(self):
        """
        (TestValidation) save_all_tasks returns 0 on success
        """

        self.assertEqual(self.DUT.request_tasks(self._dao, 0)[1], 0)
        self.assertFalse(self.DUT.save_all_tasks())
