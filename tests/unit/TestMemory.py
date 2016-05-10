#!/usr/bin/env python -O
"""
This is the test class for testing Memory IC module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
<<<<<<< HEAD
#       tests.hardware.TestMemory.py is part of The RTK Project
=======
#       tests.unit.TestMemory.py is part of The RTK Project
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

<<<<<<< HEAD
import dao.DAO as _dao
from hardware.component.integrated_circuit.Memory import *
=======
from hardware.component.integrated_circuit.Memory import Memory, DRAM, \
                                                         EEPROM, ROM, SRAM
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestMemoryModel(unittest.TestCase):
    """
    Class for testing the Memory IC data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Memory IC class.
        """

<<<<<<< HEAD
        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.DUT = Memory()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestMemory) __init__ should return an Memory IC data model
        """

        self.assertTrue(isinstance(self.DUT, Memory))

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
        self.assertEqual(self.DUT.subcategory, 3)
        self.assertEqual(self.DUT.part_type, 0)
        self.assertEqual(self.DUT.technology, 0)
        self.assertEqual(self.DUT.package, 0)
        self.assertEqual(self.DUT.ecc, 0)
        self.assertEqual(self.DUT.memory_size, 0)
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
        (TestMemory) set_attributes should return a 0 error code on success
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
                   0.0, 0.0, 1.0, 0.0, 1.5, 75.0, 22000.0, 0.0025, 0.0097, 1.2,
                   0.0038, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 3, 2, 2, 32000, 516, 8, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.part_type, 1)
        self.assertEqual(self.DUT.technology, 3)
        self.assertEqual(self.DUT.package, 2)
        self.assertEqual(self.DUT.ecc, 2)
        self.assertEqual(self.DUT.memory_size, 32000)
        self.assertEqual(self.DUT.n_cycles, 516)
        self.assertEqual(self.DUT.n_pins, 8)
        self.assertEqual(self.DUT.manufacturing, 1)
        self.assertEqual(self.DUT.years_production, 1.5)
        self.assertEqual(self.DUT.case_temperature, 75.0)
        self.assertEqual(self.DUT.C1, 0.0025)
        self.assertEqual(self.DUT.C2, 0.0097)
        self.assertEqual(self.DUT.piL, 1.2)
        self.assertEqual(self.DUT.lambda_cyc, 0.0038)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestMemory) set_attributes should return a 40 error code when too few items are passed
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
                   0.0, 0.0, 1.0, 0.0, 1.5, 75.0, 22000.0, 0.0025, 0.0097, 1.2,
                   0.0038, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 3, 2, 2, 32000, 8, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestMemory) set_attributes should return a 10 error code when the wrong type is passed
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
                   0.0, 0.0, 1.0, 0.0, 1.5, 75.0, 22000.0, 0.0025, 0.0097, 1.2,
                   0.0038, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 3, 2, 2, 32000, '', 8, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestMemory) get_attributes should return a tuple of attribute values
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
                   0.0, 0.0, 1.0, 0.0, 0.0, 0, '',
                   0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestMemory) get_attributes(set_attributes(values)) == values
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
                      0.0, 0.0, 1.0, 0.0, 1.5, 75.0, 22000.0, 0.0025, 0.0097,
                      1.2, 0.0038, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 1, 3, 2, 2, 32000, 516, 8, 1)
        _out_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                       'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                       0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                       0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                       'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                       1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                       0.0, 1.0,
                       0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, '', 0.0, 0.0, 0.0, 1, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0,
                       1.0, 0.0, 0.0, 0,
                       0, 0,
                       0.0, 30.0, 0.0, 358.0,
                       0.0, 0.0, 1.0, 0.0, 1.5, 0, '',
                       1, 3, 2, 2, 32000, 516, 8, 1.5, 75.0, 22000.0, 0.0025,
                       0.0097, 1.2, 0.0038, 1)

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)


class TestDRAMModel(unittest.TestCase):
    """
    Class for testing the DRAM data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the DRAM class.
        """

