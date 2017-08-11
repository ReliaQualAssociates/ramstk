#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKSurvival.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKSurvival module algorithms and
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

from dao.RTKSurvival import RTKSurvival

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKSurvival(unittest.TestCase):
    """
    Class for testing the RTKSurvival class.
    """

    _attributes =(1, 1, 1, 'Test Survival Analysis', 0, 0, 75.0, 0, 0, 0, 0.0,
                  0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                  date.today(), date.today() + timedelta(days=30), 0)

    def setUp(self):
        """
        Sets up the test fixture for the RTKSurvival class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKSurvival).first()
        self.DUT.hardware_id = self._attributes[2]
        self.DUT.description = self._attributes[3]

        session.commit()

        @attr(all=True, unit=True)
        def test00_rtksurvival_create(self):
            """
            (TestRTKSurvival) __init__ should create an RTKSurvival model.
            """

            self.assertTrue(isinstance(self.DUT, RTKSurvival))

            # Verify class attributes are properly initialized.
            self.assertEqual(self.DUT.__tablename__, 'rtk_survival')
            self.assertEqual(self.DUT.revision_id, 1)
            self.assertEqual(self.DUT.survival_id, 1)
            self.assertEqual(self.DUT.hardware_id, 0)
            self.assertEqual(self.DUT.description, 'Test Survival Analysis')
            self.assertEqual(self.DUT.source_id, 0)
            self.assertEqual(self.DUT.distribution_id, 0)
            self.assertEqual(self.DUT.confidence, 75.0)
            self.assertEqual(self.DUT.confidence_type_id, 0)
            self.assertEqual(self.DUT.confidence_method_id, 0)
            self.assertEqual(self.DUT.fit_method_id, 0)
            self.assertEqual(self.DUT.rel_time, 0.0)
            self.assertEqual(self.DUT.n_rel_points, 0)
            self.assertEqual(self.DUT.n_suspension, 0)
            self.assertEqual(self.DUT.n_failures, 0)
            self.assertEqual(self.DUT.scale_ll, 0.0)
            self.assertEqual(self.DUT.scale, 0.0)
            self.assertEqual(self.DUT.scale_ul, 0.0)
            self.assertEqual(self.DUT.shape_ll, 0.0)
            self.assertEqual(self.DUT.shape, 0.0)
            self.assertEqual(self.DUT.shape_ul, 0.0)
            self.assertEqual(self.DUT.location_ll, 0.0)
            self.assertEqual(self.DUT.location, 0.0)
            self.assertEqual(self.DUT.location_ul, 0.0)
            self.assertEqual(self.DUT.variance_1, 0.0)
            self.assertEqual(self.DUT.variance_2, 0.0)
            self.assertEqual(self.DUT.variance_3, 0.0)
            self.assertEqual(self.DUT.covariance_1, 0.0)
            self.assertEqual(self.DUT.covariance_2, 0.0)
            self.assertEqual(self.DUT.covariance_3, 0.0)
            self.assertEqual(self.DUT.mhb, 0.0)
            self.assertEqual(self.DUT.lp, 0.0)
            self.assertEqual(self.DUT.lr, 0.0)
            self.assertEqual(self.DUT.aic, 0.0)
            self.assertEqual(self.DUT.bic, 0.0)
            self.assertEqual(self.DUT.mle, 0.0)
            self.assertEqual(self.DUT.start_time, 0.0)
            self.assertEqual(self.DUT.start_date, date.today())
            self.assertEqual(self.DUT.end_date,
                             date.today() + timedelta(days=30))
            self.assertEqual(self.DUT.nevada_chart, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKSurvival) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKSurvival) set_attributes should return a zero error code on success
        """

        _attributes = (1, 'Test Survival Analysis', 0, 0, 75.0, 0, 0, 0, 0.0,
                       0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, date.today(),
                       date.today() + timedelta(days=30), 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKSurvival {0:d} " \
                               "attributes.".format(self.DUT.survival_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKSurvival) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (1, 'Test Survival Analysis', 0, 0, 75.0, 0, 0, 0, 0.0,
                       0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, date.today(),
                       date.today() + timedelta(days=30), 0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKSurvival " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKSurvival) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (1, 'Test Survival Analysis', 0, 0, 75.0, 0, 0, 0, 0.0,
                       0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, date.today(),
                       date.today() + timedelta(days=30))

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKSurvival.set_attributes().")
