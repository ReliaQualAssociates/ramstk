#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKLevel.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKLevel module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKLevel import RTKLevel

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKLevel(unittest.TestCase):
    """
    Class for testing the RTKLevel class.
    """

    attributes = (1, 'Software System', 'software', 0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKLevel class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKLevel).first()
        self.DUT.description = self.attributes[1]
        self.DUT.type = self.attributes[2]
        self.DUT.value = self.attributes[3]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKLevel_create(self):
        """
        (TestRTKLevel) __init__ should create an RTKLevel model
        """

        self.assertTrue(isinstance(self.DUT, RTKLevel))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_level')
        self.assertEqual(self.DUT.level_id, 1)
        self.assertEqual(self.DUT.description, 'Software System')
        self.assertEqual(self.DUT.type, 'software')
        self.assertEqual(self.DUT.value, 0)

    @attr(all=True, unit=True)
    def test01_RTKLevel_get_attributes(self):
        """
        (TestRTKLevel) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKLevel_set_attributes(self):
        """
        (TestRTKLevel) set_attributes should return a zero error code on success
        """

        _attributes = ('Software Module', 'software', 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKLevel {0:d} " \
                               "attributes.".format(self.DUT.level_id))

    @attr(all=True, unit=True)
    def test02b_RTKLevel_set_attributes_to_few(self):
        """
        (TestRTKLevel) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Software Module', 'software')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKLevel.set_attributes().")

    @attr(all=True, unit=True)
    def test02c_RTKLevel_set_attributes_wrong_type(self):
        """
        (TestRTKLevel) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('Software Module', 'software', 'zero')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKLevel " \
                               "attributes.")