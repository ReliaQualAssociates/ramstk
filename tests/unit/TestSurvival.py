#!/usr/bin/env python -O
"""
This is the test class for testing Survival module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestSurvival.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr
import numpy as np

from collections import OrderedDict

import dao.DAO as _dao
from survival.Survival import Model, Survival
from survival.Record import Model as Record

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestSurvivalModel(unittest.TestCase):
    """
    Class for testing the Survival data model class.
    """

    KAPLANMEIER = [(1, 'Sub-System 1', 735835, 56.7, 56.7, 1, 1, 56.7, 1, 0,
                    719163, 719163, 0.0, 0.0, 0.0, 0, 0, 0, 'None', 'None',
                    'None'),
                   (1, 'Sub-System 1', 735623, 198.4, 198.4, 1, 3, 141.7, 1, 0,
                    719163, 719163, 0.0, 0.0, 0.0, 0, 0, 0, 'None', 'None',
                    'None'),
                   (1, 'Sub-System 1', 735682, 286.1, 286.1, 1, 2,
                    87.70000000000002, 1, 0, 719163, 719163, 0.0, 0.0, 0.0, 0,
                    0, 0, 'None', 'None', 'None'),
                   (1, 'Sub-System 1', 735698, 322.9, 322.9, 1, 6,
                    36.799999999999955, 1, 0, 719163, 719163, 0.0, 0.0, 0.0, 0,
                    0, 0, 'None', 'None', 'None'),
                   (1, 'Sub-System 1', 735710, 343.6, 343.6, 1, 1,
                    20.700000000000045, 1, 0, 719163, 719163, 0.0, 0.0, 0.0, 0,
                    0, 0, 'None', 'None', 'None'),
                   (1, 'Sub-System 1', 735734, 389.7, 389.7, 1, 3,
                    46.099999999999966, 1, 0, 719163, 719163, 0.0, 0.0, 0.0, 0,
                    0, 0, 'None', 'None', 'None'),
                   (1, 'Sub-System 1', 735749, 421.0, 421.0, 1, 1,
                    31.30000000000001, 1, 0, 719163, 719163, 0.0, 0.0, 0.0, 0,
                    0, 0, 'None', 'None', 'None')]

    NHPPPL = [(2, 'MIL-HDBK-217FN2 Example System', 735903, 53.0, 53.0, 1, 3,
               53.0, 1, 0, 719163, 719163, 0.0, 0.0, 0.0, 0, 0, 0, 'None',
               'None', 'None'),
              (2, 'MIL-HDBK-217FN2 Example System', 735912, 93.0, 93.0, 1, 2,
               40.0, 1, 0, 719163, 719163, 0.0, 0.0, 0.0, 0, 0, 0, 'None',
               'None', 'None'),
              (2, 'MIL-HDBK-217FN2 Example System', 735917, 120.0, 120.0, 1, 6,
               27.0, 1, 0, 719163, 719163, 0.0, 0.0, 0.0, 0, 0, 0, 'None',
               'None', 'None')]

    EXP = [(3, 'MIL-HDBK-217FN2 Example System', 719163, 0.0, 20.0, 1, 1, 20.0,
            1, 0, 719163, 719163, 0.0, 0.0, 0.0, 0, 0, 0, 'None', 'None',
            'None'),
           (3, 'MIL-HDBK-217FN2 Example System', 719163, 0.0, 40.0, 1, 1, 40.0,
            1, 0, 719163, 1, 719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', ''),
           (3, 'MIL-HDBK-217FN2 Example System', 719163, 0.0, 60.0, 1, 1, 60.0,
            1, 0, 719163, 1, 719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', ''),
           (3, 'MIL-HDBK-217FN2 Example System', 719163, 0.0, 100.0, 1, 1,
            100.0, 1, 0, 719163, 1, 719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', ''),
           (3, 'MIL-HDBK-217FN2 Example System', 719163, 0.0, 150.0, 1, 1,
            150.0, 1, 0, 719163, 1, 719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', '')]

    LOGN = [(184, '0', 719163, 0.0, 5.0, 1, 1, 5.0, 1, 0, 719163, 1, 719163.0,
             0.0, 0.0, 0, 0, 0, '0', '0', ''),
            (184, '0', 719163, 0.0, 10.0, 1, 1, 10.0, 1, 0, 719163, 1,
             719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', ''),
            (184, '0', 719163, 0.0, 15.0, 1, 1, 15.0, 1, 0, 719163, 1,
             719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', ''),
            (184, '0', 719163, 0.0, 20.0, 1, 1, 20.0, 1, 0, 719163, 1,
             719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', ''),
            (184, '0', 719163, 0.0, 25.0, 1, 1, 25.0, 1, 0, 719163, 1,
             719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', ''),
            (184, '0', 719163, 0.0, 30.0, 1, 1, 30.0, 1, 0, 719163, 1,
             719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', ''),
            (184, '0', 719163, 0.0, 35.0, 1, 1, 35.0, 1, 0, 719163, 1,
             719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', ''),
            (184, '0', 719163, 0.0, 40.0, 1, 1, 40.0, 1, 0, 719163, 1,
             719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', ''),
            (184, '0', 719163, 0.0, 50.0, 1, 1, 50.0, 1, 0, 719163, 1,
             719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', ''),
            (184, '0', 719163, 0.0, 60.0, 1, 1, 60.0, 1, 0, 719163, 1,
             719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', ''),
            (184, '0', 719163, 0.0, 70.0, 1, 1, 70.0, 1, 0, 719163, 1,
             719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', ''),
            (184, '0', 719163, 0.0, 80.0, 1, 1, 80.0, 1, 0, 719163, 1,
             719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', ''),
            (184, '0', 719163, 0.0, 90.0, 1, 1, 90.0, 1, 0, 719163, 1,
             719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', ''),
            (184, '0', 719163, 0.0, 100.0, 1, 1, 100.0, 1, 0, 719163, 1,
             719163.0, 0.0, 0.0, 0, 0, 0, '0', '0', '')]

    def setUp(self):
        """
        Setup the test fixture for the Survival class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test01_create(self):
        """
        (TestSurvival) __init__ should return an Survival model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.dicRecords, {})
        self.assertEqual(self.DUT.dicMTBF, {})
        self.assertEqual(self.DUT.dicHazard, {})
        self.assertEqual(self.DUT.dicReliability, {})
        np.testing.assert_array_equal(self.DUT.hazard, np.array([]))
        np.testing.assert_array_equal(self.DUT.km, np.array([]))
        np.testing.assert_array_equal(self.DUT.mcf, np.array([]))
        np.testing.assert_array_equal(self.DUT.nhpp, [])
        self.assertEqual(self.DUT.scale, [0.0, 0.0, 0.0])
        self.assertEqual(self.DUT.shape, [0.0, 0.0, 0.0])
        self.assertEqual(self.DUT.location, [0.0, 0.0, 0.0])
        self.assertEqual(self.DUT.variance, [0.0, 0.0, 0.0])
        self.assertEqual(self.DUT.covariance, [0.0, 0.0, 0.0])
        self.assertEqual(self.DUT.chi2_critical_value, [0.0, 0.0])
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
        self.assertEqual(self.DUT.chi_square, 0.0)
        self.assertEqual(self.DUT.cramer_vonmises, 0.0)
        self.assertEqual(self.DUT.cvm_critical_value, 0.0)
        self.assertEqual(self.DUT.grouped, 0)

    @attr(all=True, unit=True)
    def test02_set_attributes(self):
        """
        (TestSurvival) set_attributes should return a 0 error code on success
        """

        _values = (0, 1, 2, 'Description', 3, 4, 0.5, 6, 7, 8, 90.0, 10, 11,
                   12, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21, 22,
                   23, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0,
                   33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test02a_set_attributes_wrong_type(self):
        """
        (TestSurvival) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, 1, 2, 'Description', 3, 4, 0.5, 6, 7, 8, 90.0, 10, 11,
                   12, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21, 22,
                   23, 24.0, 25.0, 26.0, 27.0, 28.0, None, 30.0, 31.0, 32.0,
                   33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test02b_set_attributes_missing_index(self):
        """
        (TestSurvival) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 1, 2, 'Description', 3, 4, 0.5, 6, 7, 8, 90.0, 10, 11,
                   12, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21, 22,
                   24.0, 25.0, 26.0, 27.0, 28.0, 30.0, 31.0, 32.0, 33.0, 34.0,
                   35.0, 36.0, 37.0, 38.0, 39.0, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test03_get_attributes(self):
        """
        (TestSurvival) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (0, 0, 0, '', 0, 0, 0.75, 0, 0, 0, 100.0, 0, 0, 0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0,
                          0, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]))

    @attr(all=True, unit=True)
    def test04_sanity(self):
        """
        (TestSurvival) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 1, 2, 'Description', 4, 5, 60.0, 7, 8, 9, 10.0, 11,
                   12, 13, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21, 22,
                   23, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0,
                   33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0, 0)
        _results = (0, 1, 2, 'Description', 4, 5, 60.0, 7, 8, 9, 10.0, 11,
                    12, 13, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0,
                    37.0, 38.0, 39.0, 0, [14.0, 15.0, 16.0],
                    [17.0, 18.0, 19.0], [20.0, 21.0, 22.0], [23.0, 24.0, 25.0],
                    [26.0, 27.0, 28.0])

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _results)

    @attr(all=True, unit=True)
    def test05_calculate_tbf(self):
        """
        (TestSurvival) calculate_tbf should return False on success and set the current record interarrival time to a float value
        """

        _record = Record()
        _record.set_attributes((1, 'Sub-System 1', 735835, 56.7, 56.7, 1, 1,
                                56.7, 1, 0, 719163, 719163, 0.0, 0.0, 0.0, 0,
                                0, 0, 'None', 'None', 'None'))
        self.DUT.dicRecords[1] = _record
        _record = Record()
        _record.set_attributes((1, 'Sub-System 1', 735623, 198.4, 198.4, 1, 3,
                                0.0, 1, 0, 719163, 719163, 0.0, 0.0, 0.0, 0, 0,
                                0, 'None', 'None', 'None'))
        self.DUT.dicRecords[2] = _record
        self.DUT.dicRecords = OrderedDict(sorted(self.DUT.dicRecords.items(),
                                                 key=lambda r: r[1].right_interval))

        self.assertFalse(self.DUT.calculate_tbf(1, 2))
        self.assertAlmostEqual(self.DUT.dicRecords[2].interarrival_time, 141.7)

    @attr(all=True, unit=False)
    def test06_estimate_parameters_mcf(self):
        """
        (TestSurvival) estimate_parameters should return False on success when estimating the Mean Cumulative Function
        """

        pass

    @attr(all=True, unit=True)
    def test06a_estimate_parameters_km(self):
        """
        (TestSurvival) estimate_parameters should return False on success when estimating Kaplan-Meier parameters
        """

        self.DUT.distribution_id = 2
        self.DUT.start_time = 0.0
        self.DUT.rel_time = 500.0
        self.DUT.confidence = 0.75
        self.DUT.confidence_type = 3

        for _index, _data in enumerate(self.KAPLANMEIER):
            _record = Record()
            _record.set_attributes(_data)
            self.DUT.dicRecords[_index] = _record

        self.DUT.dicRecords = OrderedDict(sorted(self.DUT.dicRecords.items(),
                                                 key=lambda r: r[1].right_interval))

        self.assertFalse(self.DUT.estimate_parameters())
        self.assertEqual(self.DUT.n_failures, 17.0)
        self.assertEqual(self.DUT.n_suspensions, 0.0)
        self.assertAlmostEqual(self.DUT.scale[0], 273.9018359)
        self.assertAlmostEqual(self.DUT.scale[1], 299.7176471)
        self.assertAlmostEqual(self.DUT.scale[2], 325.5334582)

    @attr(all=True, unit=True)
    def test06b_estimate_parameters_nhpppl(self):
        """
        (TestSurvival) estimate_parameters should return False on success when estimating NHPP - Power Law parameters
        """

        self.DUT.distribution_id = 3
        self.DUT.start_time = 0.0
        self.DUT.rel_time = 500.0
        self.DUT.confidence = 0.75
        self.DUT.confidence_type = 3
        self.confidence_method = 3
        self.DUT.fit_method = 2

        for _index, _data in enumerate(self.NHPPPL):
            _record = Record()
            _record.set_attributes(_data)
            self.DUT.dicRecords[_index] = _record

        self.DUT.dicRecords = OrderedDict(sorted(self.DUT.dicRecords.items(),
                                                 key=lambda r: r[1].right_interval))

        self.assertFalse(self.DUT.estimate_parameters())
        self.assertEqual(self.DUT.n_failures, 11)
        self.assertEqual(self.DUT.n_suspensions, 0)
        self.assertAlmostEqual(self.DUT.scale[0], 0.007534060)
        self.assertAlmostEqual(self.DUT.scale[1], 0.007875004)
        self.assertAlmostEqual(self.DUT.scale[2], 0.008231378)

    @attr(all=True, unit=False)
    def test06c_estimate_parameters_nhppll(self):
        """
        (TestSurvival) estimate_parameters should return False on success when estimating NHPP - Log Linear parameters
        """

        self.DUT.distribution_id = 4
        self.DUT.start_time = 0.0
        self.DUT.rel_time = 500.0
        self.DUT.confidence = 0.75
        self.DUT.confidence_type = 3
        self.DUT.confidence_method = 3
        self.DUT.fit_method = 2

        for _index, _data in enumerate(self.NHPPPL):
            _record = Record()
            _record.set_attributes(_data)
            self.DUT.dicRecords[_index] = _record

        self.DUT.dicRecords = OrderedDict(sorted(self.DUT.dicRecords.items(),
                                                 key=lambda r: r[1].right_interval))

        self.assertFalse(self.DUT.estimate_parameters())
        self.assertEqual(self.DUT.n_failures, 11)
        self.assertEqual(self.DUT.n_suspensions, 0)
        self.assertAlmostEqual(self.DUT.scale[0], 0.007534060)
        self.assertAlmostEqual(self.DUT.scale[1], 0.007875004)
        self.assertAlmostEqual(self.DUT.scale[2], 0.008231378)

    @attr(all=True, unit=True)
    def test06d_estimate_parameters_exponential(self):
        """
        (TestSurvival) estimate_parameters should return False on success when estimating Exponential parameters
        """

        self.DUT.distribution_id = 5
        self.DUT.start_time = 0.0
        self.DUT.rel_time = 1000.0
        self.DUT.n_rel_points = 10
        self.DUT.confidence = 0.75
        self.DUT.confidence_type = 3
        self.DUT.confidence_method = 3
        self.DUT.fit_method = 2

        for _index, _data in enumerate(self.EXP):
            _record = Record()
            _record.set_attributes(_data)
            self.DUT.dicRecords[_index] = _record

        self.DUT.dicRecords = OrderedDict(sorted(self.DUT.dicRecords.items(),
                                                 key=lambda r: r[1].right_interval))

        self.assertFalse(self.DUT.estimate_parameters())
        self.assertEqual(self.DUT.n_failures, 5.0)
        self.assertEqual(self.DUT.n_suspensions, 0)
        self.assertAlmostEqual(self.DUT.scale[0], 0.01407715)
        self.assertAlmostEqual(self.DUT.scale[1], 0.01448397)
        self.assertAlmostEqual(self.DUT.scale[2], 0.01490256)

    @attr(all=True, unit=True)
    def test06e_estimate_parameters_lognormal(self):
        """
        (TestSurvival) estimate_parameters should return False on success when estimating LogNormal parameters
        """

        self.DUT.distribution_id = 6
        self.DUT.start_time = 0.0
        self.DUT.rel_time = 1000.0
        self.DUT.n_rel_points = 10
        self.DUT.confidence = 0.75
        self.DUT.confidence_type = 3
        self.DUT.confidence_method = 3
        self.DUT.fit_method = 2

        for _index, _data in enumerate(self.LOGN):
            _record = Record()
            _record.set_attributes(_data)
            self.DUT.dicRecords[_index] = _record

        self.DUT.dicRecords = OrderedDict(sorted(self.DUT.dicRecords.items(),
                                                 key=lambda r: r[1].right_interval))

        self.assertFalse(self.DUT.estimate_parameters())
        self.assertEqual(self.DUT.n_failures, 14.0)
        self.assertEqual(self.DUT.n_suspensions, 0)
        self.assertAlmostEqual(self.DUT.scale[0], 3.4706899)
        self.assertAlmostEqual(self.DUT.scale[1], 3.5158554)
        self.assertAlmostEqual(self.DUT.scale[2], 3.5616086)

    @attr(all=True, unit=True)
    def test06f_estimate_parameters_normal(self):
        """
        (TestSurvival) estimate_parameters should return False on success when estimating Normal parameters
        """

        self.DUT.distribution_id = 7
        self.DUT.start_time = 0.0
        self.DUT.rel_time = 1000.0
        self.DUT.n_rel_points = 10
        self.DUT.confidence = 0.75
        self.DUT.confidence_type = 3
        self.DUT.confidence_method = 3
        self.DUT.fit_method = 2

        for _index, _data in enumerate(self.LOGN):
            _record = Record()
            _record.set_attributes(_data)
            self.DUT.dicRecords[_index] = _record

        self.DUT.dicRecords = OrderedDict(sorted(self.DUT.dicRecords.items(),
                                                 key=lambda r: r[1].right_interval))

        self.assertFalse(self.DUT.estimate_parameters())
        self.assertEqual(self.DUT.n_failures, 14.0)
        self.assertEqual(self.DUT.n_suspensions, 0)
        self.assertAlmostEqual(self.DUT.scale[0], 44.9987914)
        self.assertAlmostEqual(self.DUT.scale[1], 45.0000000)
        self.assertAlmostEqual(self.DUT.scale[2], 45.0012087)

    @attr(all=True, unit=True)
    def test06g_estimate_parameters_weibull(self):
        """
        (TestSurvival) estimate_parameters should return False on success when estimating Weibull parameters
        """

        self.DUT.distribution_id = 8
        self.DUT.start_time = 0.0
        self.DUT.rel_time = 1000.0
        self.DUT.n_rel_points = 10
        self.DUT.confidence = 0.75
        self.DUT.confidence_type = 3
        self.DUT.confidence_method = 3
        self.DUT.fit_method = 2

        for _index, _data in enumerate(self.LOGN):
            _record = Record()
            _record.set_attributes(_data)
            self.DUT.dicRecords[_index] = _record

        self.DUT.dicRecords = OrderedDict(sorted(self.DUT.dicRecords.items(),
                                                 key=lambda r: r[1].right_interval))

        self.assertFalse(self.DUT.estimate_parameters())
        self.assertEqual(self.DUT.n_failures, 14.0)
        self.assertEqual(self.DUT.n_suspensions, 0)
        self.assertAlmostEqual(self.DUT.scale[0], 44.9987914)
        self.assertAlmostEqual(self.DUT.scale[1], 45.0000000)
        self.assertAlmostEqual(self.DUT.scale[2], 45.0012087)
        self.assertAlmostEqual(self.DUT.shape[0], 33.5790669)
        self.assertAlmostEqual(self.DUT.shape[1], 33.6440913)
        self.assertAlmostEqual(self.DUT.shape[2], 33.7092415)


class TestSurvivalController(unittest.TestCase):
    """
    Class for testing the Survival data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Survival class.
        """

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
