#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKUnit.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKUnit module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKUnit import RTKUnit

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKUnit(unittest.TestCase):
    """
    Class for testing the RTKUnit class.
    """

    attributes = (1, 'lbf','Pounds Force','measurement')

    def setUp(self):
        """
        Sets up the test fixture for the RTKUnit class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKUnit).first()
        self.DUT.code = self.attributes[1]
        self.DUT.description = self.attributes[2]
        self.DUT.type = self.attributes[3]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKUnit_create(self):
        """
        (TestRTKUnit) __init__ should create an RTKUnit model
        """

        self.assertTrue(isinstance(self.DUT, RTKUnit))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_unit')
        self.assertEqual(self.DUT.unit_id, 1)
        self.assertEqual(self.DUT.description, 'Pounds Force')
        self.assertEqual(self.DUT.code, 'lbf')
        self.assertEqual(self.DUT.type, 'measurement')

    @attr(all=True, unit=True)
    def test01_RTKUnit_get_attributes(self):
        """
        (TestRTKUnit) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKUnit_set_attributes(self):
        """
        (TestRTKUnit) set_attributes should return a zero error code on success
        """

        _attributes = ('N', 'Newtons', 'measurement')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKUnit {0:d} " \
                               "attributes.".format(self.DUT.unit_id))

    @attr(all=True, unit=True)
    def test02b_RTKUnits_set_attributes_to_few(self):
        """
        (TestRTKUnits) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('N', 'Newtons',)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKUnit.set_attributes().")