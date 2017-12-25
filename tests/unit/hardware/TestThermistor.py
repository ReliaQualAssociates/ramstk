#!/usr/bin/env python -O
"""
This is the test class for testing Thermistor module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestThermistor.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk",
)

import unittest
from nose.plugins.attrib import attr

from hardware.component.resistor.variable.Thermistor import *

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestThermistorModel(unittest.TestCase):
    """
    Class for testing the Thermistor resistor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Thermistor resistor class.
        """

        self.DUT = Thermistor()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestThermistor) __init__ should return a Thermistor resistor model
        """

        self.assertTrue(isinstance(self.DUT, Thermistor))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Resistor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Thermistor resistor class was properly initialized.
        self.assertEqual(self.DUT._lst_piE, [
            1.0, 5.0, 21.0, 11.0, 24.0, 11.0, 30.0, 16.0, 42.0, 37.0, 0.5,
            20.0, 53.0, 950.0
        ])
        self.assertEqual(self.DUT._lst_piQ_count,
                         [0.03, 0.1, 0.3, 1.0, 3.0, 10.0])
        self.assertEqual(self.DUT._lst_piQ_stress, [1.0, 15.0])
        self.assertEqual(self.DUT._lst_lambdab_count, [
            0.065, 0.32, 1.4, 0.71, 1.6, 0.71, 1.9, 1.0, 2.7, 2.4, 0.032, 1.3,
            3.4, 62.0
        ])
        self.assertEqual(self.DUT.subcategory, 32)
        self.assertEqual(self.DUT.type, 0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestThermistor) set_attributes should return a 0 error code on success
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0, 0,
                   'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0, 'Remarks',
                   0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014, 1.0, 155.0, -25.0,
                   1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0,
                   0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, '', 0.0,
                   0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, 0, 0, 1, 0.0, 0, 0,
                   0.0, 30.0, 0.0, 358.0, 1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 3, 1)

        (_error_code, _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.type, 1)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestThermistor) set_attributes should return a 40 error code with missing inputs
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0, 0,
                   'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0, 'Remarks',
                   0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014, 1.0, 155.0, -25.0,
                   1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0,
                   0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, '', 0.0,
                   0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, 0, 0, 1, 0.0, 0, 0,
                   0.0, 30.0, 0.0, 358.0, 1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1,
                   8.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 3)

        (_error_code, _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestThermistor) set_attributes should return a 10 error code with a wrong data type
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0, 0,
                   'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0, 'Remarks',
                   0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014, 1.0, 155.0, -25.0,
                   1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0,
                   0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, '', 0.0,
                   0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, 0, 0, 1, 0.0, 0, 0,
                   0.0, 30.0, 0.0, 358.0, 1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 0.1,
                   8.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 3, '')

        (_error_code, _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestThermistor) get_attributes should return a tuple of attribute values
        """

        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0,
                   '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '',
                   1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0,
                   1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {},
                   0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, 0, 0, 0.0, 30.0,
                   0.0, 30.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestThermistor) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 1.6)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.03)
        self.assertEqual(self.DUT.hazard_rate_active, 4.8E-08)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_bead(self):
        """
        (TestThermistor) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for a bead thermistor
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.021)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 5.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.05E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_disk(self):
        """
        (TestThermistor) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for a disk thermistor
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.type = 2

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.065)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 5.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.25E-07)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_rod(self):
        """
        (TestThermistor) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for a rod thermistor
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.type = 3

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.105)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 5.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 5.25E-07)
