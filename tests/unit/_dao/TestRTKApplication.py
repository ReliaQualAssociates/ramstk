#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKApplication.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKApplication module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from dao.DAO import DAO
from dao.RTKApplication import RTKApplication

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKApplication(unittest.TestCase):
    """
    Class for testing the RTKApplication class.
    """

    attributes = (1, 'Airborne', 0.0128, 6.28)

    def setUp(self):
        """
        Sets up the test fixture for the RTKApplication class.
        """

        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestCommonDB.rtk')

        self.DUT = self.dao.session.query(RTKApplication).first()
        self.DUT.description = self.attributes[1]
        self.DUT.fault_density = self.attributes[2]
        self.DUT.transformation_ratio = self.attributes[3]

        self.dao.db_update()

    @attr(all=True, unit=True)
    def test00_RTKApplication_create(self):
        """
        (TestRTKApplication) __init__ should create an RTKApplication model
        """

        self.assertTrue(isinstance(self.DUT, RTKApplication))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_application')
        self.assertEqual(self.DUT.application_id, 1)
        self.assertEqual(self.DUT.description, 'Airborne')
        self.assertEqual(self.DUT.fault_density, 0.0128)
        self.assertEqual(self.DUT.transformation_ratio, 6.28)

    @attr(all=True, unit=True)
    def test01_RTKApplication_get_attributes(self):
        """
        (TestRTKApplication) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKApplication_set_attributes(self):
        """
        (TestRTKApplication) set_attributes should return a zero error code on success
        """

        _attributes = ('Developmental', 0.0123, 132.6)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKApplication {0:d} " \
                               "attributes.".format(self.DUT.application_id))

    @attr(all=True, unit=True)
    def test02b_RTKApplication_set_attributes_to_few(self):
        """
        (TestRTKApplication) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Developmental', 0.0123)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKApplication.set_attributes().")

    @attr(all=True, unit=True)
    def test02c_RTKApplication_set_attributes_wrong_type(self):
        """
        (TestRTKApplication) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('Developmental', 0.0123, 'big number')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKApplication " \
                               "attributes.")