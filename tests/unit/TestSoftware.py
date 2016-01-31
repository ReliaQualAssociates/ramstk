#!/usr/bin/env python -O
"""
This is the test class for testing Software module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.software.TestSoftware.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

from software.Software import Model, _calculate_application_risk, _calculate_development_risk, _calculate_anomaly_risk, _calculate_traceability_risk, _calculate_quality_risk, _calculate_language_type_risk, _calculate_risk_reduction, _calculate_reliability_estimation_number

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestSoftwareModel(unittest.TestCase):
    """
    Class for testing the Software data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Software class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestSoftware) __init__ should return a Software model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.software_id, None)
        self.assertEqual(self.DUT.level_id, 0)
        self.assertEqual(self.DUT.description, "")
        self.assertEqual(self.DUT.application_id, 0)
        self.assertEqual(self.DUT.development_id, 0)
        self.assertEqual(self.DUT.a_risk, 0.0)
        self.assertEqual(self.DUT.do, 0.0)
        self.assertEqual(self.DUT.dd, 0)
        self.assertEqual(self.DUT.dc, 0.0)
        self.assertEqual(self.DUT.d_risk, 0.0)
        self.assertEqual(self.DUT.am, 0.0)
        self.assertEqual(self.DUT.sa, 0.0)
        self.assertEqual(self.DUT.st, 0.0)
        self.assertEqual(self.DUT.dr, 0.0)
        self.assertEqual(self.DUT.sq, 0.0)
        self.assertEqual(self.DUT.s1, 0.0)
        self.assertEqual(self.DUT.hloc, 0)
        self.assertEqual(self.DUT.aloc, 0)
        self.assertEqual(self.DUT.sloc, 0)
        self.assertEqual(self.DUT.sl, 0.0)
        self.assertEqual(self.DUT.ax, 0)
        self.assertEqual(self.DUT.bx, 0)
        self.assertEqual(self.DUT.cx, 0)
        self.assertEqual(self.DUT.nm, 0)
        self.assertEqual(self.DUT.sx, 0.0)
        self.assertEqual(self.DUT.um, 0)
        self.assertEqual(self.DUT.wm, 0)
        self.assertEqual(self.DUT.xm, 0)
        self.assertEqual(self.DUT.sm, 1.0)
        self.assertEqual(self.DUT.df, 0.0)
        self.assertEqual(self.DUT.sr, 0.0)
        self.assertEqual(self.DUT.s2, 0.0)
        self.assertEqual(self.DUT.rpfom, 0.0)
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.dev_assess_type, 0)
        self.assertEqual(self.DUT.phase_id, 0)
        self.assertEqual(self.DUT.tcl, 0)
        self.assertEqual(self.DUT.test_path, 0)
        self.assertEqual(self.DUT.category, 0)
        self.assertEqual(self.DUT.test_effort, 0)
        self.assertEqual(self.DUT.test_approach, 0)
        self.assertEqual(self.DUT.labor_hours_test, 0.0)
        self.assertEqual(self.DUT.labor_hours_dev, 0.0)
        self.assertEqual(self.DUT.budget_test, 0.0)
        self.assertEqual(self.DUT.budget_dev, 0.0)
        self.assertEqual(self.DUT.schedule_test, 0.0)
        self.assertEqual(self.DUT.schedule_dev, 0.0)
        self.assertEqual(self.DUT.branches, 0)
        self.assertEqual(self.DUT.branches_test, 0)
        self.assertEqual(self.DUT.inputs, 0)
        self.assertEqual(self.DUT.inputs_test, 0)
        self.assertEqual(self.DUT.nm_test, 0)
        self.assertEqual(self.DUT.interfaces, 0)
        self.assertEqual(self.DUT.interfaces_test, 0)
        self.assertEqual(self.DUT.te, 0.0)
        self.assertEqual(self.DUT.tm, 0.0)
        self.assertEqual(self.DUT.tc, 0.0)
        self.assertEqual(self.DUT.t_risk, 0.0)
        self.assertEqual(self.DUT.ft1, 0.0)
        self.assertEqual(self.DUT.ft2, 0.0)
        self.assertEqual(self.DUT.ren_avg, 0.0)
        self.assertEqual(self.DUT.ren_eot, 0.0)
        self.assertEqual(self.DUT.ec, 0.0)
        self.assertEqual(self.DUT.ev, 0.0)
        self.assertEqual(self.DUT.et, 0.0)
        self.assertEqual(self.DUT.os, 0.0)
        self.assertEqual(self.DUT.ew, 0.0)
        self.assertEqual(self.DUT.e_risk, 0.0)
        self.assertEqual(self.DUT.failure_rate, 0.0)
        self.assertEqual(self.DUT.cb, 0)
        self.assertEqual(self.DUT.ncb, 0)
        self.assertEqual(self.DUT.dr_test, 0)
        self.assertEqual(self.DUT.test_time, 0.0)
        self.assertEqual(self.DUT.dr_eot, 0)
        self.assertEqual(self.DUT.test_time_eot, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestSoftware) set_attributes should return a 0 error code on success
        """

        _values = (0, 32, 0, "Description", 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0.0, 0,
                   0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0, 0, 0, 0, 0, 0, 0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0, 0, 0, 0, 0, 0.0, 0, 0.0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestSoftware) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, 32, 0, "Description", 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0.0, 0,
                   0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 21, 0, 0, 0, 0, 0, 0, 0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0,
                   0.0, None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0, 0, 0, 0, 0, 0.0, 0, 0.0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestSoftware) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 32, 0, "Description", 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0.0, 0,
                   0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 44, 0, 0, 0, 0, 0, 0,
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0, 0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestSoftware) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, 0, "", 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0.0, 0, 0, 0,
                   1.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0,
                   0, 0, 0.0, 0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestSoftware) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 32, 0, "Description", 0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0.0, 0, 0, 0, 0, 0.0, 0,
                   0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 21, 0, 0, 0, 0, 0, 0, 0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0, 0, 0, 0.0, 0, 0.0)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)

    @attr(all=True, unit=True)
    def test_calculate_application_risk(self):
        """
        (TestSoftware) _calculate_application_risk should return False on success
        """

        self.DUT.application_id = 1

        self.assertFalse(_calculate_application_risk(self.DUT))
        self.assertEqual(self.DUT.a_risk, 1.0)

        self.DUT.application_id = 4
        _calculate_application_risk(self.DUT)
        self.assertEqual(self.DUT.a_risk, 2.0)

        self.DUT.application_id = 5
        _calculate_application_risk(self.DUT)
        self.assertEqual(self.DUT.a_risk, 3.0)

    @attr(all=True, unit=True)
    def test_calculate_development_risk(self):
        """
        (TestSoftware) _calculate_development_risk should return False on success
        """

        self.DUT.lst_development = [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                    1]
        self.assertFalse(_calculate_development_risk(self.DUT))
        self.assertEqual(self.DUT.d_risk, 0.5)

        self.DUT.lst_development = [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1,
                                    0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                                    1]
        _calculate_development_risk(self.DUT)
        self.assertEqual(self.DUT.d_risk, 2.0)

        self.DUT.lst_development = [1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                                    0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                    0]
        _calculate_development_risk(self.DUT)
        self.assertEqual(self.DUT.d_risk, 1.0)

    @attr(all=True, unit=True)
    def test_calculate_anomaly_risk(self):
        """
        (TestSoftware) _calculate_anomaly_risk should return False on success
        """

        self.DUT.phase_id = 2               # Requirements review
        self.DUT.lst_anomaly_mgmt = [[5, 5, 10, 10, 1, 3, 3, 1, 1, 0, 1, 1, 0,
                                      1, 1, 1, 0, 1, 0]]

        self.assertFalse(_calculate_anomaly_risk(self.DUT))
        self.assertAlmostEqual(self.DUT.am, 0.3684211)
        self.assertEqual(self.DUT.sa, 0.9)

        self.DUT.phase_id = 3               # PDR
        self.DUT.lst_anomaly_mgmt = [[],
                                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1,
                                     1, 1, 0, 1, 0]]

        self.assertFalse(_calculate_anomaly_risk(self.DUT))
        self.assertAlmostEqual(self.DUT.am, 0.1428571)
        self.assertEqual(self.DUT.sa, 0.9)

    @attr(all=True, unit=True)
    def test_calculate_traceability_risk(self):
        """
        (TestSoftware) _calculate_traceability_risk should return False on success
        """

        self.DUT.phase_id = 2
        self.DUT.lst_traceability = [[1, 0]]

        self.assertFalse(_calculate_traceability_risk(self.DUT))
        self.assertAlmostEqual(self.DUT.st, 1.0)

        self.DUT.phase_id = 3
        self.DUT.lst_traceability = [[], [0, 0]]

        self.assertFalse(_calculate_traceability_risk(self.DUT))
        self.assertAlmostEqual(self.DUT.st, 1.1)

        self.DUT.phase_id = 4
        self.DUT.lst_traceability = [[], [], [1, 1]]

        self.assertFalse(_calculate_traceability_risk(self.DUT))
        self.assertAlmostEqual(self.DUT.st, 1.0)

    @attr(all=True, unit=True)
    def test_calculate_quality_risk(self):
        """
        (TestSoftware) _calculate_quality_risk should return False on success
        """

        self.DUT.phase_id = 2
        self.DUT.lst_sftw_quality = [[1, 1, 1, 1, 1, 1, 0, 1, 5, 4, 4, 4, 1, 1,
                                      1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        self.assertFalse(_calculate_quality_risk(self.DUT))
        self.assertAlmostEqual(self.DUT.dr, 0.12)
        self.assertAlmostEqual(self.DUT.sq, 1.1)

        self.DUT.phase_id = 3
        self.DUT.lst_sftw_quality = [[],
                                     [1, 1, 125.0, 15.0, 1, 1, 5, 4, 4, 4, 4,
                                      3, 1, 0, 10, 8, 1, 1, 1, 1, 0, 1, 1, 1,
                                      0, 0, 0]]

        self.assertFalse(_calculate_quality_risk(self.DUT))
        self.assertAlmostEqual(self.DUT.dr, 0.2631579)
        self.assertAlmostEqual(self.DUT.sq, 1.1)

    @attr(all=True, unit=True)
    def test_calculate_language_type_risk(self):
        """
        (TestSoftware) _calculate_language_type_risk should return False on success
        """

        self.DUT.sloc = 150
        self.DUT.aloc = 15

        self.assertFalse(_calculate_language_type_risk(self.DUT))
        self.assertEqual(self.DUT.hloc, 135)
        self.assertAlmostEqual(self.DUT.sl, 0.14)

    @attr(all=True, unit=True)
    def test_calculate_risk_reduction_labor(self):
        """
        (TestSoftware) calculate_risk_reduction should return False on success when using labor hours
        """

        self.DUT.level_id = 2

        self.DUT.test_effort = 1
        self.DUT.labor_hours_test = 15
        self.DUT.labor_hours_dev = 150
        self.DUT.nm_test = 4
        self.DUT.nm = 5
        self.DUT.interfaces_test = 10
        self.DUT.interfaces = 12
        self.DUT.tu = 3
        self.DUT.tt = 5

        self.assertFalse(_calculate_risk_reduction(self.DUT))
        self.assertEqual(self.DUT.te, 1.0)
        self.assertAlmostEqual(self.DUT.tm, 1.0)
        self.assertAlmostEqual(self.DUT.tc, 1.2244898)
        self.assertAlmostEqual(self.DUT.t_risk, 1.2244898)

    @attr(all=True, unit=True)
    def test_calculate_risk_reduction_budget(self):
        """
        (TestSoftware) calculate_risk_reduction should return False on success when using budget
        """

        self.DUT.level_id = 3

        self.DUT.test_effort = 2
        self.DUT.budget_test = 15286.00
        self.DUT.budget_dev = 150894.00
        self.DUT.branches_test = 61
        self.DUT.branches = 85
        self.DUT.inputs_test = 10
        self.DUT.inputs = 12
        self.DUT.tu = 3
        self.DUT.tt = 5

        self.assertFalse(_calculate_risk_reduction(self.DUT))
        self.assertAlmostEqual(self.DUT.te, 1.0)
        self.assertAlmostEqual(self.DUT.tm, 1.0)
        self.assertAlmostEqual(self.DUT.tc, 1.2895070)
        self.assertAlmostEqual(self.DUT.t_risk, 1.2895070)

    @attr(all=True, unit=True)
    def test_calculate_risk_reduction_schedule(self):
        """
        (TestSoftware) calculate_risk_reduction should return False on success when using schedule
        """

        self.DUT.level_id = 3

        self.DUT.test_effort = 3
        self.DUT.schedule_test = 15
        self.DUT.schedule_dev = 186
        self.DUT.branches_test = 61
        self.DUT.branches = 85
        self.DUT.inputs_test = 10
        self.DUT.inputs = 12
        self.DUT.tu = 3
        self.DUT.tt = 5

        self.assertFalse(_calculate_risk_reduction(self.DUT))
        self.assertAlmostEqual(self.DUT.te, 1.0)
        self.assertAlmostEqual(self.DUT.tm, 1.0)
        self.assertAlmostEqual(self.DUT.tc, 1.2895070)
        self.assertAlmostEqual(self.DUT.t_risk, 1.2895070)

    @attr(all=True, unit=True)
    def test_calculate_reliability_estimation_number(self):
        """
        (TestSoftware) calculate_reliability_estimation_number should return False on success
        """

        self.DUT.level_id = 3

        self.DUT.et = 32
        self.DUT.os = 15
        self.DUT.ec = 18
        self.DUT.dr_test = 61
        self.DUT.test_time = 6.2
        self.DUT.dr_eot = 7
        self.DUT.test_time_eot = 1.3
        self.DUT.t_risk = 7.035549936788876

        self.assertFalse(_calculate_reliability_estimation_number(self.DUT))
        self.assertAlmostEqual(self.DUT.ew, 1.8823529)
        self.assertAlmostEqual(self.DUT.ev, 81.1)
        self.assertAlmostEqual(self.DUT.ft1, 9.8387097)
        self.assertAlmostEqual(self.DUT.ft2, 5.3846154)
        self.assertAlmostEqual(self.DUT.ren_avg, 1.3844147)
        self.assertAlmostEqual(self.DUT.ren_eot, 5.3037223)
        self.assertAlmostEqual(self.DUT.e_risk, 152.65882352941176)

    @attr(all=True, unit=False)
    def test_calculate(self):
        """
        (TestSoftware) calculate should return False on success
        """

        self.DUT.lst_development = [1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                                    0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                    0]
        self.DUT.lst_anomaly_mgmt = [[],
                                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1,
                                      1, 1, 0, 1, 0]]
        self.DUT.lst_traceability = [[], [0, 0]]
        self.DUT.lst_sftw_quality = [[],
                                     [1, 1, 125.0, 15.0, 1, 1, 5, 4, 4, 4, 4,
                                      3, 1, 0, 10, 8, 1, 1, 1, 1, 0, 1, 1, 1,
                                      0, 0, 0]]

        self.DUT.application_id = 4
        self.DUT.phase_id = 3               # PDR

        self.assertFalse(self.DUT.calculate(self.DUT))
        self.assertEqual(self.DUT.a_risk, 2.0)
        self.assertEqual(self.DUT.d_risk, 1.0)
        self.assertAlmostEqual(self.DUT.am, 0.1428571)
        self.assertEqual(self.DUT.sa, 0.9)
        self.assertEqual(self.DUT.st, 1.1)
        self.assertAlmostEqual(self.DUT.dr, 0.2631579)
        self.assertAlmostEqual(self.DUT.sq, 1.1)
        self.assertAlmostEqual(self.DUT.s1, 1.089)
        self.assertAlmostEqual(self.DUT.rpfom, 2.178)
