#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestMemory.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing Memory IC module algorithms and models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from hardware.component.integrated_circuit.Memory import Memory, DRAM, \
                                                         EEPROM, ROM, SRAM

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestDRAMModel(unittest.TestCase):
    """
    Class for testing the DRAM data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the DRAM class.
        """

        self.DUT = DRAM()

        self._base_values = (0, 1, 'Alt Part #', 'Attachments', 'CAGE Code',
                             'Comp Ref Des', 6.0, 7.0, 8.0, 'Description',
                             10.0, 11, 12, 'Figure #', 14.0, 'LCN', 16, 17,
                             18.0, 'Name', 'NSN', 21, 'Page #', 23, 24,
                             'Part #', 26, 'Ref Des', 28.0, 29, 'Remarks',
                             31.0, 'Spec #', 33, 34.0, 35.0, 36.0, 2014,
                             38, 39, 40, 41.0, 1, 1)
        self._stress_values = (44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0,
                               52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0,
                               'Sixty')
        self._rel_values = (61.0, 62.0, 63.0, 64.0, 65.0, 66, 67.0, 68.0, 69.0,
                            70.0, 71.0, 72.0, 73, 74.0, {}, 76.0, 77.0, 78.0,
                            79, 80.0, 81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 87.0,
                            88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96)
        self._user_values = (97.0, 98.0, 99.0, 100.0, 101.0, 102, 103, 104.0,
                             105.0, 106.0, 107.0, 108, 109, 110.0, 111, 112.0,
                             113.0, 114.0, 115, 116.0, 117.0, 118.0, 119, 120,
                             121.0, 122, 123, 124.0, 125.0, 126, 'Thirty',
                             'Thirty One', '32', '33', '34')

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestDRAM) __init__ should return an DRAM data model
        """

        self.assertTrue(isinstance(self.DUT, DRAM))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)

        # Verify the Component class was properly intialized.
        self.assertEqual(self.DUT.junction_temperature, 30.0)

        # Verify the Integrated Circuit class was properly initialized.
        self.assertEqual(self.DUT.category_id, 1)
        self.assertEqual(self.DUT.quality_id, 0)
        self.assertEqual(self.DUT.base_hr, 0.0)

        # Verify the Memory IC class was properly initialized.
        self.assertEqual(self.DUT.subcategory_id, 7)
        self.assertEqual(self.DUT.package_id, 0)
        self.assertEqual(self.DUT.n_pins, 0)
        self.assertEqual(self.DUT.family_id, 0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestDRAM) set_attributes should return a 0 error code on success
        """

        _all_values = self._base_values + self._stress_values + \
                      self._rel_values + self._user_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[5], 0)
        self.assertEqual(self.DUT.package_id, 120)
        self.assertEqual(self.DUT.n_pins, 121)
        self.assertEqual(self.DUT.family_id, 122)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestDRAM) set_attributes should return a 40 error code when too few items are passed
        """

        _user_values = (97.0, 98.0, 99.0, 100.0, 101.0, 102, 103, 104.0,
                        105.0, 106.0, 107.0, 108, 109, 110.0, 111, 112.0,
                        113.0, 114.0, 115, 116.0, 117, 118, 119, 120)

        _all_values = self._base_values + self._stress_values + \
                      self._rel_values + _user_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[5], 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestDRAM) set_attributes should return a 10 error code when the wrong type is passed
        """

        _user_values = (97.0, 98.0, 99.0, 100.0, 101.0, 102, 103, 104.0, 105.0,
                        106.0, 107.0, 108, 109, 110.0, 111, 112.0, 113.0,
                        114.0, 115, 116.0, 117, 118, 119, None, 121.0, 122,
                        123, 124.0, 125.0, 126, 'Thirty', 'Thirty One', '32',
                        '33', '34')

        _all_values = self._base_values + self._stress_values + \
                      self._rel_values + _user_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[5], 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestDRAM) get_attributes should return a tuple of attribute values
        """

        _base_values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0,
                        0, 0, '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0,
                        '', 1, '', 1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0,
                        2014, 0, 0, 0, 0.0, 1, 7)
        _stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                          0.0, 1.0, 30.0, 25.0, 0.0, 25.0, '')
        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0)
        _comp_values = (0.0, 30.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
                        0.0, 0, 0, 0, 0, 0)

        _all_values = _base_values + _stress_values + _rel_values + \
            _comp_values

        _result = self.DUT.get_attributes()
        self.assertEqual(_result[:38], _base_values[:38])
        self.assertEqual(_result[38:50], _stress_values[:12])
        self.assertEqual(_result[50], _stress_values[16])
        self.assertEqual(_result[51:87], _rel_values)
        self.assertEqual(_result[87:89], _base_values[42:44])
        self.assertEqual(_result[89:93], _stress_values[12:16])
        self.assertEqual(_result[93:], _comp_values)

    @attr(all=False, unit=False)
    def test_calculate_217_count(self):
        """
        (TestDRAM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality_id = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')

    @attr(all=True, unit=True)
    def test_calculate_217_count_all(self):
        """
        (TestDRAM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.num_elements = 4096
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.04)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.0E-8)

        self.DUT.num_elements = 48000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.051)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.275E-8)

        self.DUT.num_elements = 246000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.06)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.5E-8)

        self.DUT.num_elements = 256096
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.077)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.925E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestDRAM) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality_id = 1

        self.DUT.operating_power = 0.25
        self.DUT.thermal_resistance = 60.0

        self.DUT.technology_id = 1
        self.DUT.package_id = 3
        self.DUT.num_elements = 16000
        self.DUT.n_pins = 18
        self.DUT.years_produced = 1.5
        self.DUT.case_temperature = 35.0

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.junction_temperature, 50.0)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         '(C1 * piT + C2 * piE) * piQ * piL')
        self.assertEqual(self.DUT.hazard_rate_model['C1'], 0.0013)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['C2'], 0.0063511495)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 0.7144676)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piL'], 1.2458647)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.2158302E-8)


class TestEEPROMModel(unittest.TestCase):
    """
    Class for testing the EEPROM data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the EEPROM class.
        """

        self.DUT = EEPROM()

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
        (TestEEPROM) __init__ should return an EEPROM data model
        """

        self.assertTrue(isinstance(self.DUT, EEPROM))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Integrated Circuit class was properly initialized.
        self.assertEqual(self.DUT.category, 1)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piQ, 1.0)

        # Verify the Memory IC class was properly initialized.
        self.assertEqual(self.DUT.subcategory, 6)
        self.assertEqual(self.DUT.part_type, 0)
        self.assertEqual(self.DUT.technology, 0)
        self.assertEqual(self.DUT.package, 0)
        self.assertEqual(self.DUT.ecc, 0)
        self.assertEqual(self.DUT.num_elements, 0)
        self.assertEqual(self.DUT.n_cycles, 0)
        self.assertEqual(self.DUT.n_pins, 0)
        self.assertEqual(self.DUT.manufacturing, 0)
        self.assertEqual(self.DUT.years_production, 0.0)
        self.assertEqual(self.DUT.case_temperature, 0.0)
        self.assertEqual(self.DUT.life_op_hours, 0.0)
        self.assertEqual(self.DUT.C1, 0.0)
        self.assertEqual(self.DUT.C2, 0.0)
        self.assertEqual(self.DUT.piL, 0.0)
        self.assertEqual(self.DUT.lambda_cyc, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestEEPROM) set_attributes should return a 0 error code on success
        """

        _my_values = (1, 3, 2, 2, 32000, 516, 8, 1, 1.5, 75.0, 1000.0, 0.0025,
                      0.0097, 1.2, 0.0038)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._ic_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.part_type, 1)
        self.assertEqual(self.DUT.technology, 3)
        self.assertEqual(self.DUT.package, 2)
        self.assertEqual(self.DUT.ecc, 2)
        self.assertEqual(self.DUT.num_elements, 32000)
        self.assertEqual(self.DUT.n_cycles, 516)
        self.assertEqual(self.DUT.n_pins, 8)
        self.assertEqual(self.DUT.manufacturing, 1)
        self.assertEqual(self.DUT.years_production, 1.5)
        self.assertEqual(self.DUT.case_temperature, 75.0)
        self.assertEqual(self.DUT.life_op_hours, 1000.0)
        self.assertEqual(self.DUT.C1, 0.0025)
        self.assertEqual(self.DUT.C2, 0.0097)
        self.assertEqual(self.DUT.piL, 1.2)
        self.assertEqual(self.DUT.lambda_cyc, 0.0038)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestEEPROM) get_attributes should return a tuple of attribute values
        """

        _my_values = (0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
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

    @attr(all=False, unit=False)
    def test_calculate_217_count(self):
        """
        (TestEEPROM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
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
        (TestEEPROM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.technology = 2
        self.DUT.num_elements = 4096
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.053)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.325E-8)

        self.DUT.technology = 1
        self.DUT.num_elements = 48000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.091)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.275E-8)

        self.DUT.technology = 2
        self.DUT.num_elements = 246000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.067)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.675E-8)

        self.DUT.technology = 1
        self.DUT.num_elements = 256096
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.21)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 5.25E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestEEPROM) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.operating_power = 0.25
        self.DUT.thermal_resistance = 60.0

        self.DUT.technology = 1
        self.DUT.package = 3
        self.DUT.num_elements = 16000
        self.DUT.n_pins = 18
        self.DUT.n_cycles = 200
        self.DUT.years_production = 1.5
        self.DUT.case_temperature = 35.0

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.junction_temperature, 50.0)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         '(C1 * piT + C2 * piE + lambdacyc) * piQ * piL')
        self.assertEqual(self.DUT.hazard_rate_model['C1'], 0.0094)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['C2'], 0.0063511495)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 0.7144676)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdacyc'],
                               0.004065449)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piL'], 1.2458647)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.4838145E-8)


class TestROMModel(unittest.TestCase):
    """
    Class for testing the ROM data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the ROM class.
        """

        self.DUT = ROM()

        self._base_values = (0, 1, 'Alt Part #', 'Attachments', 'CAGE Code',
                             'Comp Ref Des', 6.0, 7.0, 8.0, 'Description',
                             10.0, 11, 12, 'Figure #', 14.0, 'LCN', 16, 17,
                             18.0, 'Name', 'NSN', 21, 'Page #', 23, 24,
                             'Part #', 26, 'Ref Des', 28.0, 29, 'Remarks',
                             31.0, 'Spec #', 33, 34.0, 35.0, 36.0, 2014,
                             38, 39, 40, 41.0, 1, 1)
        self._stress_values = (44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0,
                               52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0,
                               'Sixty')
        self._rel_values = (61.0, 62.0, 63.0, 64.0, 65.0, 66, 67.0, 68.0, 69.0,
                            70.0, 71.0, 72.0, 73, 74.0, {}, 76.0, 77.0, 78.0,
                            79, 80.0, 81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 87.0,
                            88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96)
        self._user_values = (97.0, 98.0, 99.0, 100.0, 101.0, 102, 103, 104.0,
                             105.0, 106.0, 107.0, 108, 109, 110.0, 111, 112.0,
                             113.0, 114.0, 115, 116.0, 117.0, 118.0, 119, 120,
                             121.0, 122, 123, 124.0, 125.0, 126, 'Thirty',
                             'Thirty One', '32', '33', '34')

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestROM) __init__ should return an ROM data model
        """

        self.assertTrue(isinstance(self.DUT, ROM))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)

        # Verify the Component class was properly intialized.
        self.assertEqual(self.DUT.junction_temperature, 30.0)

        # Verify the Integrated Circuit class was properly initialized.
        self.assertEqual(self.DUT.category_id, 1)
        self.assertEqual(self.DUT.quality_id, 0)
        self.assertEqual(self.DUT.base_hr, 0.0)

        # Verify the Memory IC class was properly initialized.
        self.assertEqual(self.DUT.part_type, 0)
        self.assertEqual(self.DUT.package_id, 0)
        self.assertEqual(self.DUT.n_pins, 0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestROM) set_attributes should return a 0 error code on success
        """

        _all_values = self._base_values + self._stress_values + \
                      self._rel_values + self._user_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[5], 0)
        self.assertEqual(self.DUT.package_id, 120)
        self.assertEqual(self.DUT.n_pins, 121)
        self.assertEqual(self.DUT.family_id, 122)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestROM) set_attributes should return a 40 error code when too few items are passed
        """

        _user_values = (97.0, 98.0, 99.0, 100.0, 101.0, 102, 103, 104.0,
                        105.0, 106.0, 107.0, 108, 109, 110.0, 111, 112.0,
                        113.0, 114.0, 115, 116.0, 117, 118, 119, 120)

        _all_values = self._base_values + self._stress_values + \
                      self._rel_values + _user_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[5], 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestROM) set_attributes should return a 10 error code when the wrong type is passed
        """

        _user_values = (97.0, 98.0, 99.0, 100.0, 101.0, 102, 103, 104.0, 105.0,
                        106.0, 107.0, 108, 109, 110.0, 111, 112.0, 113.0,
                        114.0, 115, 116.0, 117, 118, 119, None, 121.0, 122,
                        123, 124.0, 125.0, 126, 'Thirty', 'Thirty One', '32',
                        '33', '34')

        _all_values = self._base_values + self._stress_values + \
                      self._rel_values + _user_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[5], 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestROM) get_attributes should return a tuple of attribute values
        """

        _base_values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0,
                        0, 0, '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0,
                        '', 1, '', 1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0,
                        2014, 0, 0, 0, 0.0, 1, 5)
        _stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                          0.0, 1.0, 30.0, 25.0, 0.0, 25.0, '')
        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0)
        _comp_values = (0.0, 30.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
                        0.0, 0, 0, 0, 0, 0)

        _all_values = _base_values + _stress_values + _rel_values + \
            _comp_values

        _result = self.DUT.get_attributes()
        self.assertEqual(_result[:38], _base_values[:38])
        self.assertEqual(_result[38:50], _stress_values[:12])
        self.assertEqual(_result[50], _stress_values[16])
        self.assertEqual(_result[51:87], _rel_values)
        self.assertEqual(_result[87:89], _base_values[42:44])
        self.assertEqual(_result[89:93], _stress_values[12:16])
        self.assertEqual(_result[93:], _comp_values)

    @attr(all=False, unit=False)
    def test_calculate_217_count(self):
        """
        (TestROM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality_id = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')

    @attr(all=True, unit=True)
    def test_calculate_217_count_all(self):
        """
        (TestROM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.num_elements = 4096
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.053)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.325E-8)

        self.DUT.num_elements = 48000
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.063)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.575E-8)

        self.DUT.num_elements = 246000
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.066)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.65E-8)

        self.DUT.num_elements = 256096
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.098)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.45E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestROM) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality_id = 1

        self.DUT.operating_power = 0.25
        self.DUT.thermal_resistance = 60.0

        self.DUT.technology_id = 1
        self.DUT.package_id = 3
        self.DUT.num_elements = 16000
        self.DUT.n_pins = 18
        self.DUT.years_produced = 1.5
        self.DUT.case_temperature = 35.0

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.junction_temperature, 50.0)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         '(C1 * piT + C2 * piE) * piQ * piL')
        self.assertEqual(self.DUT.hazard_rate_model['C1'], 0.0094)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['C2'], 0.0063511495)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 0.7144676)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piL'], 1.2458647)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.3960815E-8)


