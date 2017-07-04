#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKCategory.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKCategory module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKCategory import RTKCategory

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKCategory(unittest.TestCase):
    """
    Class for testing the RTKCategory class.
    """

    attributes = (1, 'IC', 'Integrated Circuit', 'hardware', 1)

    def setUp(self):
        """
        Sets up the test fixture for the RTKCategory class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKCategory).first()
        self.DUT.name = self.attributes[1]
        self.DUT.description = self.attributes[2]
        self.DUT.type = self.attributes[3]
        self.DUT.value = self.attributes[4]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKCategory_create(self):
        """
        (TestRTKCategory) __init__ should create an RTKCategory model
        """

        self.assertTrue(isinstance(self.DUT, RTKCategory))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_category')
        self.assertEqual(self.DUT.category_id, 1)
        self.assertEqual(self.DUT.name, 'IC')
        self.assertEqual(self.DUT.description, 'Integrated Circuit')
        self.assertEqual(self.DUT.type, 'hardware')
        self.assertEqual(self.DUT.value, 1)

    @attr(all=True, unit=True)
    def test01_RTKCategory_get_attributes(self):
        """
        (TestRTKCategory) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKCategory_set_attributes(self):
        """
        (TestRTKCategory) set_attributes should return a zero error code on success
        """

        _attributes = ('SEMI', 'Semiconductor', 'hardware', 1)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKCategory {0:d} " \
                               "attributes.".format(self.DUT.category_id))

    @attr(all=True, unit=True)
    def test02b_RTKCategory_set_attributes_to_few(self):
        """
        (TestRTKCategory) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('ASS', 'Assessed')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKCategory.set_attributes().")