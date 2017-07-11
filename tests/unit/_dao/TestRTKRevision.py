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
    def test01a_calculate_reliability(self):
        """
        (TestRTKRevision) calculate_reliability should return False on success.
        """

        self.DUT.hazard_rate_active = 0.00000151
        self.DUT.hazard_rate_dormant = 0.0000000152
        self.DUT.hazard_rate_software = 0.0000003
        self.DUT.hazard_rate_mission = 0.000002

        self.assertFalse(self.DUT.calculate_reliability(100.0))
        self.assertAlmostEqual(self.DUT.hazard_rate_logistics, 1.8252e-06)
        self.assertAlmostEqual(self.DUT.mtbf_logistics, 547885.1632698)
        self.assertAlmostEqual(self.DUT.mtbf_mission, 500000.0)
        self.assertAlmostEqual(self.DUT.reliability_logistics, 0.9998175)
        self.assertAlmostEqual(self.DUT.reliability_mission, 0.9998000)

    @attr(all=True, unit=True)
    def test01b_calculate_reliability_divide_by_zero(self):
        """
        (TestRTKRevision) calculate_reliability should return True when attempting to divide by zero.
        """

        self.DUT.hazard_rate_mission = 0.0

        self.assertTrue(self.DUT.calculate_reliability(100.0))

    @attr(all=True, unit=True)
    def test02a_calculate_availability(self):
        """
        (TestRTKRevision) calculate_availability should return False on success.
        """

        self.DUT.mpmt = 0.5
        self.DUT.mcmt = 1.2
        self.DUT.mttr = 5.8
        self.DUT.mmt = 0.85
        self.DUT.mtbf_logistics = 547885.1632698
        self.DUT.mtbf_mission = 500000.0

        self.assertFalse(self.DUT.calculate_availability())
        self.assertAlmostEqual(self.DUT.availability_logistics, 0.9999894)
        self.assertAlmostEqual(self.DUT.availability_mission, 0.9999884)

    @attr(all=True, unit=True)
    def test02b_calculate_availability_divide_by_zero(self):
        """
        (TestRTKRevision) calculate_availability should return True when attempting to divide by zero.
        """

        self.DUT.mttr = 0.0
        self.DUT.mtbf_logistics = 547885.1632698
        self.DUT.mtbf_mission = 0.0

        self.assertTrue(self.DUT.calculate_availability())

    @attr(all=True, unit=True)
    def test03a_calculate_costs(self):
        """
        (TestRTKRevision) calculate_costs should return False on success.
        """

        self.DUT.cost = 1252.78
        self.DUT.hazard_rate_logistics = 1.0 / 547885.1632698

        self.assertFalse(self.DUT.calculate_costs(100.0))
        self.assertAlmostEqual(self.DUT.cost_per_failure, 0.002286574)
        self.assertAlmostEqual(self.DUT.cost_per_hour, 12.5278)

    @attr(all=True, unit=True)
    def test03b_calculate_costs_divide_by_zero(self):
        """
        (TestRTKRevision) calculate_costs should return True when attempting to divide by zero.
        """

        self.DUT.cost = 1252.78
        self.DUT.hazard_rate_logistics = 1.0 / 547885.1632698

        self.assertTrue(self.DUT.calculate_costs(0.0))

    @attr(all=True, unit=True)
    def test04_get_attributes(self):
        """
        (TestRTKRevision) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (1, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'Test Revision', 1.0,
                          1.0, '', 1, '', 0.0, 0.0, 0.0, 0.0))

    @attr(all=True, unit=True)
    def test05a_set_attributes(self):
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
    def test05b_set_attributes_wrong_type(self):
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
    def test05c_set_attributes_too_few_passed(self):
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

