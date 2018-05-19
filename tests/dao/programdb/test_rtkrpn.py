#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKRPN.py is part of The RTK Project

#
# All rights reserved.
"""
This is the test class for testing the RTKRPN module algorithms and
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

from dao.RTKRPN import RTKRPN

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKRPN(unittest.TestCase):
    """
    Class for testing the RTKRPN class.
    """

    attributes = (1, 'None', 'No effect.', 'severity', 1)

    def setUp(self):
        """
        Sets up the test fixture for the RTKRPN class.
        """

        engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKRPN).first()
        self.DUT.name = self.attributes[1]
        self.DUT.description = self.attributes[2]
        self.DUT.rpn_type = self.attributes[3]
        self.DUT.value = self.attributes[4]

        session.commit()

    @attr(all=True, unit=True)
    def test00_RTKRPN_create(self):
        """
        (TestRTKRPN) __init__ should create an RTKRPN model
        """

        self.assertTrue(isinstance(self.DUT, RTKRPN))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_rpn')
        self.assertEqual(self.DUT.rpn_id, 1)
        self.assertEqual(self.DUT.description, 'No effect.')
        self.assertEqual(self.DUT.name, 'None')
        self.assertEqual(self.DUT.rpn_type, 'severity')
        self.assertEqual(self.DUT.value, 1)

    @attr(all=True, unit=True)
    def test01_RTKRPN_get_attributes(self):
        """
        (TestRTKRPN) get_attributes should return a tuple of attributes values on success
        """

        self.assertEqual(self.DUT.get_attributes(), self.attributes)

    @attr(all=True, unit=True)
    def test02a_RTKRPN_set_attributes(self):
        """
        (TestRTKRPN) set_attributes should return a zero error code on success
        """

        _attributes = ('Very High',
                       'System inoperable with destructive failure without ' \
                       'compromising safety.', 'severity', 8)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKRPN {0:d} " \
                               "attributes.".format(self.DUT.rpn_id))

    @attr(all=True, unit=True)
    def test02b_RTKRPN_set_attributes_to_few(self):
        """
        (TestRTKRPN) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Very High',
                       'System inoperable with destructive failure without ' \
                       'compromising safety.', 'severity')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKRPN.set_attributes().")

    @attr(all=True, unit=True)
    def test02c_RTKRPN_set_attributes_wrong_type(self):
        """
        (TestRTKRPN) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('Very High',
                       'System inoperable with destructive failure without ' \
                       'compromising safety.', 'severity', 'eight')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKRPN " \
                               "attributes.")