<<<<<<< HEAD
        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.DUT = DRAM()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestDRAM) __init__ should return an DRAM data model
        """

        self.assertTrue(isinstance(self.DUT, DRAM))

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
        self.assertEqual(self.DUT.subcategory, 7)
        self.assertEqual(self.DUT.part_type, 0)
        self.assertEqual(self.DUT.technology, 0)
        self.assertEqual(self.DUT.package, 0)
        self.assertEqual(self.DUT.ecc, 0)
        self.assertEqual(self.DUT.memory_size, 0)
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
        (TestDRAM) set_attributes should return a 0 error code on success
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
                   0.0, 0.0, 1.0, 0.0, 1.5, 75.0, 22000.0, 0.0025, 0.0097, 1.2,
                   0.0038, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 3, 2, 2, 32000, 516, 8, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.part_type, 1)
        self.assertEqual(self.DUT.technology, 3)
        self.assertEqual(self.DUT.package, 2)
        self.assertEqual(self.DUT.ecc, 2)
        self.assertEqual(self.DUT.memory_size, 32000)
        self.assertEqual(self.DUT.n_cycles, 516)
        self.assertEqual(self.DUT.n_pins, 8)
        self.assertEqual(self.DUT.manufacturing, 1)
        self.assertEqual(self.DUT.years_production, 1.5)
        self.assertEqual(self.DUT.case_temperature, 75.0)
        self.assertEqual(self.DUT.C1, 0.0025)
        self.assertEqual(self.DUT.C2, 0.0097)
        self.assertEqual(self.DUT.piL, 1.2)
        self.assertEqual(self.DUT.lambda_cyc, 0.0038)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestDRAM) get_attributes should return a tuple of attribute values
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
                   0.0, 0.0, 1.0, 0.0, 0.0, 0, '',
                   0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=False, unit=False)
    def test_calculate_217_count(self):
        """
<<<<<<< HEAD
        (TestDRAM) calculate should return False on success when calculating MIL-HDBK-217F parts count results
