#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKSubCategory.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKSubCategory module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKSubCategory import RTKSubCategory

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKSubCategory(unittest.TestCase):
    """
    Class for testing the RTKSubCategory class.
    """

    attributes = (1, 1, 'Linear')

    def setUp(self):
        """
        Sets up the test fixture for the RTKSubCategory class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKSubCategory).first()
        self.DUT.category_id = self.attributes[0]
        self.DUT.description = self.attributes[2]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKSubCategory_create(self):
        """
        (TestRTKSubCategory) __init__ should create an RTKSubCategory model
        """

        self.assertTrue(isinstance(self.DUT, RTKSubCategory))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_subcategory')
        self.assertEqual(self.DUT.category_id, 1)
        self.assertEqual(self.DUT.subcategory_id, 1)
        self.assertEqual(self.DUT.description, 'Linear')

    @attr(all=True, unit=True)
    def test01_RTKSubCategory_get_attributes(self):
        """
        (TestRTKSubCategory) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKSubCategory_set_attributes(self):
        """
        (TestRTKSubCategory) set_attributes should return a zero error code on success
        """

        _attributes = (1, 'Logic')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKSubCategory {0:d} " \
                               "attributes.".format(self.DUT.subcategory_id))

    @attr(all=True, unit=True)
    def test02b_RTKSubCategory_set_attributes_to_few(self):
        """
        (TestRTKSubCategory) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (1, )

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKSubCategory.set_attributes().")