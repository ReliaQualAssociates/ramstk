#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKIncidentAction.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKIncidentAction module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from datetime import date, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKIncidentAction import RTKIncidentAction

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKIncidentAction(unittest.TestCase):
    """
    Class for testing the RTKIncidentAction class.
    """

    _attributes = (1, 1, 0, 'Test Prescribed Action', '', 0, 0,
                   date.today() + timedelta(days=30), 0, 0,
                   date.today() + timedelta(days=30),
                   date.today() + timedelta(days=30), 0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKIncidentAction class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKIncidentAction).first()
        self.DUT.action_prescribed = self._attributes[3]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkincidentaction_create(self):
        """
        (TestRTKIncidentAction) __init__ should create an RTKIncidentAction model.
        """

        self.assertTrue(isinstance(self.DUT, RTKIncidentAction))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_incident_action')
        self.assertEqual(self.DUT.incident_id, 1)
        self.assertEqual(self.DUT.action_id, 1)
        self.assertEqual(self.DUT.action_owner, 0)
        self.assertEqual(self.DUT.action_prescribed, 'Test Prescribed Action')
        self.assertEqual(self.DUT.action_taken, '')
        self.assertEqual(self.DUT.approved, 0)
        self.assertEqual(self.DUT.approved_by, 0)
        self.assertEqual(self.DUT.approved_date,
                         date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.closed, 0)
        self.assertEqual(self.DUT.closed_by, 0)
        self.assertEqual(self.DUT.closed_date,
                         date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.due_date, date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.status_id, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKIncidentAction) get_attributes should return a tuple of attribute values.
        """
        print self.DUT.get_attributes()
        print self._attributes
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKIncidentAction) set_attributes should return a zero error code on success
        """

        _attributes = (0, 'Test Prescribed Action', '', 0, 0,
                       date.today() + timedelta(days=30), 0, 0,
                       date.today() + timedelta(days=30),
                       date.today() + timedelta(days=30), 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKIncidentAction " \
                               "{0:d} attributes.".format(self.DUT.action_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKIncidentAction) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0, 'Test Prescribed Action', '', 'zero', 0,
                       date.today() + timedelta(days=30), 0, 0,
                       date.today() + timedelta(days=30),
                       date.today() + timedelta(days=30), 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKIncidentAction " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKIncidentAction) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0, 'Test Prescribed Action', '', 0, 0,
                       date.today() + timedelta(days=30), 0, 0,
                       date.today() + timedelta(days=30),
                       date.today() + timedelta(days=30))

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKIncidentAction.set_attributes().")
