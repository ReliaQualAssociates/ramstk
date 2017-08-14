#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKManufacturer.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKManufacturer module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKManufacturer import RTKManufacturer

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKManufacturer(unittest.TestCase):
    """
    Class for testing the RTKManufacturer class.
    """

    attributes = (1, 'Sprague','New Hampshire','13606')

    def setUp(self):
        """
        Sets up the test fixture for the RTKManufacturer class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKManufacturer).first()
        self.DUT.description = self.attributes[1]
        self.DUT.location = self.attributes[2]
        self.DUT.cage_code = self.attributes[3]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKManufacturer_create(self):
        """
        (TestRTKManufacturer) __init__ should create an RTKManufacturer model
        """

        self.assertTrue(isinstance(self.DUT, RTKManufacturer))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_manufacturer')
        self.assertEqual(self.DUT.manufacturer_id, 1)
        self.assertEqual(self.DUT.description, 'Sprague')
        self.assertEqual(self.DUT.location, 'New Hampshire')
        self.assertEqual(self.DUT.cage_code, '13606')

    @attr(all=True, unit=True)
    def test01_RTKManufacturer_get_attributes(self):
        """
        (TestRTKManufacturer) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKManufacturer_set_attributes(self):
        """
        (TestRTKManufacturer) set_attributes should return a zero error code on success
        """

        _attributes = ('National Semiconductor', 'California', '27014')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKManufacturer {0:d} " \
                               "attributes.".format(self.DUT.manufacturer_id))

    @attr(all=True, unit=True)
    def test02b_RTKManufacturers_set_attributes_to_few(self):
        """
        (TestRTKManufacturers) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('National Semiconductor', 'California',)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKManufacturer.set_attributes().")