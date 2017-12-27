#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKIncidentDetail.py is part of The RTK Project

#
# All rights reserved.
"""
This is the test class for testing the RTKIncidentDetail module algorithms and
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

from dao.RTKIncidentDetail import RTKIncidentDetail

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKIncidentDetail(unittest.TestCase):
    """
    Class for testing the RTKIncidentDetail class.
    """

    _attributes = (1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0.0, 0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKIncidentDetail class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKIncidentDetail).first()
        self.DUT.failure = self._attributes[4]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkincidentdetail_create(self):
        """
        (TestRTKIncidentDetail) __Init__ should create an RTKIncidentDetail model.
        """

        self.assertTrue(isinstance(self.DUT, RTKIncidentDetail))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_incident_detail')
        self.assertEqual(self.DUT.incident_id, 1)
        self.assertEqual(self.DUT.hardware_id, 0)
        self.assertEqual(self.DUT.age_at_incident, 0)
        self.assertEqual(self.DUT.failure, 1)
        self.assertEqual(self.DUT.suspension, 0)
        self.assertEqual(self.DUT.cnd_nff, 0)
        self.assertEqual(self.DUT.occ_fault, 0)
        self.assertEqual(self.DUT.initial_installation, 0)
        self.assertEqual(self.DUT.interval_censored, 0)
        self.assertEqual(self.DUT.use_op_time, 0)
        self.assertEqual(self.DUT.use_cal_time, 0)
        self.assertEqual(self.DUT.ttf, 0.0)
        self.assertEqual(self.DUT.mode_type_id, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKIncidentDetail) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKIncidentDetail) set_attributes should return a zero error code on success
        """

        _attributes = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKIncidentDetail " \
                               "{0:d} attributes.".\
                         format(self.DUT.incident_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKIncidentDetail) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0, 0, 0, 'zero', 0, 0, 0, 0, 0, 0.0, 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKIncidentDetail " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKIncidentDetail) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKIncidentDetail.set_attributes().")
