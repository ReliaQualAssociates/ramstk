#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKReliability.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKReliability module algorithms and models."""

import sys
from os.path import dirname

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from nose.plugins.attrib import attr

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

from dao.RTKReliability import RTKReliability

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKReliability(unittest.TestCase):
    """Class for testing the RTKReliability class."""

    _attributes = {
        'hazard_rate_percent': 0.0,
        'reliability_mission': 1.0,
        'reliability_goal_measure_id': 0,
        'hazard_rate_specified': 0.0,
        'hazard_rate_active': 0.0,
        'hr_mission_variance': 0.0,
        'reliability_goal': 0.0,
        'mtbf_log_variance': 0.0,
        'quality_id': 0,
        'scale_parameter': 0.0,
        'add_adj_factor': 0.0,
        'availability_mission': 1.0,
        'mtbf_spec_variance': 0.0,
        'mtbf_miss_variance': 0.0,
        'lambda_b': 0.0,
        'hr_specified_variance': 0.0,
        'avail_log_variance': 0.0,
        'hazard_rate_type_id': 0,
        'mtbf_mission': 0.0,
        'failure_distribution_id': 0,
        'reliability_miss_variance': 0.0,
        'avail_mis_variance': 0.0,
        'hazard_rate_method_id': 0,
        'hazard_rate_mission': 0.0,
        'hazard_rate_software': 0.0,
        'mtbf_specified': 0.0,
        'hr_logistics_variance': 0.0,
        'shape_parameter': 0.0,
        'hardware_id': 1,
        'hr_dormant_variance': 0.0,
        'location_parameter': 0.0,
        'survival_analysis_id': 0,
        'hazard_rate_logistics': 0.0,
        'reliability_logistics': 1.0,
        'hazard_rate_model': 'Test HR Model',
        'reliability_log_variance': 0.0,
        'hr_active_variance': 0.0,
        'availability_logistics': 1.0,
        'hazard_rate_dormant': 0.0,
        'mtbf_logistics': 0.0,
        'mult_adj_factor': 1.0
    }

    def setUp(self):
        """(TestRTKReliability) Set up the test fixture for the RTKReliability class."""
        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKReliability).first()
        self.DUT.hazard_rate_model = self._attributes['hazard_rate_model']

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkreliability_create(self):
        """(TestRTKReliability) __init__ should create an RTKReliability model."""
        self.assertTrue(isinstance(self.DUT, RTKReliability))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_reliability')
        self.assertEqual(self.DUT.hardware_id, 1)
        self.assertEqual(self.DUT.add_adj_factor, 0.0)
        self.assertEqual(self.DUT.availability_logistics, 1.0)
        self.assertEqual(self.DUT.availability_mission, 1.0)
        self.assertEqual(self.DUT.avail_log_variance, 0.0)
        self.assertEqual(self.DUT.avail_mis_variance, 0.0)
        self.assertEqual(self.DUT.failure_distribution_id, 0)
        self.assertEqual(self.DUT.hazard_rate_active, 0.0)
        self.assertEqual(self.DUT.hazard_rate_dormant, 0.0)
        self.assertEqual(self.DUT.hazard_rate_logistics, 0.0)
        self.assertEqual(self.DUT.hazard_rate_method_id, 0)
        self.assertEqual(self.DUT.hazard_rate_mission, 0.0)
        self.assertEqual(self.DUT.hazard_rate_model, 'Test HR Model')
        self.assertEqual(self.DUT.hazard_rate_percent, 0.0)
        self.assertEqual(self.DUT.hazard_rate_software, 0.0)
        self.assertEqual(self.DUT.hazard_rate_specified, 0.0)
        self.assertEqual(self.DUT.hazard_rate_type_id, 0)
        self.assertEqual(self.DUT.hr_active_variance, 0.0)
        self.assertEqual(self.DUT.hr_dormant_variance, 0.0)
        self.assertEqual(self.DUT.hr_logistics_variance, 0.0)
        self.assertEqual(self.DUT.hr_mission_variance, 0.0)
        self.assertEqual(self.DUT.hr_specified_variance, 0.0)
        self.assertEqual(self.DUT.location_parameter, 0.0)
        self.assertEqual(self.DUT.mtbf_logistics, 0.0)
        self.assertEqual(self.DUT.mtbf_mission, 0.0)
        self.assertEqual(self.DUT.mtbf_specified, 0.0)
        self.assertEqual(self.DUT.mtbf_log_variance, 0.0)
        self.assertEqual(self.DUT.mtbf_miss_variance, 0.0)
        self.assertEqual(self.DUT.mtbf_spec_variance, 0.0)
        self.assertEqual(self.DUT.mult_adj_factor, 1.0)
        self.assertEqual(self.DUT.quality_id, 0)
        self.assertEqual(self.DUT.reliability_goal, 0.0)
        self.assertEqual(self.DUT.reliability_goal_measure_id, 0)
        self.assertEqual(self.DUT.reliability_logistics, 1.0)
        self.assertEqual(self.DUT.reliability_mission, 1.0)
        self.assertEqual(self.DUT.reliability_log_variance, 0.0)
        self.assertEqual(self.DUT.reliability_miss_variance, 0.0)
        self.assertEqual(self.DUT.scale_parameter, 0.0)
        self.assertEqual(self.DUT.shape_parameter, 0.0)
        self.assertEqual(self.DUT.survival_analysis_id, 0)
        self.assertEqual(self.DUT.lambda_b, 0.0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """(TestRTKReliability) get_attributes should return a dict of attribute key:value pairs."""
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """(TestRTKReliability) set_attributes should return a zero error code on success."""
        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKReliability {0:d} "
                         "attributes.".format(self.DUT.hardware_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_missing_key(self):
        """(TestRTKReliability) set_attributes should return a 40 error code when passed a dict with a missing key."""
        self._attributes.pop('shape_parameter')

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Missing attribute "
                         "'shape_parameter' in attribute dictionary "
                         "passed to RTKReliability.set_attributes().")

        self._attributes['shape_parameter'] = 0.0
