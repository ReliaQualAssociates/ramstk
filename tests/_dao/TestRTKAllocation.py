#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKAllocation.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKAllocation module algorithms and
models.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKAllocation import RTKAllocation

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKAllocation(unittest.TestCase):
    """
    Class for testing the RTKAllocation class.
    """

    _attributes =(1, 0.0, 10, 1, 0.0, 0.0, 1, 1, 1, 0.0, 0.0, 1, 1, 1, 0.0,
                  0.0, 1.0, 1, 1, 1)

    def setUp(self):
        """
        Sets up the test fixture for the RTKAllocation class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKAllocation).first()
        self.DUT.env_factor = self._attributes[2]

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkallocation_create(self):
        """
        (TestRTKAllocation) __init__ should create an RTKAllocation model.
        """

        self.assertTrue(isinstance(self.DUT, RTKAllocation))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_allocation')
        self.assertEqual(self.DUT.hardware_id, 1)
        self.assertEqual(self.DUT.availability_alloc, 0.0)
        self.assertEqual(self.DUT.env_factor, 10)
        self.assertEqual(self.DUT.goal_measure_id, 1)
        self.assertEqual(self.DUT.hazard_rate_alloc, 0.0)
        self.assertEqual(self.DUT.hazard_rate_goal, 0.0)
        self.assertEqual(self.DUT.included, 1)
        self.assertEqual(self.DUT.int_factor, 1)
        self.assertEqual(self.DUT.method_id, 1)
        self.assertEqual(self.DUT.mtbf_alloc, 0.0)
        self.assertEqual(self.DUT.mtbf_goal, 0.0)
        self.assertEqual(self.DUT.n_sub_systems, 1)
        self.assertEqual(self.DUT.n_sub_elements, 1)
        self.assertEqual(self.DUT.parent_id, 1)
        self.assertEqual(self.DUT.percent_weight_factor, 0.0)
        self.assertEqual(self.DUT.reliability_alloc, 0.0)
        self.assertEqual(self.DUT.reliability_goal, 1.0)
        self.assertEqual(self.DUT.op_time_factor, 1)
        self.assertEqual(self.DUT.soa_factor, 1)
        self.assertEqual(self.DUT.weight_factor, 1)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKAllocation) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKAllocation) set_attributes should return a zero error code on success
        """

        _attributes = (0.0, 10, 1, 0.0, 0.0, 1, 1, 1, 0.0, 0.0, 1, 1, 1, 0.0,
                       0.0, 1.0, 1, 1, 1)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKAllocation {0:d} " \
                               "attributes.".format(self.DUT.hardware_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKAllocation) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0.0, 10, 1, 0.0, 'None', 1, 1, 1, 0.0, 0.0, 1, 1, 1,
                       0.0, 0.0, 1.0, 1, 1, 1)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKAllocation " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKAllocation) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0.0, 10, 1, 0.0, 0.0, 1, 1, 1, 0.0, 0.0, 1, 1, 1, 0.0,
                       0.0, 1.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKAllocation.set_attributes().")
