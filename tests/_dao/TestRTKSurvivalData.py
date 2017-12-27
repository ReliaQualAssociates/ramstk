#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKSurvivalData.py is part of The RTK Project

#
# All rights reserved.
"""
This is the test class for testing the RTKSurvivalData module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk",
)

from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKSurvivalData import RTKSurvivalData

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKSurvivalData(unittest.TestCase):
    """
    Class for testing the RTKSurvivalData class.
    """

    _attributes = (1, 1, 'Test Survival Record Name', 0,
                   date.today(), 0.0, 0.0, 0, 0, 0.0, 0, 0, date.today(), 0,
                   date.today(), 0, 0.0, 0.0, 0.0, 0, 0, 0, '', '', '')

    def setUp(self):
        """
        Sets up the test fixture for the RTKSurvivalData class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKSurvivalData).first()
        self.DUT.name = self._attributes[2]

        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtksurvivaldata_create(self):
        """
        (TestRTKSurvivalData) __init__ should create an RTKSurvivalData model.
        """

        self.assertTrue(isinstance(self.DUT, RTKSurvivalData))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_survival_data')
        self.assertEqual(self.DUT.survival_id, 1)
        self.assertEqual(self.DUT.record_id, 1)
        self.assertEqual(self.DUT.name, 'Test Survival Record Name')
        self.assertEqual(self.DUT.source_id, 0)
        self.assertEqual(self.DUT.failure_date, date.today())
        self.assertEqual(self.DUT.left_interval, 0.0)
        self.assertEqual(self.DUT.right_interval, 0.0)
        self.assertEqual(self.DUT.status_id, 0)
        self.assertEqual(self.DUT.quantity, 0)
        self.assertEqual(self.DUT.tbf, 0.0)
        self.assertEqual(self.DUT.mode_type_id, 0)
        self.assertEqual(self.DUT.nevada_chart, 0)
        self.assertEqual(self.DUT.ship_date, date.today())
        self.assertEqual(self.DUT.number_shipped, 0)
        self.assertEqual(self.DUT.return_date, date.today())
        self.assertEqual(self.DUT.number_returned, 0)
        self.assertEqual(self.DUT.user_float_1, 0.0)
        self.assertEqual(self.DUT.user_float_2, 0.0)
        self.assertEqual(self.DUT.user_float_3, 0.0)
        self.assertEqual(self.DUT.user_integer_1, 0)
        self.assertEqual(self.DUT.user_integer_2, 0)
        self.assertEqual(self.DUT.user_integer_3, 0)
        self.assertEqual(self.DUT.user_string_1, '')
        self.assertEqual(self.DUT.user_string_2, '')
        self.assertEqual(self.DUT.user_string_3, '')

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKSurvivalData) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKSurvivalData) set_attributes should return a zero error code on success
        """

        _attributes = ('Test Survival Record Name', 0, date.today(), 0.0, 0.0,
                       0, 0, 0.0, 0, 0, date.today(), 0, date.today(), 0, 0.0,
                       0.0, 0.0, 0, 0, 0, '', '', '')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKSurvivalData {0:d} " \
                               "attributes.".format(self.DUT.record_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKSurvivalData) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('Test Survival Record Name', 0, date.today(), 0.0, 0.0,
                       0, 0, 0.0, 0, 0, date.today(), 0, date.today(), 0, 0.0,
                       0.0, 'None', 0, 0, 0, '', '', '')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKSurvivalData " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKSurvivalData) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ('Test Survival Record Name', 0, date.today(), 0.0, 0.0,
                       0, 0, 0.0, 0, 0, date.today(), 0, date.today(), 0, 0.0,
                       0.0, 0.0, 0, 0, 0, '', '')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKSurvivalData.set_attributes().")
