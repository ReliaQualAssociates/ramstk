#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRAMSTKIncidentAction.py is part of The RAMSTK Project

#
# All rights reserved.
"""
This is the test class for testing the RAMSTKIncidentAction module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/ramstk",
)

from datetime import date, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RAMSTKIncidentAction import RAMSTKIncidentAction

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'


class TestRAMSTKIncidentAction(unittest.TestCase):
    """
    Class for testing the RAMSTKIncidentAction class.
    """

    _attributes = (1, 1, 0, 'Test Prescribed Action',
                   '', 0, 0, date.today() + timedelta(days=30), 0, 0,
                   date.today() + timedelta(days=30),
                   date.today() + timedelta(days=30), 0)

    def setUp(self):
        """
        Sets up the test fixture for the RAMSTKIncidentAction class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.ramstk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RAMSTKIncidentAction).first()
        self.DUT.action_prescribed = self._attributes[3]

        session.commit()

    @attr(all=True, unit=True)
    def test00_ramstkincidentaction_create(self):
        """
        (TestRAMSTKIncidentAction) __init__ should create an RAMSTKIncidentAction model.
        """

        self.assertTrue(isinstance(self.DUT, RAMSTKIncidentAction))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'ramstk_incident_action')
        self.assertEqual(self.DUT.incident_id, 1)
        self.assertEqual(self.DUT.action_id, 1)
        self.assertEqual(self.DUT.action_owner, 0)
        self.assertEqual(self.DUT.action_prescribed, 'Test Prescribed Action')
        self.assertEqual(self.DUT.action_taken, '')
        self.assertEqual(self.DUT.approved, 0)
        self.assertEqual(self.DUT.approved_by, 0)
        self.assertEqual(
            self.DUT.approved_date, date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.closed, 0)
        self.assertEqual(self.DUT.closed_by, 0)
        self.assertEqual(
            self.DUT.closed_date, date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.due_date, date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.status_id, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRAMSTKIncidentAction) get_attributes should return a tuple of attribute values.
        """
        print self.DUT.get_attributes()
        print self._attributes
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRAMSTKIncidentAction) set_attributes should return a zero error code on success
        """

        _attributes = (0, 'Test Prescribed Action', '',
                       0, 0, date.today() + timedelta(days=30), 0, 0,
                       date.today() + timedelta(days=30),
                       date.today() + timedelta(days=30), 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RAMSTK SUCCESS: Updating RAMSTKIncidentAction " \
                               "{0:d} attributes.".format(self.DUT.action_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRAMSTKIncidentAction) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0, 'Test Prescribed Action', '',
                       'zero', 0, date.today() + timedelta(days=30), 0, 0,
                       date.today() + timedelta(days=30),
                       date.today() + timedelta(days=30), 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RAMSTK ERROR: Incorrect data type when " \
                               "converting one or more RAMSTKIncidentAction " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRAMSTKIncidentAction) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0, 'Test Prescribed Action', '',
                       0, 0, date.today() + timedelta(days=30), 0, 0,
                       date.today() + timedelta(days=30),
                       date.today() + timedelta(days=30))

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RAMSTK ERROR: Insufficient number of input " \
                               "values to RAMSTKIncidentAction.set_attributes().")