class TestSRAMModel(unittest.TestCase):
    """
    Class for testing the SRAM data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the SRAM class.
        """

        self.DUT = SRAM()

        self._base_values = (0, 1, 'Alt Part #', 'Attachments', 'CAGE Code',
                             'Comp Ref Des', 6.0, 7.0, 8.0, 'Description',
                             10.0, 11, 12, 'Figure #', 14.0, 'LCN', 16, 17,
                             18.0, 'Name', 'NSN', 21, 'Page #', 23, 24,
                             'Part #', 26, 'Ref Des', 28.0, 29, 'Remarks',
                             31.0, 'Spec #', 33, 34.0, 35.0, 36.0, 2014,
                             38, 39, 40, 41.0, 1, 1)
        self._stress_values = (44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0,
                               52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0,
                               'Sixty')
        self._rel_values = (61.0, 62.0, 63.0, 64.0, 65.0, 66, 67.0, 68.0, 69.0,
                            70.0, 71.0, 72.0, 73, 74.0, {}, 76.0, 77.0, 78.0,
                            79, 80.0, 81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 87.0,
                            88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96)
        self._user_values = (97.0, 98.0, 99.0, 100.0, 101.0, 102, 103, 104.0,
                             105.0, 106.0, 107.0, 108, 109, 110.0, 111, 112.0,
                             113.0, 114.0, 115, 116.0, 117.0, 118.0, 119, 120,
                             121.0, 122, 123, 124.0, 125.0, 126, 'Thirty',
                             'Thirty One', '32', '33', '34')

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestSRAM) __init__ should return an SRAM data model
        """

        self.assertTrue(isinstance(self.DUT, SRAM))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)

        # Verify the Component class was properly intialized.
        self.assertEqual(self.DUT.junction_temperature, 30.0)

        # Verify the Integrated Circuit class was properly initialized.
        self.assertEqual(self.DUT.category_id, 1)
        self.assertEqual(self.DUT.quality_id, 0)
        self.assertEqual(self.DUT.base_hr, 0.0)

        # Verify the SRAM IC class was properly initialized.
        self.assertEqual(self.DUT.package_id, 0)
        self.assertEqual(self.DUT.n_pins, 0)
        self.assertEqual(self.DUT.family_id, 0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestSRAM) set_attributes should return a 0 error code on success
        """

        _all_values = self._base_values + self._stress_values + \
                      self._rel_values + self._user_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[5], 0)
        self.assertEqual(self.DUT.package_id, 120)
        self.assertEqual(self.DUT.n_pins, 121)
        self.assertEqual(self.DUT.family_id, 122)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestSRAM) set_attributes should return a 40 error code when too few items are passed
        """

        _user_values = (97.0, 98.0, 99.0, 100.0, 101.0, 102, 103, 104.0,
                        105.0, 106.0, 107.0, 108, 109, 110.0, 111, 112.0,
                        113.0, 114.0, 115, 116.0, 117, 118, 119, 120)

        _all_values = self._base_values + self._stress_values + \
                      self._rel_values + _user_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[5], 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestSRAM) set_attributes should return a 10 error code when the wrong type is passed
        """

        _user_values = (97.0, 98.0, 99.0, 100.0, 101.0, 102, 103, 104.0, 105.0,
                        106.0, 107.0, 108, 109, 110.0, 111, 112.0, 113.0,
                        114.0, 115, 116.0, 117, 118, 119, None, 121.0, 122,
                        123, 124.0, 125.0, 126, 'Thirty', 'Thirty One', '32',
                        '33', '34')

        _all_values = self._base_values + self._stress_values + \
                      self._rel_values + _user_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_all_values)
        self.assertEqual(_error_code[5], 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestSRAM) get_attributes should return a tuple of attribute values
        """

        _base_values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0,
                        0, 0, '', 50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0,
                        '', 1, '', 1.0, 0, '', 0.0, '', 0, 30.0, 30.0, 0.0,
                        2014, 0, 0, 0, 0.0, 1, 8)
        _stress_values = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
                          0.0, 1.0, 30.0, 25.0, 0.0, 25.0, '')
        _rel_values = (0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                       0.0, 0)
        _comp_values = (0.0, 30.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
                        0.0, 0, 0, 0, 0, 0)

        _all_values = _base_values + _stress_values + _rel_values + \
            _comp_values

        _result = self.DUT.get_attributes()
        self.assertEqual(_result[:38], _base_values[:38])
        self.assertEqual(_result[38:50], _stress_values[:12])
        self.assertEqual(_result[50], _stress_values[16])
        self.assertEqual(_result[51:87], _rel_values)
        self.assertEqual(_result[87:89], _base_values[42:44])
        self.assertEqual(_result[89:93], _stress_values[12:16])
        self.assertEqual(_result[93:], _comp_values)

    @attr(all=False, unit=False)
    def test_calculate_217_count(self):
        """
        (TestSRAM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality_id = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')

    @attr(all=True, unit=True)
    def test_calculate_217_count_all(self):
        """
        (TestSRAM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.num_elements = 4096
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.05)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.25E-8)

        self.DUT.num_elements = 48000
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.073)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.825E-8)

        self.DUT.num_elements = 246000
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.1)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.5E-8)

        self.DUT.num_elements = 256096
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.16)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.0E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestSRAM) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality_id = 1

        self.DUT.operating_power = 0.25
        self.DUT.thermal_resistance = 60.0

        self.DUT.technology_id = 1
        self.DUT.package_id = 3
        self.DUT.num_elements = 16000
        self.DUT.n_pins = 18
        self.DUT.years_produced = 1.5
        self.DUT.case_temperature = 35.0

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.junction_temperature, 50.0)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         '(C1 * piT + C2 * piE) * piQ * piL')
        self.assertEqual(self.DUT.hazard_rate_model['C1'], 0.0062)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['C2'], 0.0063511495)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 0.7144676)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piL'], 1.2458647)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.3248711E-8)
