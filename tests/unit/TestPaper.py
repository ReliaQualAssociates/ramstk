#!/usr/bin/env python -O
"""
This is the test class for testing Paper capacitor module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.hardware.TestPaper.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from hardware.component.capacitor.fixed.Paper import Bypass, Feedthrough, Metallized

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestPaperBypassModel(unittest.TestCase):
    """
    Class for testing the Fixed Paper Bypass capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Capacitor class.
        """

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)

        self.DUT = Bypass()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestPaperBypass) __init__ should return a Fixed Paper Bypass capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Bypass))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Fixed Paper Bypass capacitor class was properly
        # initialized.
        self.assertEqual(self.DUT._piE, [1.0, 2.0, 9.0, 5.0, 15.0, 6.0, 8.0,
                                         17.0, 32.0, 22.0, 0.5, 12.0, 32.0,
                                         670.0])
        self.assertEqual(self.DUT._piQ, [3.0, 7.0])
        self.assertEqual(self.DUT._lambdab_count, [[0.0036, 0.0072, 0.330,
                                                    0.016, 0.055, 0.023,
                                                    0.030, 0.07, 0.13, 0.083,
                                                    0.0018, 0.044, 0.12, 2.1],
                                                   [0.0039, 0.0087, 0.042,
                                                    0.022, 0.070, 0.035,
                                                    0.047, 0.19, 0.35, 0.130,
                                                    0.0020, 0.056, 0.19, 2.5]])
        self.assertEqual(self.DUT.subcategory, 40)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.spec_sheet, 0)
        self.assertEqual(self.DUT.reference_temperature, 358.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestPaperBypass) set_attributes should return a 0 error code on success
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   0.0, 0.05, 0.00000033, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   2, 3, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestPaperBypass) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   0.0, 0.05, 0.00000033, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   2, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestPaperBypass) set_attributes should return a 10 error code when the wrong type is passed
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   0.0, 0.05, 0.00000033, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   2, '', 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestPaperBypass) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0,
                   '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '',
                   1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0,
                   1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {},
                   0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, 0, 0, 0.0, 30.0,
                   0.0, 358.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, '')

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestPaperBypass) get_attributes(set_attributes(values)) == values
        """

        _in_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                      'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                      0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                      'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                      'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                      1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                      0.0, 1.0,
                      0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                      0, 0, 1, 0.0,
                      0, 0, 0.0, 30.0, 0.0, 358.0,
                      0.0, 0.05, 0.00000033, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      2, 3, 1)
        _out_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                       'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                       0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                       0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                       'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                       1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                       0.0, 1.0,
                       0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0,
                       0, 0, 0.0, 30.0, 0.0, 358.0,
                       0.0, 0.05, 0.00000033, 0.0, 0.0, 0.0, 0.0, 2, 3, 1, '')

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=True, unit=True)
    def test_calculate_217_count_low_temp(self):
        """
        (TestPaperBypass) calculate should return False on success when calculating MIL-HDBK-217F parts count results for the 85C specification
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.specification = 2
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.07)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.1E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_count_high_temp(self):
        """
        (TestPaperBypass) calculate should return False on success when calculating MIL-HDBK-217F parts count results for the 125C specification
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.specification = 1
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.055)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.65E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp(self):
        """
        (TestPaperBypass) calculate should return False on success when calculating MIL-HDBK-217F stress results for the 85C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 358.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.001722632)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.318744932)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.36302712E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_temp(self):
        """
        (TestPaperBypass) calculate should return False on success when calculating MIL-HDBK-217F stress results for the 125C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 398.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.001549814)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.318744932)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.22628566E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestPaperBypass) calculate should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.00000001

        self.assertTrue(self.DUT.calculate())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestPaperBypass) calculate should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate())


