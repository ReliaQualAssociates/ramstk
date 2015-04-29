#!/usr/bin/env python -O
"""
This is the test class for testing BiPolar module algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.hardware.TestLFBipolar.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
import configuration as _conf
from hardware.component.semiconductor.transistor.Bipolar import *


class TestLFBipolarModel(unittest.TestCase):
    """
    Class for testing the Low Frequency Bipolar Transistor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the BiPolar class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = LFBipolar()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestLFBipolar) __init__ should return a Low Frequency Bipolar Transistor data model
        """

        self.assertTrue(isinstance(self.DUT, LFBipolar))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify the Semiconductor class was properly initialized.
        self.assertEqual(self.DUT.category, 2)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.q_override, 0.0)
        self.assertEqual(self.DUT.piQ, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piT, 0.0)

        # Verify the Low Frequency Bipolar Transistor class was properly
        # initialized.
        self.assertEqual(self.DUT._lst_piE, [1.0, 6.0, 9.0, 9.0, 19.0, 13.0,
                                             29.0, 20.0, 43.0, 24.0, 0.5, 14.0,
                                             32.0, 320.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.7, 1.0, 2.4, 5.5, 8.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [0.7, 1.0, 2.4, 5.5, 8.0])
        self.assertEqual(self.DUT._lambdab_count, [[0.00015, 0.0011, 0.0017,
                                                    0.0017, 0.0037, 0.0030,
                                                    0.0067, 0.0060, 0.013,
                                                    0.0056, 0.000073, 0.0027,
                                                    0.0074, 0.056],
                                                   [0.0057, 0.042, 0.069,
                                                    0.063, 0.15, 0.12, 0.26,
                                                    0.23, 0.50, 0.22, 0.0029,
                                                    0.11, 0.29, 1.1]])
        self.assertEqual(self.DUT.subcategory, 14)
        self.assertEqual(self.DUT.application, 0)
        self.assertEqual(self.DUT.piA, 0.0)
        self.assertEqual(self.DUT.piR, 0.0)
        self.assertEqual(self.DUT.piS, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestLFBipolar) set_attributes should return a 0 error code on success
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
                   1.0, 0.01, 2.0, 1.0, 1.0, 0.5, 0.8, 0.03, 2.3, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.application, 1)
        self.assertEqual(self.DUT.piA, 0.5)
        self.assertEqual(self.DUT.piR, 0.8)
        self.assertEqual(self.DUT.piS, 0.03)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestLFBipolar) set_attributes should return a 40 error code when too few items are passed
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
                   1.0, 0.01, 2.0, 1.0, 1.0, 0.5, 0.8, 0.03, 2.3, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestLFBipolar) set_attributes should return a 10 error code when the wrong type is passed
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
                   1.0, 1.0, 0.01, 2.0, 1.0, 1.0, None, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, '', 2)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestLFBipolar) get_attributes should return a tuple of attribute values
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
                   0, 0.0, 0.00074, 0.0, 0.0, 0.0, '', 0, 0.0, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestLFBipolar) get_attributes(set_attributes(values)) == values
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
                      1.0, 0.01, 2.0, 1.0, 1.0, 0.5, 0.8, 0.03, 2.3, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1)
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
                       3, 1.0, 0.01, 2.0, 1.0, 1.0, '', 1, 0.5, 0.8, 0.03)

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_high_power(self):
        """
        (TestLFBipolar) _overstressed should return False and overstress=False on success with operating power greater than rated in a harsh environment
        """

        self.DUT.operating_power = 18.0
        self.DUT.rated_power = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_high_voltage(self):
        """
        (TestLFBipolar) _overstressed should return False and overstress=False on success with operating voltage greater than rated in a harsh environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_voltage = 22.8
        self.DUT.rated_voltage = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_high_temperature(self):
        """
        (TestLFBipolar) _overstressed should return False and overstress=False on success with junction temperature greater than 125C in a harsh environment
        """

        self.DUT.junction_temperature = 135.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_high_power(self):
        """
        (TestLFBipolar) _overstressed should return False and overstress=False on success with operating power greater than rated in a mild environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_power = 23.0
        self.DUT.rated_power = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_high_voltage(self):
        """
        (TestLFBipolar) _overstressed should return False and overstress=False on success with operating voltage greater than rated in a mild environment
        """

        self.DUT.operating_voltage = 23.0
        self.DUT.rated_voltage = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_calculate_217_count_low_power(self):
        """
        (TestLFBipolar) calculate should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.rated_power = 0.075

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.0037)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.7)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.59E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_count_high_power(self):
        """
        (TestLFBipolar) calculate should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.rated_power = 0.75

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.15)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.7)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.05E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_power(self):
        """
        (TestLFBipolar) calculate should return False on success when calculating MIL-HDBK-217F stress results for a low power transistor
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.rated_power = 0.075
        self.DUT.operating_voltage = 17.0
        self.DUT.rated_voltage = 33.0
        self.DUT.junction_temperature = 32.0
        self.DUT.application = 1

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piA * piR * piS * piQ * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.00074)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 1.1768157)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piA'], 1.5)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piR'], 0.43)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piS'], 0.2222121)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.7)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 5.2422398E-10)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_power(self):
        """
        (TestLFBipolar) calculate should return False on success when calculating MIL-HDBK-217F stress results for a low power transistor
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.rated_power = 0.75
        self.DUT.operating_voltage = 17.0
        self.DUT.rated_voltage = 33.0
        self.DUT.junction_temperature = 32.0
        self.DUT.application = 1

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piA * piR * piS * piQ * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.00074)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 1.1768157)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piA'], 1.5)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piR'], 0.8990269)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piS'], 0.2222121)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.7)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.0960266E-09)


class TestHFLNBipolarModel(unittest.TestCase):
    """
    Class for testing the High Frequency Low Noise Bipolar Transistor data
    model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the BiPolar class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = HFLNBipolar()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestHFLNBipolar) __init__ should return a High Frequency Low Noise Bipolar Transistor data model
        """

        self.assertTrue(isinstance(self.DUT, HFLNBipolar))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify the Semiconductor class was properly initialized.
        self.assertEqual(self.DUT.category, 2)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.q_override, 0.0)
        self.assertEqual(self.DUT.piQ, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piT, 0.0)

        # Verify the High Frequency Low Noise Bipolar Transistor class was properly
        # initialized.
        self.assertEqual(self.DUT._lst_piE, [1.0, 2.0, 5.0, 4.0, 11.0, 4.0,
                                             5.0, 7.0, 12.0, 16.0, 0.5, 9.0,
                                             24.0, 250.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.7, 1.0, 2.4, 5.5, 8.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [0.5, 1.0, 2.0, 5.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.094, 0.23, 0.63, 0.46,
                                                       1.4, 0.60, 0.75, 1.3,
                                                       2.3, 2.4, 0.047, 1.1,
                                                       3.6, 28.0])
        self.assertEqual(self.DUT.subcategory, 17)
        self.assertEqual(self.DUT.base_hr, 0.18)
        self.assertEqual(self.DUT.piR, 0.0)
        self.assertEqual(self.DUT.piS, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestHFLNBipolar) set_attributes should return a 0 error code on success
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
                   1.0, 0.01, 2.0, 1.0, 1.0, 0.5, 0.8, 0.03, 2.3, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.piR, 0.5)
        self.assertEqual(self.DUT.piS, 0.8)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestHFLNBipolar) set_attributes should return a 40 error code when too few items are passed
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
                   1.0, 0.01, 2.0, 1.0, 1.0, 0.5)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestHFLNBipolar) set_attributes should return a 10 error code when the wrong type is passed
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
                   1.0, 1.0, 0.01, 2.0, 1.0, 1.0, None, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, '', 2)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestHFLNBipolar) get_attributes should return a tuple of attribute values
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
                   0, 0.0, 0.18, 0.0, 0.0, 0.0, '', 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestHFLNBipolar) get_attributes(set_attributes(values)) == values
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
                      1.0, 0.01, 2.0, 1.0, 1.0, 0.5, 0.8, 0.03, 2.3, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1)
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
                       3, 1.0, 0.01, 2.0, 1.0, 1.0, '', 0.5, 0.8)

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_high_power(self):
        """
        (TestHFLNBipolar) _overstressed should return False and overstress=False on success with operating power greater than rated in a harsh environment
        """

        self.DUT.operating_power = 18.0
        self.DUT.rated_power = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_high_voltage(self):
        """
        (TestHFLNBipolar) _overstressed should return False and overstress=False on success with operating voltage greater than rated in a harsh environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_voltage = 22.8
        self.DUT.rated_voltage = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_high_temperature(self):
        """
        (TestHFLNBipolar) _overstressed should return False and overstress=False on success with junction temperature greater than 125C in a harsh environment
        """

        self.DUT.junction_temperature = 135.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_high_power(self):
        """
        (TestHFLNBipolar) _overstressed should return False and overstress=False on success with operating power greater than rated in a mild environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_power = 23.0
        self.DUT.rated_power = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_high_voltage(self):
        """
        (TestHFLNBipolar) _overstressed should return False and overstress=False on success with operating voltage greater than rated in a mild environment
        """

        self.DUT.operating_voltage = 23.0
        self.DUT.rated_voltage = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestHFLNBipolar) calculate should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 1.4)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.7)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 9.8E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_power(self):
        """
        (TestHFLNBipolar) calculate should return False on success when calculating MIL-HDBK-217F stress results for a low power transistor
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.rated_power = 0.075
        self.DUT.operating_voltage = 17.0
        self.DUT.rated_voltage = 33.0
        self.DUT.junction_temperature = 32.0

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piR * piS * piQ * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.18)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 1.1768157)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piR'], 0.43)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piS'], 0.2222121)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.02403081E-08)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_power(self):
        """
        (TestHFLNBipolar) calculate should return False on success when calculating MIL-HDBK-217F stress results for a low power transistor
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.rated_power = 0.75
        self.DUT.operating_voltage = 17.0
        self.DUT.rated_voltage = 33.0
        self.DUT.junction_temperature = 32.0

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piR * piS * piQ * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.18)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 1.1768157)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piR'], 0.8990269)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piS'], 0.2222121)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.2317631E-08)


class TestHFHPBipolarModel(unittest.TestCase):
    """
    Class for testing the High Frequency High Power Bipolar Transistor data
    model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the BiPolar class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = HFHPBipolar()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestHFHPBipolar) __init__ should return a High Frequency High Power Bipolar Transistor data model
        """

        self.assertTrue(isinstance(self.DUT, HFHPBipolar))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify the Semiconductor class was properly initialized.
        self.assertEqual(self.DUT.category, 2)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.q_override, 0.0)
        self.assertEqual(self.DUT.piQ, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piT, 0.0)

        # Verify the High Frequency High Power Bipolar Transistor class was properly
        # initialized.
        self.assertEqual(self.DUT._lst_piE, [1.0, 2.0, 5.0, 4.0, 11.0, 4.0,
                                             5.0, 7.0, 12.0, 16.0, 0.5, 9.0,
                                             24.0, 250.0])
        self.assertEqual(self.DUT._lst_piQ_count, [0.7, 1.0, 2.4, 5.5, 8.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [0.5, 1.0, 2.0, 5.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [0.074, 0.15, 0.37, 0.29,
                                                       0.81, 0.29, 0.37, 0.52,
                                                       0.88, 0.037, 0.33, 0.66,
                                                       1.8, 18.0])
        self.assertEqual(self.DUT.subcategory, 18)
        self.assertEqual(self.DUT.construction, 0)
        self.assertEqual(self.DUT.application, 0)
        self.assertEqual(self.DUT.matching, 0)
        self.assertEqual(self.DUT.frequency, 0.0)
        self.assertEqual(self.DUT.piA, 0.0)
        self.assertEqual(self.DUT.piM, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestHFHPBipolar) set_attributes should return a 0 error code on success
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
                   1.0, 0.01, 2.0, 1.0, 1.0, 0.5, 0.8, 0.03, 2.3, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1, 2, 4)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.construction, 1)
        self.assertEqual(self.DUT.application, 2)
        self.assertEqual(self.DUT.matching, 4)
        self.assertEqual(self.DUT.frequency, 0.5)
        self.assertEqual(self.DUT.piA, 0.8)
        self.assertEqual(self.DUT.piM, 0.03)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestHFHPBipolar) set_attributes should return a 40 error code when too few items are passed
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
                   1.0, 0.01, 2.0, 1.0, 1.0, 0.5, 0.8, 0.03, 2.3, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestHFHPBipolar) set_attributes should return a 10 error code when the wrong type is passed
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
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, '', 2)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestHFHPBipolar) get_attributes should return a tuple of attribute values
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
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 0, 0, 0, 0.0, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestHFHPBipolar) get_attributes(set_attributes(values)) == values
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
                      1.0, 0.01, 2.0, 1.0, 1.0, 0.5, 0.8, 0.03, 2.3, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 1, 2, 3)
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
                       3, 1.0, 0.01, 2.0, 1.0, 1.0, '', 1, 2, 3, 0.5, 0.8,
                       0.03)

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_high_power(self):
        """
        (TestHFHPBipolar) _overstressed should return False and overstress=False on success with operating power greater than rated in a harsh environment
        """

        self.DUT.operating_power = 18.0
        self.DUT.rated_power = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_harsh_env_high_voltage(self):
        """
        (TestHFHPBipolar) _overstressed should return False and overstress=False on success with operating voltage greater than rated in a harsh environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_voltage = 22.8
        self.DUT.rated_voltage = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_high_temperature(self):
        """
        (TestHFHPBipolar) _overstressed should return False and overstress=False on success with junction temperature greater than 125C in a harsh environment
        """

        self.DUT.junction_temperature = 135.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_high_power(self):
        """
        (TestHFHPBipolar) _overstressed should return False and overstress=False on success with operating power greater than rated in a mild environment
        """

        self.DUT.environment_active = 1
        self.DUT.operating_power = 23.0
        self.DUT.rated_power = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_overstressed_mild_env_high_voltage(self):
        """
        (TestHFHPBipolar) _overstressed should return False and overstress=False on success with operating voltage greater than rated in a mild environment
        """

        self.DUT.operating_voltage = 23.0
        self.DUT.rated_voltage = 25.0
        self.assertFalse(self.DUT._overstressed())
        self.assertTrue(self.DUT.overstress)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestHFHPBipolar) calculate should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.81)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.7)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 5.67E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_continuous(self):
        """
        (TestHFHPBipolar) calculate should return False on success when calculating MIL-HDBK-217F stress results for a continuous duty transistor
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 5.0
        self.DUT.junction_temperature = 32.0
        self.DUT.construction = 1
        self.DUT.application = 1
        self.DUT.matching = 1
        self.DUT.frequency = 1.0

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piA * piM * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0468821)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 0.01763665)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piA'], 7.6)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piM'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.2840082E-09)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_pulsed(self):
        """
        (TestHFHPBipolar) calculate should return False on success when calculating MIL-HDBK-217F stress results for a pulsed transistor
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_power = 5.0
        self.DUT.junction_temperature = 32.0
        self.DUT.duty_cycle = 75.0
        self.DUT.construction = 2
        self.DUT.application = 2
        self.DUT.matching = 2
        self.DUT.frequency = 1.0

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piT * piA * piM * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0468821)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 0.01190504)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piA'], 4.9)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piM'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.5)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 5.4697061E-09)
