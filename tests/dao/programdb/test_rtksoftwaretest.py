#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKSoftwareTest.py is part of The RTK
#       Project

#
# All rights reserved.
"""
This is the test class for testing the RTKSoftwareTest module algorithms
and models.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk",
)

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKSoftwareTest import RTKSoftwareTest

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKSoftwareTest(unittest.TestCase):
    """
    Class for testing the RTKSoftwareTest class.
    """

    _attributes = (1, 1, 0, 0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKSoftwareTest class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKSoftwareTest).first()

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtksoftware_create(self):
        """
        (TestRTKSoftwareTest) __init__ should create an RTKSoftwareTest model.
        """

        self.assertTrue(isinstance(self.DUT, RTKSoftwareTest))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_software_test')
        self.assertEqual(self.DUT.software_id, 1)
        self.assertEqual(self.DUT.technique_id, 1)
        self.assertEqual(self.DUT.recommended, 0)
        self.assertEqual(self.DUT.used, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKSoftwareTest) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKSoftwareTest) set_attributes should return a zero error code on success
        """

        _attributes = (0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating " \
                               "RTKSoftwareTest {0:d} " \
                               "attributes.".format(self.DUT.software_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKSoftwareTest) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('one', 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more " \
                               "RTKSoftwareTest attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKSoftwareTest) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0, )

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to " \
                               "RTKSoftwareTest.set_attributes().")
