#!/usr/bin/env python -O
"""
This is the test class for testing Aluminum capacitor module algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.hardware.TestAluminum.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
import configuration as _conf
from hardware.component.capacitor.electrolytic.Aluminum import Dry, Wet


class TestDryAluminumModel(unittest.TestCase):
    """
    Class for testing the Dry Aluminum capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Capacitor class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Dry()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestDryAluminum) __init__ should return a Dry Aluminum capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Dry))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Dry Aluminum capacitor class was properly initialized.
        self.assertEqual(self.DUT._piE, [1.0, 2.0, 12.0, 6.0, 17.0, 10.0, 12.0,
                                         28.0, 35.0, 27.0, 0.5, 14.0, 38.0,
                                         690.0])
        self.assertEqual(self.DUT._piQ, [3.0, 10.0])
        self.assertEqual(self.DUT._lambdab_count, [0.029, 0.081, 0.58, 0.24,
                                                   0.83, 0.73, 0.88, 4.3, 5.4,
                                                   2.0, 0.015, 0.68, 2.8,
                                                   28.0])
        self.assertEqual(self.DUT.subcategory, 54)
        self.assertEqual(self.DUT.reference_temperature, 358.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestDryAluminum) set_attributes should return a 0 error code on success
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
        (TestDryAluminum) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0, 0,
                   'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0, 'Remarks',
                   0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
                   0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, '', 0.0, 0.0,
                   0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, 0, 0, 0.0, 30.0, 0.0, 30.0,
                   0, 0.0, 0, 0, 0.0, 0.0, 0.0, '', 0.0, 0.0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestDryAluminum) set_attributes should return a 10 error code when the wrong type is passed
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0, 0,
                   'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0, 'Remarks',
                   0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
                   0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, '', 0.0, 0.0,
                   0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, 0, 0, 0.0, 30.0, 0.0, 30.0,
                   0, 0.0, 0, 0, 0.0, 0.0, None, '', 0.0, 0.0, 0.0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestDryAluminum) get_attributes should return a tuple of attribute values
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
        (TestDryAluminum) get_attributes(set_attributes(values)) == values
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
        (TestDryAluminum) calculate should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.hazard_rate_type = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 28.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 10.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 0.00028)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestDryAluminum) calculate should return False on success when calculating MIL-HDBK-217F stress results
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000033
        self.DUT.effective_resistance = 0.5
        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.05007399)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 10.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 690.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.03250293)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.1230105e-05)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestDryAluminum) calculate should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
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
        (TestDryAluminum) calculate should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000033
        self.DUT.effective_resistance = 0.5
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate())


class TestWetAluminumModel(unittest.TestCase):
    """
    Class for testing the Wet Aluminum capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Wet Aluminum capacitor class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Wet()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestWetAluminum) __init__ should return a Wet Aluminum capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Wet))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Wet Aluminum capacitor class was properly initialized.
        self.assertEqual(self.DUT._piE, [1.0, 2.0, 12.0, 6.0, 17.0, 10.0, 12.0,
                                         28.0, 35.0, 27.0, 0.5, 14.0, 38.0,
                                         690.0])
        self.assertEqual(self.DUT._piQ, [0.03, 0.1, 0.3, 1.0, 3.0, 10.0])
        self.assertEqual(self.DUT._lambdab_count, [0.024, 0.061, 0.42, 0.18,
                                                   0.59, 0.46, 0.55, 2.1, 2.6,
                                                   1.2, .012, 0.49, 1.7, 21.0])
        self.assertEqual(self.DUT.subcategory, 53)
        self.assertEqual(self.DUT.reference_temperature, 358.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestWetAluminum) set_attributes should return a 0 error code on success
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
        (TestWetAluminum) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0, 0,
                   'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0, 'Remarks',
                   0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
                   0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, '', 0.0, 0.0,
                   0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, 0, 0, 0.0, 30.0, 0.0, 30.0,
                   0, 0.0, 0, 0, 0.0, 0.0, 0.0, '', 0.0, 0.0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestWetAluminum) set_attributes should return a 10 error code when the wrong type is passed
        """

        _values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                   'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0, 0,
                   'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                   'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0, 'Remarks',
                   0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
                   0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, '', 0.0, 0.0,
                   0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, 0, 0, 0.0, 30.0, 0.0, 30.0,
                   0, 0.0, 0, 0, 0.0, None, 0.0, '', 0.0, 0.0, 0.0)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestWetAluminum) get_attributes should return a tuple of attribute values
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
        (TestWetAluminum) get_attributes(set_attributes(values)) == values
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
        (TestWetAluminum) calculate should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.hazard_rate_type = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 21.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 10.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 0.00021)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestWetAluminum) calculate should return False on success when calculating MIL-HDBK-217F stress results
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000033
        self.DUT.effective_resistance = 0.5

        self.assertFalse(self.DUT.calculate())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCV')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.10104114)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 10.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 690.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCV'], 0.03250293)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.26605180e-05)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestWetAluminum) calculate should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
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
        (TestWetAluminum) calculate should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000033
        self.DUT.effective_resistance = 0.5
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate())
