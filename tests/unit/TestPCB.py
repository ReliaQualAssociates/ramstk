#!/usr/bin/env python -O
"""
This is the test class for testing PCB Connection module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
<<<<<<< HEAD
#       tests.hardware.TestPCB.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

=======
#       tests.unit.TestPCB.py is part of The RTK Project
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

<<<<<<< HEAD
        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.DUT = PCB()

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
                   0.0, 0.0, 0.0, 0.0,
                   0.005, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0,
                   1, 20, 26)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.n_active_contacts, 20)
        self.assertEqual(self.DUT.amps_per_contact, 0.005)
        self.assertEqual(self.DUT.piK, 1.0)
        self.assertEqual(self.DUT.piP, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestPCB) set_attributes should return a 40 error code when too few items are passed
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
                   0.0, 0.0, 0.0, 0.0,
                   1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0,
                   20)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_type_error(self):
        """
        (TestPCB) set_attributes should return a 10 error code when the wrong type is passed
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
                   0.0, 0.0, 0.0, 0.0,
                   1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0,
                   0, '')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestPCB) get_attributes should return a tuple of attribute values
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
                   0.0, 0.0, 1.0, 0.0, 0, '',
                   0, 26, 0.0, 0.0, 0.0, 0.0, 0.0)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_attribute_sanity(self):
        """
        (TestPCB) get_attributes(set_attributes(values)) == values
        """

        _in_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                      'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                      0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN', 0,
                      'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                      'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                      1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                      0.0, 1.0,
                      0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      1, 0.0, 'Equation', 0.0, 0.0, 0.0, 1, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                      0.0, 0,
                      0, 0, 1, 0.0,
                      0, 0,
                      0.0, 30.0, 0.0, 358.0,
                      0.0, 0.0, 0.0, 0.0,
                      1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                      0.0, 0.0, 0.0, 0.0, 0.0,
                      0, 20, 26)
        _out_values = (0, 32, 'Alt Part #', 'Attachments', 'CAGE Code',
                       'Comp Ref Des', 0.0, 0.0, 0.0, 'Description', 100.0, 0,
                       0, 'Figure #', 50.0, 'LCN', 1, 0, 10.0, 'Name', 'NSN',
                       0, 'Page #', 0, 0, 'Part #', 1, 'Ref Des', 1.0, 0,
                       'Remarks', 0.0, 'Spec #', 0, 30.0, 30.0, 0.0, 2014,
                       1.0, 155.0, -25.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
                       0.0, 1.0,
                       0.0, 1.0, 1.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 1, 0.0, 'Equation', 0.0, 0.0, 0.0, 1, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0,
                       1.0, 0.0, 0.0, 0,
                       0, 0,
                       0.0, 30.0, 0.0, 358.0,
                       0.0, 0.0, 0.0, 0.0, 0, '',
                       20, 26, 1.0, 0.0, 0.0, 0.0, 0.0)

        self.DUT.set_attributes(_in_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _out_values)

    @attr(all=True, unit=True)
    def test_calculate_217_count(self):
        """
<<<<<<< HEAD
        (TestPCB) calculate should return False on success when calculating MIL-HDBK-217F parts count results
=======
        (TestPCB) calculate_part should return False on success when calculating MIL-HDBK-217F parts count results
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
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'], 0.1)
        self.assertEqual(self.DUT.hazard_rate_model['piQ'], 1.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 1.0E-7)

    @attr(all=True, unit=True)
    def test_calculate_217_stress(self):
        """
<<<<<<< HEAD
        (TestPCB) calculate should return False on success when calculating MIL-HDBK-217F parts stress results
=======
        (TestPCB) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.n_active_contacts = 20
        self.DUT.mate_unmate_cycles = 10.0

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

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
<<<<<<< HEAD
        (TestPCB) calculate should return False on success when calculating MIL-HDBK-217F parts stress results with no active contacts
=======
        (TestPCB) calculate_part should return False on success when calculating MIL-HDBK-217F parts stress results with no active contacts
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        self.DUT.environment_active = 2
        self.DUT.hazard_rate_type = 2
        self.DUT.quality = 1

        self.DUT.n_active_contacts = 1
        self.DUT.mate_unmate_cycles = 10.0

<<<<<<< HEAD
        self.assertFalse(self.DUT.calculate())
=======
        self.assertFalse(self.DUT.calculate_part())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.assertEqual(self.DUT.hazard_rate_model['equation'],
                         'lambdab * piE * piK * piP')
        self.assertAlmostEqual(self.DUT.hazard_rate_model['lambdab'],
                               0.0002844941)
        self.assertEqual(self.DUT.hazard_rate_model['piE'], 3.0)
        self.assertEqual(self.DUT.hazard_rate_model['piK'], 3.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_model['piP'], 0.0)
        self.assertAlmostEqual(self.DUT.hazard_rate_active, 0.0)
