#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestVariable.py is part of The RTK Project
#
# All rights reserved.
"""
This is the test class for testing Variable capacitor module algorithms and models.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk",
)

import unittest
from nose.plugins.attrib import attr
from hardware.component.capacitor.variable.Variable import AirTrimmer, \
                                                           Ceramic, Piston, \
                                                           Vacuum

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestAirTrimmerModel(unittest.TestCase):
    """
    Class for testing the Variable Air Trimmer capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Variable Air Trimmer Capacitor class.
        """

        self.DUT = AirTrimmer()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestAirTrimmer) __init__ should return a Variable Air Trimmer capacitor model
        """

        self.assertTrue(isinstance(self.DUT, AirTrimmer))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Variable Air Trimmer capacitor class was properly initialized.
        self.assertEqual(self.DUT._piE, [
            1.0, 3.0, 13.0, 8.0, 24.0, 6.0, 10.0, 37.0, 70.0, 36.0, 0.5, 20.0,
            52.0, 950.0
        ])
        self.assertEqual(self.DUT._piQ, [5.0, 20.0])
        self.assertEqual(self.DUT._lambdab_count, [
            0.80, 0.33, 1.6, 0.87, 3.0, 1.0, 1.7, 9.9, 19.0, 8.1, 0.032, 2.5,
            8.9, 100.0
        ])
        self.assertEqual(self.DUT.subcategory, 57)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.spec_sheet, 0)
        self.assertEqual(self.DUT.reference_temperature, 358.0)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestAirTrimmer) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.specification = 2
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 5.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.5E-5)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestAirTrimmer) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 65C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 358.0
        self.DUT.quality = 1
        self.DUT.specification = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.045158336)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 5.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.77375033E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestAirTrimmer) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.00000001

        self.assertTrue(self.DUT.calculate_part())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestAirTrimmer) calculate_part should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate_part())


class TestVariableCeramicModel(unittest.TestCase):
    """
    Class for testing the Plastic capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Variable Ceramic Capacitor class.
        """

        self.DUT = Ceramic()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestVariableCeramic) __init__ should return a Variable Ceramic capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Ceramic))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Plastic capacitor class was properly initialized.
        self.assertEqual(self.DUT._piE, [
            1.0, 3.0, 13.0, 8.0, 24.0, 6.0, 10.0, 37.0, 70.0, 36.0, 0.4, 20.0,
            52.0, 950.0
        ])
        self.assertEqual(self.DUT._piQ, [4.0, 20.0])
        self.assertEqual(self.DUT._lambdab_count, [
            0.08, 0.27, 1.2, 0.71, 2.3, 0.69, 1.1, 6.2, 12.0, 4.1, 0.032, 1.9,
            5.9, 85.0
        ])
        self.assertEqual(self.DUT.subcategory, 55)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.spec_sheet, 0)
        self.assertEqual(self.DUT.reference_temperature, 358.0)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestVariableCeramic) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.specification = 2
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 2.3)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 4.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 9.2E-6)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp(self):
        """
        (TestVariableCeramic) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 85C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 358.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.036488651)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 4.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.37863811E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_temp(self):
        """
        (TestVariableCeramic) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 125C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 398.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0300614426)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 4.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.60737312E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestVariableCeramic) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.00000001

        self.assertTrue(self.DUT.calculate_part())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestVariableCeramic) calculate_part should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate_part())


class TestVariablePistonModel(unittest.TestCase):
    """
    Class for testing the Variable Piston capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Variable Piston Capacitor class.
        """

        self.DUT = Piston()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestVariablePiston) __init__ should return a Variable Piston capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Piston))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Super-Metallized Plastic capacitor class was properly
        # initialized.
        self.assertEqual(self.DUT._piE, [
            1.0, 3.0, 12.0, 7.0, 18.0, 3.0, 4.0, 20.0, 30.0, 32.0, 0.5, 18.0,
            46.0, 830.0
        ])
        self.assertEqual(self.DUT._piQ, [3.0, 10.0])
        self.assertEqual(self.DUT._lambdab_count, [
            0.033, 0.13, 0.62, 0.31, 0.93, 0.21, 0.28, 2.2, 3.3, 2.2, 0.16,
            0.93, 3.2, 37.0
        ])
        self.assertEqual(self.DUT.subcategory, 56)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.spec_sheet, 0)
        self.assertEqual(self.DUT.reference_temperature, 398.0)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestVariablePiston) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.specification = 2
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.93)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.79E-6)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp(self):
        """
        (TestVariablePiston) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 85C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 398.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0184334302)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.65900871E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_temp(self):
        """
        (TestVariablePiston) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the 125C specification
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 423.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0106945334)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 9.62508006E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestVariablePiston) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.00000001

        self.assertTrue(self.DUT.calculate_part())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestVariablePiston) calculate_part should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate_part())


