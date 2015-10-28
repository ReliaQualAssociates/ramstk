#!/usr/bin/env python -O
"""
This is the test class for testing Survival module algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.survival.TestSurvival.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr
import numpy as np

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from survival.Survival import Model, Survival


class TestSurvivalModel(unittest.TestCase):
    """
    Class for testing the Survival data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Survival class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestSurvival) __init__ should return an Survival model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT._nevada_chart, False)
        self.assertEqual(self.DUT.dicDatasets, {})
        self.assertEqual(self.DUT.scale, [0.0, 0.0, 0.0])
        self.assertEqual(self.DUT.shape, [0.0, 0.0, 0.0])
        self.assertEqual(self.DUT.location, [0.0, 0.0, 0.0])
        self.assertEqual(self.DUT.variance, [0.0, 0.0, 0.0])
        self.assertEqual(self.DUT.covariance, [0.0, 0.0, 0.0])
        self.assertEqual(self.DUT.revision_id, 0)
        self.assertEqual(self.DUT.survival_id, 0)
        self.assertEqual(self.DUT.assembly_id, 0)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.source, 0)
        self.assertEqual(self.DUT.distribution_id, 0)
        self.assertEqual(self.DUT.confidence, 0.75)
        self.assertEqual(self.DUT.confidence_type, 0)
        self.assertEqual(self.DUT.confidence_method, 0)
        self.assertEqual(self.DUT.fit_method, 0)
        self.assertEqual(self.DUT.rel_time, 100.0)
        self.assertEqual(self.DUT.n_rel_points, 0)
        self.assertEqual(self.DUT.n_suspensions, 0)
        self.assertEqual(self.DUT.n_failures, 0)
        self.assertEqual(self.DUT.mhb, 0.0)
        self.assertEqual(self.DUT.lp, 0.0)
        self.assertEqual(self.DUT.lr, 0.0)
        self.assertEqual(self.DUT.aic, 0.0)
        self.assertEqual(self.DUT.bic, 0.0)
        self.assertEqual(self.DUT.mle, 0.0)
        self.assertEqual(self.DUT.start_time, 0.0)
        self.assertEqual(self.DUT.end_time, 0.0)
        self.assertEqual(self.DUT.start_date, 0)
        self.assertEqual(self.DUT.end_date, 0)
        self.assertEqual(self.DUT.n_datasets, 0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestSurvival) set_attributes should return a 0 error code on success
        """

        _values = (0, 1, 2, 'Description', 3, 4, 0.5, 6, 7, 8, 90.0, 10, 11,
                   12, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21, 22,
                   23, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0,
                   33.0, 34.0, 35.0, 36.0, 37.0, 38.0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestSurvival) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, 1, 2, 'Description', 3, 4, 0.5, 6, 7, 8, 90.0, 10, 11,
                   12, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21, 22,
                   23, 24.0, 25.0, 26.0, 27.0, 28.0, None, 30.0, 31.0, 32.0,
                   33.0, 34.0, 35.0, 36.0, 37.0, 38.0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestSurvival) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 1, 2, 'Description', 3, 4, 0.5, 6, 7, 8, 90.0, 10, 11,
                   12, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21, 22,
                   24.0, 25.0, 26.0, 27.0, 28.0, 30.0, 31.0, 32.0, 33.0, 34.0,
                   35.0, 36.0, 37.0, 38.0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestSurvival) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (0, 0, 0, '', 0, 0, 0.75, 0, 0, 0, 100.0, 0, 0, 0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0,
                          [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestSurvival) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 1, 2, 'Description', 3, 4, 0.5, 6, 7, 8, 90.0, 10, 11,
                   12, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21, 22,
                   23, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0,
                   33.0, 34.0, 35.0, 36.0, 37.0, 38.0)
        _results = (0, 1, 2, 'Description', 3, 4, 0.5, 6, 7, 8, 90.0, 10, 11,
                   12, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21, 22,
                   [23.0, 24.0, 25.0], [26.0, 27.0, 28.0],
                   [29.0, 30.0, 31.0], [32.0, 33.0, 34.0], [35.0, 36.0, 37.0])

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _results)


class TestSurvivalController(unittest.TestCase):
    """
    Class for testing the Survival data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Survival class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Survival()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        (TestSurvival) __init__ should create a Survival data controller
        """

        self.assertTrue(isinstance(self.DUT, Survival))
        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicSurvival, {})

    @attr(all=True, integration=True)
    def test_request_survival(self):
        """
        (TestSurvival) request_survival should return 0 on success
        """

        self.assertEqual(self.DUT.request_survival(self._dao, 0)[1], 0)

    @attr(all=True, integration=True)
    def test_add_survival(self):
        """
        (TestSurvival) add_survival should return 0 on success
        """

        self.assertEqual(self.DUT.request_survival(self._dao, 0)[1], 0)
        self.assertEqual(self.DUT.add_survival(0)[1], 0)

    @attr(all=True, integration=True)
    def test_delete_survival(self):
        """
        (TestSurvival) delete_survival should return 0 on success
        """

        self.assertEqual(self.DUT.request_survival(self._dao, 0)[1], 0)
        _survival = self.DUT.dicSurvival[max(self.DUT.dicSurvival.keys())]

        self.assertEqual(self.DUT.delete_survival(_survival.survival_id)[1], 0)

    @attr(all=True, integration=True)
    def test_save_survival(self):
        """
        (TestSurvival) save_survival returns 0 on success
        """

        _values = (0, 1, 2, 'Test Description', 3, 4, 0.5, 6, 7, 8, 90.0, 10,
                   11, 12, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21,
                   22, 23, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0,
                   32.0, 33.0, 34.0, 35.0, 36.0, 37.0)

        self.assertEqual(self.DUT.request_survival(self._dao, 0)[1], 0)
        _survival = self.DUT.dicSurvival[min(self.DUT.dicSurvival.keys())]
        _survival.set_attributes(_values)

        (_results, _error_code) = self.DUT.save_survival(min(
                                                self.DUT.dicSurvival.keys()))

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_all_survivals(self):
        """
        (TestSurvival) save_all_survivals returns False on success
        """

        self.assertEqual(self.DUT.request_survival(self._dao, 0)[1], 0)
        self.assertFalse(self.DUT.save_all_survivals())

    @attr(all=True, integration=True)
    def test_request_datasets(self):
        """
        (TestSurvival) request_datasets should return 0 on success
        """

        self.DUT.request_survival(self._dao, 0)

        self.assertEqual(self.DUT.request_datasets(min(self.DUT.dicSurvival.keys()))[1], 0)

    @attr(all=True, integration=True)
    def test_add_dataset(self):
        """
        (TestSurvival) add_dataset should return 0 on success
        """

        self.DUT.request_survival(self._dao, 0)
        _survival = self.DUT.dicSurvival[min(self.DUT.dicSurvival.keys())]
        self.DUT.add_dataset(_survival.survival_id)

    @attr(all=True, integration=True)
    def test_delete_dataset(self):
        """
        (TestSurvival) delete_dataset should return 0 on success
        """

        self.DUT.request_survival(self._dao, 0)
        _survival = self.DUT.dicSurvival[min(self.DUT.dicSurvival.keys())]

        self.DUT.request_datasets(_survival.survival_id)
        _dataset = _survival.dicDatasets[max(_survival.dicDatasets.keys())]

        self.DUT.delete_dataset(_survival.survival_id, _dataset.dataset_id)

    @attr(all=True, integration=True)
    def test_save_dataset(self):
        """
        (TestSurvival) save_dataset returns 0 on success
        """

        self.DUT.request_survival(self._dao, 0)[1]
        _survival = self.DUT.dicSurvival[min(self.DUT.dicSurvival.keys())]
        self.DUT.request_datasets(_survival.survival_id)
        _dataset = _survival.dicDatasets[min(_survival.dicDatasets.keys())]
        _record = _dataset.dicRecords[min(_dataset.dicRecords.keys())]
        _record[2] = 138.6

        (_results, _error_code) = self.DUT.save_dataset(_survival.survival_id,
                                                        _dataset.dataset_id)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_add_record(self):
        """
        (TestSurvival) add_record should return 0 on success
        """

        self.DUT.request_survival(self._dao, 0)
        _survival = self.DUT.dicSurvival[min(self.DUT.dicSurvival.keys())]
        self.DUT.request_datasets(_survival.survival_id)
        _dataset = _survival.dicDatasets[min(_survival.dicDatasets.keys())]

        (_results, _error_code) = self.DUT.add_record(_survival.survival_id,
                                                      _dataset.dataset_id)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_delete_record(self):
        """
        (TestSurvival) delete_record should return 0 on success
        """

        self.DUT.request_survival(self._dao, 0)
        _survival = self.DUT.dicSurvival[min(self.DUT.dicSurvival.keys())]
        self.DUT.request_datasets(_survival.survival_id)
        _dataset = _survival.dicDatasets[min(_survival.dicDatasets.keys())]
        _record = _dataset.dicRecords[min(_dataset.dicRecords.keys())]

        (_results, _error_code) = self.DUT.delete_record(_survival.survival_id,
                                                         _dataset.dataset_id,
                                                         _record[0])

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)