=======
        (TestDRAM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1
<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')

    @attr(all=True, unit=True)
    def test_calculate_217_count_all(self):
        """
<<<<<<< HEAD
        (TestDRAM) calculate should return False on success when calculating MIL-HDBK-217F parts count results
=======
        (TestDRAM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.memory_size = 4096
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.04)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.0E-8)

        self.DUT.memory_size = 48000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.051)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.275E-8)

        self.DUT.memory_size = 246000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.06)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.5E-8)

        self.DUT.memory_size = 256096
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.077)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.925E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
<<<<<<< HEAD
        (TestDRAM) calculate should return False on success when calculating MIL-HDBK-217F parts stress results
=======
        (TestDRAM) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.operating_power = 0.25
        self.DUT.thermal_resistance = 60.0

        self.DUT.technology = 1
        self.DUT.package = 3
        self.DUT.memory_size = 16000
        self.DUT.n_pins = 18
        self.DUT.years_production = 1.5
        self.DUT.case_temperature = 35.0

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.assertEqual(self.DUT.junction_temperature, 50.0)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         '(C1 * piT + C2 * piE + lambdacyc) * piQ * piL')
        self.assertEqual(self.DUT.hazard_rate_model['C1'], 0.0013)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['C2'], 0.0063511495)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 0.7144676)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertEqual(self.DUT.hazard_rate_model['lambdacyc'], 0.0)
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

<<<<<<< HEAD
        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.DUT = EEPROM()

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
        self.assertEqual(self.DUT.memory_size, 0)
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
                   0.0, 0.0, 1.0, 0.0, 1.5, 75.0, 22000.0, 0.0025, 0.0097, 1.2,
                   0.0038, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 3, 2, 2, 32000, 516, 8, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.part_type, 1)
        self.assertEqual(self.DUT.technology, 3)
        self.assertEqual(self.DUT.package, 2)
        self.assertEqual(self.DUT.ecc, 2)
        self.assertEqual(self.DUT.memory_size, 32000)
        self.assertEqual(self.DUT.n_cycles, 516)
        self.assertEqual(self.DUT.n_pins, 8)
        self.assertEqual(self.DUT.manufacturing, 1)
        self.assertEqual(self.DUT.years_production, 1.5)
        self.assertEqual(self.DUT.case_temperature, 75.0)
        self.assertEqual(self.DUT.C1, 0.0025)
        self.assertEqual(self.DUT.C2, 0.0097)
        self.assertEqual(self.DUT.piL, 1.2)
        self.assertEqual(self.DUT.lambda_cyc, 0.0038)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestEEPROM) get_attributes should return a tuple of attribute values
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
                   0.0, 0.0, 1.0, 0.0, 0.0, 0, '',
                   0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=False, unit=False)
    def test_calculate_217_count(self):
        """
<<<<<<< HEAD
        (TestEEPROM) calculate should return False on success when calculating MIL-HDBK-217F parts count results
=======
        (TestEEPROM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1
<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')

    @attr(all=True, unit=True)
    def test_calculate_217_count_all(self):
        """
<<<<<<< HEAD
        (TestEEPROM) calculate should return False on success when calculating MIL-HDBK-217F parts count results
=======
        (TestEEPROM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.technology = 2
        self.DUT.memory_size = 4096
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.053)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.325E-8)

        self.DUT.technology = 1
        self.DUT.memory_size = 48000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.091)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.275E-8)

        self.DUT.technology = 2
        self.DUT.memory_size = 246000
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.067)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.675E-8)

        self.DUT.technology = 1
        self.DUT.memory_size = 256096
        self.test_calculate_217_count()
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.21)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 5.25E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
<<<<<<< HEAD
        (TestEEPROM) calculate should return False on success when calculating MIL-HDBK-217F parts stress results
=======
        (TestEEPROM) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.operating_power = 0.25
        self.DUT.thermal_resistance = 60.0

        self.DUT.technology = 1
        self.DUT.package = 3
        self.DUT.memory_size = 16000
        self.DUT.n_pins = 18
        self.DUT.n_cycles = 200
        self.DUT.years_production = 1.5
        self.DUT.case_temperature = 35.0

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

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

<<<<<<< HEAD
        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.DUT = ROM()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestROM) __init__ should return an ROM data model
        """

        self.assertTrue(isinstance(self.DUT, ROM))

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
        self.assertEqual(self.DUT.subcategory, 5)
        self.assertEqual(self.DUT.part_type, 0)
        self.assertEqual(self.DUT.technology, 0)
        self.assertEqual(self.DUT.package, 0)
        self.assertEqual(self.DUT.ecc, 0)
        self.assertEqual(self.DUT.memory_size, 0)
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
        (TestROM) set_attributes should return a 0 error code on success
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
                   0.0, 0.0, 1.0, 0.0, 1.5, 75.0, 22000.0, 0.0025, 0.0097, 1.2,
                   0.0038, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 3, 2, 2, 32000, 516, 8, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.part_type, 1)
        self.assertEqual(self.DUT.technology, 3)
        self.assertEqual(self.DUT.package, 2)
        self.assertEqual(self.DUT.ecc, 2)
        self.assertEqual(self.DUT.memory_size, 32000)
        self.assertEqual(self.DUT.n_cycles, 516)
        self.assertEqual(self.DUT.n_pins, 8)
        self.assertEqual(self.DUT.manufacturing, 1)
        self.assertEqual(self.DUT.years_production, 1.5)
        self.assertEqual(self.DUT.case_temperature, 75.0)
        self.assertEqual(self.DUT.C1, 0.0025)
        self.assertEqual(self.DUT.C2, 0.0097)
        self.assertEqual(self.DUT.piL, 1.2)
        self.assertEqual(self.DUT.lambda_cyc, 0.0038)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestROM) get_attributes should return a tuple of attribute values
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
                   0.0, 0.0, 1.0, 0.0, 0.0, 0, '',
                   0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=False, unit=False)
    def test_calculate_217_count(self):
        """
<<<<<<< HEAD
        (TestROM) calculate should return False on success when calculating MIL-HDBK-217F parts count results
=======
        (TestROM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1
<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')

    @attr(all=True, unit=True)
    def test_calculate_217_count_all(self):
        """
<<<<<<< HEAD
        (TestROM) calculate should return False on success when calculating MIL-HDBK-217F parts count results
=======
        (TestROM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.memory_size = 4096
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.053)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.325E-8)

        self.DUT.memory_size = 48000
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.063)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.575E-8)

        self.DUT.memory_size = 246000
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.066)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.65E-8)

        self.DUT.memory_size = 256096
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.098)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.45E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
<<<<<<< HEAD
        (TestROM) calculate should return False on success when calculating MIL-HDBK-217F parts stress results
