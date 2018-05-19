#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKUser.py is part of The RTK Project

#
# All rights reserved.
"""
This is the test class for testing the RTKUser module algorithms and
models.
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

from dao.DAO import DAO
from dao.RTKUser import RTKUser

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKUser(unittest.TestCase):
    """
    Class for testing the RTKUser class.
    """

    attributes = (1, 'Culpepper', 'Samual', 'sculpepper@rebelcause.gov',
                  '555.555.5555', '1:10')

    def setUp(self):
        """
        Sets up the test fixture for the RTKUser class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKUser).first()
        self.DUT.user_lname = self.attributes[1]
        self.DUT.user_fname = self.attributes[2]
        self.DUT.user_email = self.attributes[3]
        self.DUT.user_phone = self.attributes[4]
        self.DUT.user_group_id = self.attributes[5]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkuser_create(self):
        """
        (TestRTKUser) __init__ should create an RTKUser model
        """

        self.assertTrue(isinstance(self.DUT, RTKUser))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_user')
        self.assertEqual(self.DUT.user_id, 1)
        self.assertEqual(self.DUT.user_lname, 'Culpepper')
        self.assertEqual(self.DUT.user_fname, 'Samual')
        self.assertEqual(self.DUT.user_email, 'sculpepper@rebelcause.gov')
        self.assertEqual(self.DUT.user_phone, '555.555.5555')
        self.assertEqual(self.DUT.user_group_id, '1:10')

    @attr(all=True, unit=True)
    def test01_rtkuser_get_attributes(self):
        """
        (TestRTKUser) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_rtk_user_set_attributes(self):
        """
        (TestRTKUser) set_attributes should return a zero error code on success
        """

        _attributes = ('Smith', 'John', 'jsmith@rebelcause.gov',
                       '555.616.1234', '1:10:12')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKUser {0:d} " \
                               "attributes.".format(    self.DUT.user_id))

    @attr(all=True, unit=True)
    def test02b_rtk_user_set_attributes_to_few(self):
        """
        (TestRTKUser) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Smith', 'John', 'jsmith@rebelcause.gov',
                       '555.616.1234')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKUser.set_attributes().")
