#!/usr/bin/env python -O
"""
This is the test class for testing Diode module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestDiode.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from hardware.component.semiconductor.Diode import HighFrequency, LowFrequency

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 - 2016 Andrew "weibullguy" Rowland'


class TestLowFrequencyDiodeModel(unittest.TestCase):
    """
    Class for testing the Low Frequency Diode data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Low Frequency Diode class.
        """

        self.DUT = LowFrequency()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestLowFrequencyDiode) __init__ should return a Low Frequency Diode data model
        """

        self.assertTrue(isinstance(self.DUT, LowFrequency))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify the Semiconductor class was properly initialized.
        self.assertEqual(self.DUT.category, 2)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.q_override, 0.0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piQ, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piT, 0.0)

        # Verify the Low Frequency Diode class was properly initialized.
        self.assertEqual(self.DUT._lst_piE, [1.0, 6.0, 9.0, 9.0, 19.0, 13.0,
                                             29.0, 20.0, 43.0, 24.0, 0.5, 14.0,
                                             32.0, 320.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.7, 1.0, 2.4, 5.5, 8.0])
        self.assertEqual(self.DUT._lambda_count, [[0.00360, 0.0280, 0.049,
                                                   0.043, 0.100, 0.092, 0.210,
                                                   0.200, 0.44, 0.170, 0.00180,
                                                   0.076, 0.23, 1.50],
                                                  [0.00094, 0.0075, 0.013,
                                                   0.011, 0.027, 0.024, 0.054,
                                                   0.054, 0.12, 0.045, 0.00047,
                                                   0.020, 0.06, 0.40],
                                                  [0.06500, 0.5200, 0.890,
                                                   0.780, 1.900, 1.700, 3.700,
                                                   3.700, 8.00, 3.100, 0.03200,
                                                   1.400, 4.10, 28.0],
                                                  [0.00280, 0.0220, 0.039,
                                                   0.034, 0.062, 0.073, 0.160,
                                                   0.160, 0.35, 0.130, 0.00140,
                                                   0.060, 0.18, 1.20],
                                                  [0.00290, 0.0230, 0.040,
                                                   0.035, 0.084, 0.075, 0.170,
                                                   0.170, 0.36, 0.140, 0.00150,
                                                   0.062, 0.18, 1.20],
                                                  [0.00330, 0.0240, 0.039,
                                                   0.035, 0.082, 0.066, 0.150,
                                                   0.130, 0.27, 0.120, 0.00160,
                                                   0.060, 0.16, 1.30],
                                                  [0.00560, 0.0400, 0.066,
                                                   0.060, 0.140, 0.110, 0.250,
                                                   0.220, 0.460, 0.21, 0.00280,
                                                   0.100, 0.28, 2.10]])
        self.assertEqual(self.DUT.subcategory, 12)
        self.assertEqual(self.DUT.application, 0)
        self.assertEqual(self.DUT.construction, 0)
        self.assertEqual(self.DUT.piS, 0.0)
        self.assertEqual(self.DUT.piC, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestLowFrequencyDiode) set_attributes should return a 0 error code on success
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
                   1.0, 0.01, 2.0, 1.0, 1.0, 0.5, 0.8, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 2, 4)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.application, 2)
        self.assertEqual(self.DUT.construction, 4)
        self.assertEqual(self.DUT.piS, 0.5)
        self.assertEqual(self.DUT.piC, 0.8)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestLowFrequencyDiode) set_attributes should return a 40 error code when too few items are passed
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
                   1.0, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestLowFrequencyDiode) set_attributes should return a 10 error code when the wrong type is passed
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
                   1.0, 1.0, 0.01, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, '', 4)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestLowFrequencyDiode) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0,
                   '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '',
                   1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1,
                   0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0,
                   0.0, 30.0, 0.0, 30.0,
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 0, 0, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestLowFrequencyDiode) get_attributes(set_attributes(values)) == values
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
                      1.0, 0.01, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 4, 5)
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
                       3, 1.0, 0.01, 2.0, 1.0, 1.0, '', 4, 5, 0.0, 0.0)

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_high_power(self):
        """
        (TestLowFrequencyDiode) _overstressed should return False and overstress=False on success with operating power greater than rated in a non-harsh environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_power = 0.23
        self.DUT.rated_power = 0.25
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_high_power(self):
        """
        (TestLowFrequencyDiode) _overstressed should return False and overstress=False on success with operating power greater than rated in a harsh environment
        """

        self.DUT.environment_active = 3
        self.DUT.operating_power = 0.178
        self.DUT.rated_power = 0.25
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_high_temperature(self):
        """
        (TestLowFrequencyDiode) _overstressed should return False and overstress=False on success with junction temperature greater than 125C in a harsh environment
        """

        self.DUT.environment_active = 3
        self.DUT.junction_temperature = 135.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestLowFrequencyDiode) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.application = 2
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.027)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.7)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.89E-08)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestLowFrequencyDiode) calculate_part should return False on success when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.junction_temperature = 38.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.rated_voltage = 3.3
        self.DUT.application = 2
        self.DUT.construction = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piS * piC * piQ * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'],
                         0.0010)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 1.5427653)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piS'], 0.09451537)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.7)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.1242314E-10)


class TestHighFrequencyDiodeModel(unittest.TestCase):
    """
    Class for testing the High Frequency Diode data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the High Frequency Diode class.
        """

        self.DUT = HighFrequency()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestHighFrequencyDiode) __init__ should return a High Frequency Diode data model
        """

        self.assertTrue(isinstance(self.DUT, HighFrequency))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify the Semiconductor class was properly initialized.
        self.assertEqual(self.DUT.category, 2)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.q_override, 0.0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piQ, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piT, 0.0)

        # Verify the High Frequency Diode class was properly initialized.
        self.assertEqual(self.DUT._lst_piA, [0.5, 2.5, 1.0])
        self.assertEqual(self.DUT._lst_piE, [1.0, 2.0, 5.0, 4.0, 11.0, 4.0,
                                             5.0, 7.0, 12.0, 16.0, 0.5, 9.0,
                                             24.0, 250.0])
        self.assertEqual(self.DUT._piQ_count, [[0.5, 1.0, 5.0, 25, 50],
                                               [0.5, 1.0, 1.8, 2.5]])
        self.assertEqual(self.DUT._lst_piQ_stress, [0.5, 1.0, 1.8, 2.5, 1.0])
        self.assertEqual(self.DUT._lambda_count, [[0.86, 2.80, 8.9, 5.6, 20.0,
                                                   11.0, 14.0, 36.0, 62.0,
                                                   44.0, 0.43, 16.0, 67.0,
                                                   350.0],
                                                  [0.31, 0.76, 2.1, 1.5, 4.60,
                                                   2.00, 2.50, 4.50, 7.60,
                                                   7.90, 0.16, 3.70, 12.0,
                                                   94.00],
                                                  [0.004, 0.0096, 0.0026,
                                                   0.0019, 0.058, 0.025, 0.032,
                                                   0.057, 0.097, 0.10, 0.002,
                                                   0.048, 0.15, 1.2],
                                                  [0.028, 0.068, 0.19, 0.14,
                                                   0.41, 0.18, 0.22, 0.40,
                                                   0.69, 0.71, 0.014, 0.34,
                                                   1.1, 8.5],
                                                  [0.047, 0.11, 0.31, 0.23,
                                                   0.68, 0.3, 0.37, 0.67, 1.1,
                                                   1.2, 0.023, 0.56, 1.8,
                                                   14.0],
                                                  [0.0043, 0.010, 0.029, 0.021,
                                                   0.063, 0.028, 0.034, 0.062,
                                                   0.11, 0.11, 0.0022, 0.052,
                                                   0.17, 1.3]])
        self.assertEqual(self.DUT.subcategory, 13)
        self.assertEqual(self.DUT.application, 0)
        self.assertEqual(self.DUT.type, 0)
        self.assertEqual(self.DUT.piA, 0.0)
        self.assertEqual(self.DUT.piR, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestHighFrequencyDiode) set_attributes should return a 0 error code on success
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
                   1.0, 0.01, 2.0, 1.0, 1.0, 0.5, 0.8, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 2, 4)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.application, 2)
        self.assertEqual(self.DUT.type, 4)
        self.assertEqual(self.DUT.piA, 0.5)
        self.assertEqual(self.DUT.piR, 0.8)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestHighFrequencyDiode) set_attributes should return a 40 error code when too few items are passed
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
                   1.0, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestHighFrequencyDiode) set_attributes should return a 10 error code when the wrong type is passed
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
                   1.0, 1.0, 0.01, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, '', 4)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestHighFrequencyDiode) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0,
                   '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '',
                   1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014,
                   1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0,
                   0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1,
                   0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0,
                   0, 0,
                   0.0, 30.0, 0.0, 30.0,
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 0, 0, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestHighFrequencyDiode) get_attributes(set_attributes(values)) == values
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
                      1.0, 0.01, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 4, 5)
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
                       3, 1.0, 0.01, 2.0, 1.0, 1.0, '', 4, 5, 0.0, 0.0)

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_high_power(self):
        """
        (TestHighFrequencyDiode) _overstressed should return False and overstress=False on success with operating power greater than rated in a non-harsh environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_power = 0.23
        self.DUT.rated_power = 0.25
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_high_power(self):
        """
        (TestHighFrequencyDiode) _overstressed should return False and overstress=False on success with operating power greater than rated in a harsh environment
        """

        self.DUT.environment_active = 3
        self.DUT.operating_power = 0.178
        self.DUT.rated_power = 0.25
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_high_temperature(self):
        """
        (TestHighFrequencyDiode) _overstressed should return False and overstress=False on success with junction temperature greater than 125C in a harsh environment
        """

        self.DUT.environment_active = 3
        self.DUT.junction_temperature = 135.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestHighFrequencyDiode) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.application = 2
        self.DUT.hazard_rate_type = 1
        self.DUT.type = 3

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 4.6)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.5)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.3E-06)

    @attr(all=True, unit=True)
    def test_calculate_217_count_schottky(self):
        """
        (TestHighFrequencyDiode) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results for a Schottky diode
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.application = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.type = 5

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.68)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.5)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.4E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestHighFrequencyDiode) calculate_part should return False on success when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.junction_temperature = 38.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.rated_voltage = 3.3
        self.DUT.application = 7
        self.DUT.type = 3

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piA * piR * piQ * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'],
                         0.0025)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 2.09137853)
        self.assertEqual(self.DUT.hazard_rate_model['piA'], 2.5)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.3071116E-08)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_impatt(self):
        """
        (TestHighFrequencyDiode) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for an IMPATT diode
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.junction_temperature = 38.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.rated_voltage = 3.3
        self.DUT.application = 7
        self.DUT.type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piA * piR * piQ * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'],
                         0.0025)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 1.3425466)
        self.assertEqual(self.DUT.hazard_rate_model['piA'], 2.5)
        self.assertEqual(self.DUT.hazard_rate_model['piR'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 8.3909163E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_pin(self):
        """
        (TestHighFrequencyDiode) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for a PIN diode
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.junction_temperature = 38.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.rated_voltage = 3.3
        self.DUT.rated_power = 15.0
        self.DUT.application = 4
        self.DUT.type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piA * piR * piQ * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'],
                         0.0081)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 1.3425466)
        self.assertEqual(self.DUT.hazard_rate_model['piA'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piR'], 0.6328244)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.8817296E-09)