=======
        (TestROM) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.operating_power = 0.25
        self.DUT.thermal_resistance = 60.0

        self.DUT.technology = 1
        self.DUT.package = 3
        self.DUT.memory_size = 16000
        self.DUT.n_pins = 18
        self.DUT.years_production = 1.5
        self.DUT.case_temperature = 35.0

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.assertEqual(self.DUT.junction_temperature, 50.0)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         '(C1 * piT + C2 * piE + lambdacyc) * piQ * piL')
        self.assertEqual(self.DUT.hazard_rate_model['C1'], 0.0094)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['C2'], 0.0063511495)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 0.7144676)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertEqual(self.DUT.hazard_rate_model['lambdacyc'], 0.0)
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

<<<<<<< HEAD
        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.DUT = SRAM()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestSRAM) __init__ should return an SRAM data model
        """

        self.assertTrue(isinstance(self.DUT, SRAM))

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
        self.assertEqual(self.DUT.subcategory, 8)
        self.assertEqual(self.DUT.part_type, 0)
        self.assertEqual(self.DUT.technology, 0)
        self.assertEqual(self.DUT.package, 0)
        self.assertEqual(self.DUT.ecc, 0)
        self.assertEqual(self.DUT.memory_size, 0)
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
        (TestSRAM) set_attributes should return a 0 error code on success
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
                   0.0, 0.0, 1.0, 0.0, 1.5, 75.0, 22000.0, 0.0025, 0.0097, 1.2,
                   0.0038, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 3, 2, 2, 32000, 516, 8, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.part_type, 1)
        self.assertEqual(self.DUT.technology, 3)
        self.assertEqual(self.DUT.package, 2)
        self.assertEqual(self.DUT.ecc, 2)
        self.assertEqual(self.DUT.memory_size, 32000)
        self.assertEqual(self.DUT.n_cycles, 516)
        self.assertEqual(self.DUT.n_pins, 8)
        self.assertEqual(self.DUT.manufacturing, 1)
        self.assertEqual(self.DUT.years_production, 1.5)
        self.assertEqual(self.DUT.case_temperature, 75.0)
        self.assertEqual(self.DUT.C1, 0.0025)
        self.assertEqual(self.DUT.C2, 0.0097)
        self.assertEqual(self.DUT.piL, 1.2)
        self.assertEqual(self.DUT.lambda_cyc, 0.0038)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestSRAM) get_attributes should return a tuple of attribute values
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
                   0.0, 0.0, 1.0, 0.0, 0.0, 0, '',
                   0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=False, unit=False)
    def test_calculate_217_count(self):
        """
<<<<<<< HEAD
        (TestSRAM) calculate should return False on success when calculating MIL-HDBK-217F parts count results
=======
        (TestSRAM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1
<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')

    @attr(all=True, unit=True)
    def test_calculate_217_count_all(self):
        """
<<<<<<< HEAD
        (TestSRAM) calculate should return False on success when calculating MIL-HDBK-217F parts count results
=======
        (TestSRAM) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.memory_size = 4096
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.05)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.25E-8)

        self.DUT.memory_size = 48000
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.073)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.825E-8)

        self.DUT.memory_size = 246000
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.1)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 2.5E-8)

        self.DUT.memory_size = 256096
        self.test_calculate_217_count()
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 0.16)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.0E-8)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
<<<<<<< HEAD
        (TestSRAM) calculate should return False on success when calculating MIL-HDBK-217F parts stress results
=======
        (TestSRAM) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.operating_power = 0.25
        self.DUT.thermal_resistance = 60.0

        self.DUT.technology = 1
        self.DUT.package = 3
        self.DUT.memory_size = 16000
        self.DUT.n_pins = 18
        self.DUT.years_production = 1.5
        self.DUT.case_temperature = 35.0

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.assertEqual(self.DUT.junction_temperature, 50.0)
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         '(C1 * piT + C2 * piE + lambdacyc) * piQ * piL')
        self.assertEqual(self.DUT.hazard_rate_model['C1'], 0.0062)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['C2'], 0.0063511495)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piT'], 0.7144676)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 6.0)
        self.assertEqual(self.DUT.hazard_rate_model['lambdacyc'], 0.0)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 0.25)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piL'], 1.2458647)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.3248711E-8)