class TestVariableVacuumModel(unittest.TestCase):
    """
    Class for testing the Variable Vacuum capacitor data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Variable Vacuum Capacitor class.
        """

        self.DUT = Vacuum()

        self._base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                             'Comp Ref Des', 0.0, 0.0, 0.0, 'Description',
                             100.0, 0, 0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0,
                             'Name', 'NSN', 0, 'Page #', 0, 0, 'Part #', 1,
                             'Ref Des', 1.0, 0, 'Remarks', 0.0, 'Spec #', 0,
                             30.0, 30.0, 0.0, 2014)
        self._stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0,
                               1.0, 0.0, 1.0)
        self._rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
                            1.0, 1.0, 0.0, 0.0, 0)
        self._user_values = (0.0, 1.0, 2.0, 30.0, 440.0, 5, 6, 7.0, 8.0, 99.0,
                             10.0, 11, 12, 13.0, 14, 15.0, 16.0, 17.0, 18,
                             19.0, 0.0, 1.0, 2, 3, 440.0, 50, 60, 7.0, 80.0,
                             90, 'Zero', 'One', 'Two', 'Three', '4')
        self._comp_values = (0, 0, 0.0, 0.0, 0.0, 0.0)
        self._capacitor_values = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0,
                                  "")

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestVariableVacuum) __init__ should return a Variable Vacuum capacitor model
        """

        self.assertTrue(isinstance(self.DUT, Vacuum))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Capacitor class was properly initialized.
        self.assertEqual(self.DUT.quality, 0)

        # Verify the Variable Vacuum capacitor class was properly initialized.
        self.assertEqual(self.DUT._piE, [
            1.0, 3.0, 14.0, 8.0, 27.0, 10.0, 18.0, 70.0, 108.0, 40.0, 0.5, 0.0,
            0.0, 0.0
        ])
        self.assertEqual(self.DUT._piQ, [3.0, 20.0])
        self.assertEqual(self.DUT._lambdab_count, [
            0.4, 1.3, 6.8, 3.6, 13.0, 5.7, 10.0, 58.0, 90.0, 23.0, 20.0, 0.0,
            0.0, 0.0
        ])
        self.assertEqual(self.DUT.configuration, 1)
        self.assertEqual(self.DUT.subcategory, 58)
        self.assertEqual(self.DUT.specification, 0)
        self.assertEqual(self.DUT.spec_sheet, 0)
        self.assertEqual(self.DUT.piCF, 0.0)
        self.assertEqual(self.DUT.reference_temperature, 358.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestVariableVacuum) set_attributes should return a 0 error code on success
        """

        _my_values = (0, 0.0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._capacitor_values + \
                  _my_values

        (_error_code, _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestVariableVacuum) set_attributes should return a 40 error code when too few items are passed
        """

        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._capacitor_values

        (_error_code, _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestVariableVacuum) set_attributes should return a 10 error code when the wrong type is passed
        """

        _my_values = (0, None)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._capacitor_values + \
                  _my_values

        (_error_code, _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestVariableVacuum) get_attributes should return a tuple of attribute values
        """

        _my_values = (1, 0.0)
        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0,
                   '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '',
                   1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0,
                   1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {},
                   0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0, [
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
                   ], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                       ], ['', '', '', '', ''], 0, 0, 0.0, 30.0, 0.0, 358.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, "") + _my_values

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestVariableVacuum) get_attributes(set_attributes(values)) == values
        """

        _my_values = (2, 0.0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._capacitor_values + \
                  _my_values

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()

        self.assertEqual(_result[:38], self._base_values)
        self.assertEqual(_result[38:50], self._stress_values)
        self.assertEqual(_result[50:86], self._rel_values)
        self.assertEqual(_result[86], list(self._user_values[:20]))
        self.assertEqual(_result[87], list(self._user_values[20:30]))
        self.assertEqual(_result[88], list(self._user_values[30:35]))
        self.assertEqual(_result[89:95], self._comp_values)
        self.assertEqual(_result[95:106], self._capacitor_values)

        self.assertEqual(_result[106:], _my_values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestVariableVacuum) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.configuration = 1
        self.DUT.quality = 1
        self.DUT.environment_active = 5
        self.DUT.specification = 2
        self.DUT.hazard_rate_type = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 13.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 3.9E-5)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_low_temp_fixed(self):
        """
        (TestVariableVacuum) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the fixed 85C specification
        """

        self.DUT.configuration = 1
        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 358.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCF')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.1824432545)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piCF'], 0.1)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.64198929E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_high_temp_fixed(self):
        """
        (TestVariableVacuum) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the fixed 125C specification
        """

        self.DUT.configuration = 1
        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 373.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCF')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.1650654943)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piCF'], 0.1)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.48558945E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_variable(self):
        """
        (TestVariableVacuum) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for the variable capacitor
        """

        self.DUT.configuration = 2
        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.reference_temperature = 398.0
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ * piE * piCF')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.1503072132)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piCF'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.35276492E-6)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_overflow(self):
        """
        (TestVariableVacuum) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.00000001

        self.assertTrue(self.DUT.calculate_part())

    @attr(all=True, unit=True)
    def test_calculate_217_stress_zero_division(self):
        """
        (TestVariableVacuum) calculate_part should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.0025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 2.7E-6
        self.DUT.reference_temperature = 0.0

        self.assertTrue(self.DUT.calculate_part())
