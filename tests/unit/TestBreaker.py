#!/usr/bin/env python -O
"""
This is the test class for testing Breaker Switch module algorithms and
models.
"""

# -*- coding: utf-8 -*-
#
<<<<<<< HEAD
#       tests.hardware.TestBreaker.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

=======
#       tests.unit.TestBreaker.py is part of The RTK Project
#
# All rights reserved.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

<<<<<<< HEAD
import dao.DAO as _dao
=======
import unittest
from nose.plugins.attrib import attr

>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
from hardware.component.switch.Breaker import Breaker

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestBreakerModel(unittest.TestCase):
    """
    Class for testing the Breaker Switch data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Breaker Switch class.
        """

<<<<<<< HEAD
        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.DUT = Breaker()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestBreaker) __init__ should return a Breaker Switch data model
        """

        self.assertTrue(isinstance(self.DUT, Breaker))

        # Verify Hardware class was properly initialized.
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.category_id, 0)

        # Verify the Switch class was properly initialized.
        self.assertEqual(self.DUT.category, 7)
        self.assertEqual(self.DUT.quality, 0)
        self.assertEqual(self.DUT.q_override, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)

        # Verify the Breaker Switch class was properly initialized.
        self.assertEqual(self.DUT.subcategory, 71)
        self.assertEqual(self.DUT.construction, 0)
        self.assertEqual(self.DUT.contact_form, 0)
        self.assertEqual(self.DUT.use, 0)
        self.assertEqual(self.DUT.piC, 0.0)
        self.assertEqual(self.DUT.piU, 0.0)
        self.assertEqual(self.DUT.piQ, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestBreaker) set_attributes should return a 0 error code on success
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
                   1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 1.5, 4.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 2, 4, 6)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.quality, 3)
        self.assertEqual(self.DUT.construction, 2)
        self.assertEqual(self.DUT.contact_form, 4)
        self.assertEqual(self.DUT.use, 6)
        self.assertEqual(self.DUT.piC, 2.0)
        self.assertEqual(self.DUT.piU, 1.0)
        self.assertEqual(self.DUT.piQ, 1.0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestBreaker) set_attributes should return a 40 error code when too few items are passed
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
                   1.0, 0.01, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestBreaker) set_attributes should return a 10 error code when the wrong type is passed
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
                   1.0, 0.0, 0.01, 2.0, 1.0, 1.0, None, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, '')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestBreaker) get_attributes should return a tuple of attribute values
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
                   0, 0.0, 0.0, 0.0, '', 0, 0, 0, 0.0, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestBreaker) get_attributes(set_attributes(values)) == values
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
                      1.0, 125.0, 0.01, 2.0, 1.0, 1.0, 1.5, 2.5, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 5, 8, 2)
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
                       0, 0, 0.0, 30.0, 0.0, 358.0, 3, 1.0, 125.0, 0.01, '',
                       5, 8, 2, 2.0, 1.0, 1.0)

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
<<<<<<< HEAD
        (TestBreaker) calculate should return False on success when calculating MIL-HDBK-217F parts count results
=======
        (TestBreaker) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
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
        self.assertEqual(self.DUT.hazard_rate_model['lambdab'], 1.6)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.6E-06)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_magnetic(self):
        """
<<<<<<< HEAD
        (TestBreaker) calculate should return False on success when calculating MIL-HDBK-217F stress results for a magnetic actuation breaker
=======
        (TestBreaker) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for a magnetic actuation breaker
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1
        self.DUT.construction = 1
        self.DUT.contact_form = 1
        self.DUT.use = 1

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piC * piU * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.02)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piU'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 4.0E-08)

    @attr(all=True, unit=True)
    def test_calculate_217_stress_thermal(self):
        """
<<<<<<< HEAD
        (TestBreaker) calculate should return False on success when calculating MIL-HDBK-217F stress results for a thermal actuation breaker
=======
        (TestBreaker) calculate_part should return False on success when calculating MIL-HDBK-217F stress results for a thermal actuation breaker
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 2
        self.DUT.construction = 2
        self.DUT.contact_form = 2
        self.DUT.use = 2

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piC * piU * piQ * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.038)
        self.assertEqual(self.DUT.hazard_rate_model['piC'], 2.0)
        self.assertEqual(self.DUT.hazard_rate_model['piU'], 10.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piQ'], 8.4)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 2.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.2768E-05)

    @attr(all=True, unit=False)
    def test_calculate_217_stress_lamp(self):
        """
<<<<<<< HEAD
        (TestBreaker) calculate should return False on success when calculating MIL-HDBK-217F stress results with a lamp load
=======
        (TestBreaker) calculate_part should return False on success when calculating MIL-HDBK-217F stress results with a lamp load
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 2
        self.DUT.load_type = 3
        self.DUT.n_contacts = 8
        self.DUT.cycles_per_hour = 0.8
        self.DUT.operating_current = 0.023
        self.DUT.rated_current = 0.05

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         '(lambdab + piN * lambdab2) * piCYC * piL * piE')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.086)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab2'], 0.089)
        self.assertEqual(self.DUT.hazard_rate_model['piN'], 8.0)
        self.assertEqual(self.DUT.hazard_rate_model['piCYC'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piL'], 198.3434254)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 0.0004748342)

    @attr(all=True, unit=False)
    def test_calculate_217_stress_overflow(self):
        """
<<<<<<< HEAD
        (TestBreaker) calculate should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
=======
        (TestBreaker) calculate_part should return True when an OverflowError is raised when calculating MIL-HDBK-217F stress results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000027
        self.DUT.effective_resistance = 0.5
        self.DUT.reference_temperature = 0.000000000000001

<<<<<<< HEAD
        self.assertTrue(self.DUT.calculate())
=======
        self.assertTrue(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

    @attr(all=True, unit=False)
    def test_calculate_217_stress_zero_division(self):
        """
<<<<<<< HEAD
        (TestBreaker) calculate should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
=======
        (TestBreaker) calculate_part should return True when a ZeroDivisionError is raised when calculating MIL-HDBK-217F stress results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.hazard_rate_type = 2
        self.DUT.operating_voltage = 1.25
        self.DUT.acvapplied = 0.025
        self.DUT.rated_voltage = 3.3
        self.DUT.capacitance = 0.0000033
        self.DUT.effective_resistance = 0.5
        self.DUT.reference_temperature = 0.0

<<<<<<< HEAD
        self.assertTrue(self.DUT.calculate())
=======
        self.assertTrue(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
