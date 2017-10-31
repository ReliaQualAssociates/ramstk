#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKEnviron.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKEnviron module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKEnviron import RTKEnviron

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKEnviron(unittest.TestCase):
    """
    Class for testing the RTKEnviron class.
    """

    attributes = (1, 'GF', 'Ground, Fixed', 'active', 2.0, 1.0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKEnviron class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKEnviron).first()
        self.DUT.code = self.attributes[1]
        self.DUT.description = self.attributes[2]
        self.DUT.environ_type = self.attributes[3]
        self.DUT.pi_e = self.attributes[4]
        self.DUT.do = self.attributes[5]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKEnviron_create(self):
        """
        (TestRTKEnviron) __init__ should create an RTKEnviron model
        """

        self.assertTrue(isinstance(self.DUT, RTKEnviron))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_environ')
        self.assertEqual(self.DUT.environ_id, 1)
        self.assertEqual(self.DUT.code, 'GF')
        self.assertEqual(self.DUT.description, 'Ground, Fixed')
        self.assertEqual(self.DUT.environ_type, 'active')
        self.assertEqual(self.DUT.pi_e, 2.0)
        self.assertEqual(self.DUT.do, 1.0)

    @attr(all=True, unit=True)
    def test01_RTKEnviron_get_attributes(self):
        """
        (TestRTKEnviron) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKEnviron_set_attributes(self):
        """
        (TestRTKEnviron) set_attributes should return a zero error code on success
        """

        _attributes = ('GB', 'Ground, Benign', 'active', 0.5, 1.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKEnviron {0:d} " \
                               "attributes.".format(self.DUT.environ_id))

    @attr(all=True, unit=True)
    def test02b_RTKEnvirons_set_attributes_to_few(self):
        """
        (TestRTKEnvirons) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('GB', 'Ground, Benign', 'active')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKEnviron.set_attributes().")