class TestPaperFeedthroughModel(unittest.TestCase):
    """
    Class for testing the Paper, Feedthrough capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Paper, Feedthrough capacitor class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Feedthrough()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestPaperFeedthrough) __init__ should return a Fixed Paper Feedthrough capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Feedthrough))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Fixed Paper Feedthrough capacitor class was properly initialized.
        self.assertEqual(self.DUT._piE, [1.0, 2.0, 9.0, 7.0, 15.0, 6.0, 8.0,
                                         17.0, 28.0, 22.0, 0.5, 12.0, 32.0,
                                         570.0])
        self.assertEqual(self.DUT._piQ, [1.0, 3.0, 10.0])
        self.assertEqual(self.DUT._lambdab_count, [0.0047, 0.0096, 0.044,
                                                   0.034, 0.073, 0.030, 0.040,
                                                   0.094, 0.15, 0.11, 0.0024,
                                                   0.058, 0.18, 2.7])
        self.assertEqual(self.DUT.subcategory, 41)
        self.assertEqual(self.DUT.reference_temperature, 358.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestPaperFeedthrough) set_attributes should return a 0 error code on success
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   0.0, 0.05, 0.00000033, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   2, 3, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestPaperFeedthrough) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   0.0, 0.05, 0.00000033, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   3, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestPaperFeedthrough) set_attributes should return a 10 error code when the wrong type is passed
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   0.0, 0.05, 0.00000033, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   2, '', 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestPaperFeedthrough) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0,
                   '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '',
                   1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0,
                   1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {},
                   0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, 0, 0, 0.0, 30.0,
                   0.0, 358.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, '')

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestPaperFeedthrough) get_attributes(set_attributes(values)) == values
        """

        _in_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                      'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                      0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                      'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                      'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                      1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                      0.0, 1.0,
                      0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                      0, 0, 1, 0.0,
                      0, 0, 0.0, 30.0, 0.0, 358.0,
                      0.0, 0.05, 0.00000033, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      2, 3, 1)
        _out_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                       'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                       0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                       0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                       'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                       1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                       0.0, 1.0,
                       0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0,
                       0, 0, 0.0, 30.0, 0.0, 358.0,
                       0.0, 0.05, 0.00000033, 0.0, 0.0, 0.0, 0.0, 2, 3, 1, '')

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestPaperFeedthrough) calculate should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.073)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 7.3E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp(self):
        """
        (TestPaperFeedthrough) calculate should return False on success when calculating MIL-HDBK-217F stress results for 85C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.max_rated_temperature = 85.0

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.002303519)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 10.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.577217864)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 7.26630319E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_mid_temp(self):
        """
        (TestPaperFeedthrough) calculate should return False on success when calculating MIL-HDBK-217F stress results for 125C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 398.0

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.002072426)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 10.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.577217864)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.53733391E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_temp(self):
        """
        (TestPaperFeedthrough) calculate should return False on success when calculating MIL-HDBK-217F stress results for 150C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 423.0

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.002047116)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 10.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.577217864)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.45749580E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestPaperFeedthrough) calculate should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000033
        self.DUT.effective_resistance = 0.5
        self.DUT.reference_temperature = 0.00000001

        self.assertTrue(self.DUT.calculate())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestPaperFeedthrough) calculate should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000033
        self.DUT.effective_resistance = 0.5
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate())


class TestPaperMetallizedModel(unittest.TestCase):
    """
    Class for testing the Fixed Metallized Paper capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Capacitor class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Metallized()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestPaperMetallized) __init__ should return a Fixed Metallized Paper capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Metallized))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Fixed Paper Bypass capacitor class was properly
        # initialized.
        self.assertEqual(self.DUT._piE, [1.0, 2.0, 8.0, 5.0, 14.0, 4.0, 6.0,
                                         11.0, 20.0, 20.0, 0.5, 11.0, 29.0,
                                         530.0])
        self.assertEqual(self.DUT._piQ, [0.03, 0.1, 0.3, 1.0, 3.0, 7.0, 20.0])
        self.assertEqual(self.DUT._lambdab_count, [0.0029, 0.0058, 0.023,
                                                   0.014, 0.041, 0.012, 0.018,
                                                   0.037, 0.066, 0.060, 0.0014,
                                                   0.032, 0.088, 1.5])
        self.assertEqual(self.DUT.subcategory, 43)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.spec_sheet, 0)
        self.assertEqual(self.DUT.reference_temperature, 358.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestPaperMetallized) set_attributes should return a 0 error code on success
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   0.0, 0.05, 0.00000033, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   2, 3, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestPaperMetallized) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   0.0, 0.05, 0.00000033, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   2, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestPaperMetallized) set_attributes should return a 10 error code when the wrong type is passed
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                   0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                   'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                   0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0, 1, 0.0,
                   0, 0, 0.0, 30.0, 0.0, 358.0,
                   0.0, 0.05, 0.00000033, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   2, '', 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestPaperMetallized) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0,
                   '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '',
                   1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0,
                   1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {},
                   0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, 0, 0, 0.0, 30.0,
                   0.0, 358.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, '')

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestPaperMetallized) get_attributes(set_attributes(values)) == values
        """

        _in_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                      'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                      0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                      'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                      'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                      1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                      0.0, 1.0,
                      0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                      0, 0, 1, 0.0,
                      0, 0, 0.0, 30.0, 0.0, 358.0,
                      0.0, 0.05, 0.00000033, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      2, 3, 1)
        _out_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                       'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                       0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                       0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                       'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                       1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                       0.0, 1.0,
                       0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0,
                       0, 0, 0.0, 30.0, 0.0, 358.0,
                       0.0, 0.05, 0.00000033, 0.0, 0.0, 0.0, 0.0, 2, 3, 1, '')

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestPaperMetallized) calculate should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.specification = 2
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.041)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.23E-9)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp(self):
        """
        (TestPaperMetallized) calculate should return False on success when calculating MIL-HDBK-217F stress results for the 85C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 358.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.001382112)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.314821244)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.09033774E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_temp(self):
        """
        (TestPaperMetallized) calculate should return False on success when calculating MIL-HDBK-217F stress results for the 125C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 398.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.001243455)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 1.314821244)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 9.8095299E-11)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestPaperMetallized) calculate should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.00000001

        self.assertTrue(self.DUT.calculate())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestPaperMetallized) calculate should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate())
