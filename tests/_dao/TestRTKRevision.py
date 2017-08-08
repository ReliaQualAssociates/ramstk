#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKRevision.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing the RTKRevision module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(dirname(__file__)))) + "/rtk")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from dao.RTKRevision import RTKRevision

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKRevision(unittest.TestCase):
    """
    Class for testing the RTKRevision class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKRevision class.
        """

        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKRevision).first()
        self.DUT.name = 'Test Revision'

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkrevision_create(self):
        """
        (TestRTKRevision) __init__ should create an RTKRevision model
        """

        self.assertTrue(isinstance(self.DUT, RTKRevision))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_revision')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.availability_logistics, 1.0)
        self.assertEqual(self.DUT.availability_mission, 1.0)
        self.assertEqual(self.DUT.cost, 0.0)
        self.assertEqual(self.DUT.cost_failure, 0.0)
        self.assertEqual(self.DUT.cost_hour, 0.0)
        self.assertEqual(self.DUT.hazard_rate_active, 0.0)
        self.assertEqual(self.DUT.hazard_rate_dormant, 0.0)
        self.assertEqual(self.DUT.hazard_rate_logistics, 0.0)
        self.assertEqual(self.DUT.hazard_rate_mission, 0.0)
        self.assertEqual(self.DUT.hazard_rate_software, 0.0)
        self.assertEqual(self.DUT.mmt, 0.0)
        self.assertEqual(self.DUT.mcmt, 0.0)
        self.assertEqual(self.DUT.mpmt, 0.0)
        self.assertEqual(self.DUT.mtbf_logistics, 0.0)
        self.assertEqual(self.DUT.mtbf_mission, 0.0)
        self.assertEqual(self.DUT.mttr, 0.0)
        self.assertEqual(self.DUT.name, 'Test Revision')
        self.assertEqual(self.DUT.reliability_logistics, 1.0)
        self.assertEqual(self.DUT.reliability_mission, 1.0)
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.total_part_count, 1)
        self.assertEqual(self.DUT.revision_code, '')
        self.assertEqual(self.DUT.program_time, 0.0)
        self.assertEqual(self.DUT.program_time_sd, 0.0)
        self.assertEqual(self.DUT.program_cost, 0.0)
        self.assertEqual(self.DUT.program_cost_sd, 0.0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKRevision) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (1, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'Test Revision', 1.0,
                          1.0, '', 1, '', 0.0, 0.0, 0.0, 0.0))

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKRevision) set_attributes should return a zero error code on success
        """

        _attributes = (0.986, 0.999, 113.25, 1.38, 0.15, 0.000001523,
                       0.0000001523, 0.0000016753, 0.000001018, 0.00000852,
                       32.8, 2.3, 1.8, 59690.8, 982318.3, 12.6,
                       'Revision Name', 0.988, 0.9999, 'Remarks', 12, '-',
                       5688.6, 26812.0, 186238, 255487369.5)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKRevision {0:d} " \
                               "attributes.".format(self.DUT.revision_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKRevision) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0.986, 0.999, 113.25, None, 0.15, 0.000001523,
                       0.0000001523, None, 0.000001018, 0.00000852,
                       32.8, 2.3, 1.8, 59690.8, 982318.3, 12.6,
                       'Revision Name', 0.988, 0.9999, 'Remarks', 12, '-',
                       5688.6, 26812.0, 186238, 255487369.5)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKRevision " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKRevision) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0.986, 0.999, 113.25, 1.38, 0.15, 0.000001523,
                       0.0000001523, 0.0000016753, 0.000001018, 0.00000852,
                       32.8, 2.3, 1.8, 59690.8, 982318.3, 12.6,
                       'Revision Name', 0.988, 0.9999, 'Remarks', 12, '-',
                       5688.6, 26812.0, 186238)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKRevision.set_attributes().")

