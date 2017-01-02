#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestPCB.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing PCB Connection module algorithms and models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from hardware.component.connection.PCB import PCB

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestPCBModel(unittest.TestCase):
    """
    Class for testing the PCB Connection data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the PCB Connection class.
        """

        self.DUT = PCB()

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
        self._connection_values = (0.0, 0.0, 0.0, 0.0, 0, "")

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestPCB) __init__ should return a PCB Connection data model
        """

        self.assertTrue(isinstance(self.DUT, PCB))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Connection class was properly initialized.
        self.assertEqual(self.DUT.category, 8)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)

        # Verify the PCB Connection class was properly initialized.
        self.assertEqual(self.DUT.subcategory, 73)
        self.assertEqual(self.DUT.n_active_contacts, 0)
        self.assertEqual(self.DUT.contact_gauge, 26)
        self.assertEqual(self.DUT.amps_per_contact, 0.0)
        self.assertEqual(self.DUT.mate_unmate_cycles, 0.0)
        self.assertEqual(self.DUT.piK, 0.0)
        self.assertEqual(self.DUT.piP, 0.0)
        self.assertEqual(self.DUT.contact_temperature, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestPCB) set_attributes should return a 0 error code on success
        """

        _my_values = (0.0, 0.0, 0.0, 0.0, 40.0, 0, 0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._connection_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestPCB) set_attributes should return a 40 error code when too few items are passed
        """

        _my_values = (0.0, 0.0, 0.0, 0.0, 40.0, 0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._connection_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestPCB) set_attributes should return a 10 error code when the wrong type is passed
        """

        _my_values = (0.0, 0.0, None, 0.0, 40.0, 0, 0)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._connection_values + \
                  _my_values

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestPCB) get_attributes should return a tuple of attribute values
        """
        
        _my_values = (0.0, 0.0, 0.0, 0.0, 0.0, 0, 26)
        _values = (None, None, '', '', '', '', 0.0, 0.0, 0.0, '', 100.0, 0, 0, '', 
                   50.0, '', 1, 0, 10.0, '', '', 0, '', 0, 0, '', 1, '', 1.0, 0, '', 
                   0.0, '', 0, 30.0, 30.0, 0.0, 2014, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                   1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 1, 0.0, {}, 0.0, 0.0, 0.0, 1, 0.0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 
                   0.0, 0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0, 0, 0, 0, 0, 0, 
                   0, 0, 0, 0], ['', '', '', '', ''], 0, 0, 0.0, 30.0, 0.0, 30.0, 
                   0.0, 0.0, 1.0, 0.0, 0, "") + _my_values

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestPCB) get_attributes(set_attributes(values)) == values
        """

        _my_values = (0.0, 0.0, 0.0, 0.0, 0.0, 0, 26)
        _values = self._base_values + self._stress_values + self._rel_values + \
                  self._user_values + self._comp_values + self._connection_values + \
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
        self.assertEqual(_result[95:101], self._connection_values)
        
        self.assertEqual(_result[101:], _my_values)
        
    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
        (TestPCB) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
        """

        self.DUT.environment_active = 5
        self.DUT.hazard_rate_type = 1
        self.DUT.quality = 1

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piQ')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.1)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.0E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
        (TestPCB) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.n_active_contacts = 20
        self.DUT.mate_unmate_cycles = 10.0

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piE * piK * piP')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0002844941)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piK'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piP'], 4.0062301)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.4580053E-9)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_no_active_contacts(self):
        """
        (TestPCB) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results with no active contacts
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.n_active_contacts = 1
        self.DUT.mate_unmate_cycles = 10.0

        self.assertFalse(self.DUT.calculate_part())
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piE * piK * piP')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0002844941)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piK'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piP'], 0.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 0.0)
