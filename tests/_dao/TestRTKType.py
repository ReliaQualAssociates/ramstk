#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKType.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKType module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKType import RTKType

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKType(unittest.TestCase):
    """
    Class for testing the RTKType class.
    """

    attributes = (1, 'CALC', 'Calculated', 'cost')

    def setUp(self):
        """
        Sets up the test fixture for the RTKType class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKType).first()
        self.DUT.code = self.attributes[1]
        self.DUT.description = self.attributes[2]
        self.DUT.type = self.attributes[3]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKType_create(self):
        """
        (TestRTKType) __init__ should create an RTKType model
        """

        self.assertTrue(isinstance(self.DUT, RTKType))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_type')
        self.assertEqual(self.DUT.type_id, 1)
        self.assertEqual(self.DUT.code, 'CALC')
        self.assertEqual(self.DUT.description, 'Calculated')
        self.assertEqual(self.DUT.type, 'cost')

    @attr(all=True, unit=True)
    def test01_RTKType_get_attributes(self):
        """
        (TestRTKType) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKType_set_attributes(self):
        """
        (TestRTKType) set_attributes should return a zero error code on success
        """

        _attributes = ('DEF', 'Defined', 'cost')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKType {0:d} " \
                               "attributes.".format(self.DUT.type_id))

    @attr(all=True, unit=True)
    def test02b_RTKType_set_attributes_to_few(self):
        """
        (TestRTKType) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('ASS', 'Assessed')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKType.set_attributes().")