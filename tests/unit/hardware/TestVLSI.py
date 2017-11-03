#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestVLSI.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing VLSI IC module algorithms
and models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr
from hardware.component.integrated_circuit.VLSI import VLSI

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestVLSIModel(unittest.TestCase):
    """
    Class for testing the VLSI IC data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the VLSI IC class.
        """

        self.DUT = VLSI()

        self._base_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                             'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                             0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                             0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                             'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014)
        self._stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                               0.0, 1.0)
        self._rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                            0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                            0.0, 0)
        self._user_values = (0.0, 1.0, 2.0, 30.0, 440.0, 5, 6, 7.0, 8.0, 99.0, 10.0,
                             11, 12, 13.0, 14, 15.0, 16.0, 17.0, 18, 19.0, 0.0, 1.0,
                             2, 3, 440.0, 50, 60, 7.0, 80.0, 90, 'Zero', 'One',
                             'Two', 'Three', '4')
        self._comp_values = (0, 0, 0.0, 30.0, 0.0, 358.0)
        self._ic_values = (1.0, 0.05, 3.0, 4.0, 5.0, 1, "")

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestVLSI) __init__ should return an VLSI IC data model
        """

        self.assertTrue(isinstance(self.DUT, VLSI))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Integrated Circuit class was properly initialized.
        self.assertEqual(self.DUT.category, 1)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piQ, 1.0)

        # Verify the VLSI IC class was properly initialized.
        self.assertEqual(self.DUT.subcategory, 10)
        self.assertEqual(self.DUT.application, 0)
        self.assertEqual(self.DUT.package, 0)
        self.assertEqual(self.DUT.n_pins, 0)
        self.assertEqual(self.DUT.manufacturing, 0)
        self.assertEqual(self.DUT.years_production, 0.0)
        self.assertEqual(self.DUT.case_temperature, 0.0)
        self.assertEqual(self.DUT.feature_size, 0.0)
        self.assertEqual(self.DUT.esd_susceptibility, 1000.0)
        self.assertEqual(self.DUT.lambda_bd, 0.0)
        self.assertEqual(self.DUT.lambda_bp, 0.0)
        self.assertEqual(self.DUT.lambda_eos, 0.0)
        self.assertEqual(self.DUT.piMFG, 0.0)
        self.assertEqual(self.DUT.piCD, 0.0)
        self.assertEqual(self.DUT.piPT, 0.0)
        self.assertEqual(self.DUT.die_area, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestVLSI) set_attributes should return a 0 error code on success
        """

        _my_values = (1, 3, 24, 1, 1.5, 75.0, 0.0025, 0.0097, 1.2, 0.0038, 0.0, 0.0,
                      0.0, 0.0, 0.5)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._ic_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.application, 1)
        self.assertEqual(self.DUT.package, 3)
        self.assertEqual(self.DUT.n_pins, 24)
        self.assertEqual(self.DUT.manufacturing, 1)
        self.assertEqual(self.DUT.years_production, 1.5)
        self.assertEqual(self.DUT.case_temperature, 75.0)
        self.assertEqual(self.DUT.feature_size, 0.0025)
        self.assertEqual(self.DUT.esd_susceptibility, 0.0097)
        self.assertEqual(self.DUT.lambda_bd, 1.2)
        self.assertEqual(self.DUT.lambda_bp, 0.0038)
        self.assertEqual(self.DUT.lambda_eos, 0.0)
        self.assertEqual(self.DUT.piMFG, 0.0)
        self.assertEqual(self.DUT.piCD, 0.0)
        self.assertEqual(self.DUT.piPT, 0.0)
        self.assertEqual(self.DUT.die_area, 0.5)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestVLSI) set_attributes should return a 40 error code when too few items are passed
        """

        _my_values = (1, 3, 24, 1, 1.5, 75.0, 0.0025, 0.0097, 1.2, 0.0038, 0.0, 0.0,
                      0.0, 0.5)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._ic_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestVLSI) set_attributes should return a 10 error code when the wrong type is passed
        """

        _my_values = (1, 3, 24, 1, 1.5, 75.0, 0.0025, 0.0097, 1.2, 0.0038, 0.0, 0.0,
                      None, 0.0, 0.5)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._ic_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestVLSI) get_attributes should return a tuple of attribute values
        """

        _my_values = (0, 0, 0, 0, 0.0, 0.0, 0.0, 1000.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0)
        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0, '',
                   50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '', 1.0, 0, '',
                   0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                   0.0, 0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0], ['', '', '', '', ''], 0, 0, 0.0, 30.0, 0.0, 30.0,
                   0.0, 0.0, 1.0, 0.0, 0.0, 0, "") + _my_values

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestVLSI) get_attributes(set_attributes(values)) == values
        """

        _my_values = (0, 0, 0, 0, 0.0, 0.0, 0.0, 1000.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._ic_values + \
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
        self.assertEqual(_result[95:102], self._ic_values)

        self.assertEqual(_result[102:], _my_values)

    @attr(all=False, unit=False)
    def test_calculate_217_count(self):
        """
        (TestVLSI) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')

    @attr(all=True, unit=True)
    def test_calculate_217_count_all(self):
        """
        (TestVLSI) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.application = 1
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.16)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.0E-8)

        self.DUT.application = 2
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.24)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 6.0E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestVLSI) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.operating_power = 0.25
        self.DUT.thermal_resistance = 60.0

        self.DUT.application = 1
        self.DUT.package = 3
        self.DUT.manufacturing = 2
        self.DUT.n_elements = 16
        self.DUT.n_pins = 24
        self.DUT.years_production = 1.5
        self.DUT.case_temperature = 35.0
        self.DUT.esd_susceptibility = 250.0
        self.DUT.feature_size = 0.80
        self.DUT.die_area = 0.5

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.junction_temperature, 50.0)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambda_bd * piMFG * piT * piCD + lambda_bp * piE * piQ * piPT + lambda_eos')
        self.assertEqual(self.DUT.hazard_rate_model['lambda_bd'], 0.16)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambda_bp'],
                               0.0026128)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambda_eos'],
                               0.06191185)
        self.assertEqual(self.DUT.hazard_rate_model['piMFG'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 0.3148883)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piCD'], 9.8838095)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertEqual(self.DUT.hazard_rate_model['piPT'], 2.2)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.06646873E-6)
