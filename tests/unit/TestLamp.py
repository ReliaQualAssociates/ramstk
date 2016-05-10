#!/usr/bin/env python -O
"""
This is the test class for testing Lamp module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
<<<<<<< HEAD
#       tests.hardware.TestLamp.py is part of The RTK Project
#
# All rights reserved.

=======
#       tests.unit.TestLamp.py is part of The RTK Project
#
# All rights reserved.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

<<<<<<< HEAD
import dao.DAO as _dao
from hardware.component.miscellaneous.Lamp import *
=======
from hardware.component.miscellaneous.Lamp import Lamp
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestLampModel(unittest.TestCase):
    """
    Class for testing the Lamp data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Lamp class.
        """

<<<<<<< HEAD
        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.DUT = Lamp()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestLamp) __init__ should return a Lamp data model
        """

        self.assertTrue(isinstance(self.DUT, Lamp))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify Lamp class was properly initialized.
<<<<<<< HEAD
        self.assertEqual(self.DUT.category, 10)
        self.assertEqual(self.DUT.subcategory, 83)
=======
        self.assertEqual(self.DUT.category, 6)
        self.assertEqual(self.DUT.subcategory, 4)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.assertEqual(self.DUT.application, 0)
        self.assertEqual(self.DUT.illuminate_hours, 0.0)
        self.assertEqual(self.DUT.operate_hours, 0.0)
        self.assertEqual(self.DUT.base_hr, 0.0)
        self.assertEqual(self.DUT.piU, 0.0)
        self.assertEqual(self.DUT.piA, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestLamp) set_attributes should return a 0 error code on success
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
                   1.0, 2.0, 0.01, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.application, 1)
        self.assertEqual(self.DUT.illuminate_hours, 1.0)
        self.assertEqual(self.DUT.operate_hours, 2.0)
        self.assertEqual(self.DUT.base_hr, 0.01)
        self.assertEqual(self.DUT.piU, 1.0)
        self.assertEqual(self.DUT.piA, 1.0)
        self.assertEqual(self.DUT.piE, 1.0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestLamp) set_attributes should return a 40 error code when too few items are passed
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
                   1.0, 2.0, 0.01, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestLamp) set_attributes should return a 10 error code when the wrong type is passed
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
                   1.0, None, 0.01, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestLamp) get_attributes should return a tuple of attribute values
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
                   0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '')

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestLamp) get_attributes(set_attributes(values)) == values
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
                      1.0, 2.0, 0.01, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1)
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
                       1, 1.0, 2.0, 0.01, 1.0, 1.0, 1.0, '')

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
<<<<<<< HEAD
        (TestLamp) calculate should return False on success when calculating MIL-HDBK-217F parts count results
=======
        (TestLamp) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.hazard_rate_type = 1
        self.DUT.environment_active = 5
        self.DUT.application = 1

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 16.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.6E-5)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
<<<<<<< HEAD
        (TestLamp) calculate should return False on success when calculating MIL-HDBK-217F parts stress results
=======
        (TestLamp) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.environment_active = 3
        self.DUT.rated_voltage = 12.0
        self.DUT.application = 2
        self.DUT.illuminate_hours = 2.5
        self.DUT.operate_hours = 6.43

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piU * piA * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               1.8254735)
        self.assertEqual(self.DUT.hazard_rate_model['piU'], 0.72)
        self.assertEqual(self.DUT.hazard_rate_model['piA'], 3.3)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.3011975E-5)
