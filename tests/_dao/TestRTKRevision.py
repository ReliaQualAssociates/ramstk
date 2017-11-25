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

sys.path.insert(
    0,
    dirname(dirname(dirname(dirname(__file__)))) + "/rtk", )

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

    _attributes = {
        'revision_id': 1,
        'availability_logistics': 0.985,
        'availability_mission': 0.993,
        'cost': 10.86,
        'cost_per_failure': 0.00068,
        'cost_per_hour': 0.000074,
        'hazard_rate_active': 0.00052,
        'hazard_rate_dormant': 0.000052,
        'hazard_rate_logistics': 0.000572,
        'hazard_rate_mission': 0.00049,
        'hazard_rate_software': 0.0000,
        'mmt': 1.8,
        'mcmt': 1.13,
        'mpmt': 2.21,
        'mtbf_logistics': 0.0,
        'mtbf_mission': 0.0,
        'mttr': 0.84,
        'name': 'Initial revision',
        'reliability_logistics': 0.988,
        'reliability_mission': 0.995,
        'remarks': 'Some remarks',
        'n_parts': 138,
        'revision_code': '-',
        'program_time': 1283.6,
        'program_time_sd': 22.4,
        'program_cost': 34286.00,
        'program_cost_sd': 332.7
    }

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
        (TestRTKRevision) get_attributes should return a dict of {attr name:attr value} pairs.
        """

        _attributes = {
            'revision_id': 1,
            'availability_logistics': 1.0,
            'availability_mission': 1.0,
            'cost': 0.0,
            'cost_per_failure': 0.0,
            'cost_per_hour': 0.0,
            'hazard_rate_active': 0.0,
            'hazard_rate_dormant': 0.0,
            'hazard_rate_logistics': 0.0,
            'hazard_rate_mission': 0.0,
            'hazard_rate_software': 0.0,
            'mmt': 0.0,
            'mcmt': 0.0,
            'mpmt': 0.0,
            'mtbf_logistics': 0.0,
            'mtbf_mission': 0.0,
            'mttr': 0.0,
            'name': '',
            'reliability_logistics': 1.0,
            'reliability_mission': 1.0,
            'remarks': '',
            'n_parts': 0,
            'revision_code': '',
            'program_time': 0.0,
            'program_time_sd': 0.0,
            'program_cost': 0.0,
            'program_cost_sd': 0.0
        }

        _values = self.DUT.get_attributes()

        self.assertEqual(_values['availability_logistics'],
                         _attributes['availability_logistics'])

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKRevision) set_attributes should return a zero error code on success
        """

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKRevision {0:d} " \
                               "attributes.".format(self.DUT.revision_id))

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKRevision) set_attributes should return a 40 error code when passed an attribute dict with a missing key
        """

        self._attributes.pop('name')

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Missing attribute 'name' in " \
                               "attribute dictionary passed to " \
                               "RTKRevision.set_attributes().")

    @attr(all=True, unit=True)
    def test03a_calculate_hazard_rate(self):
        """
        (TestRTKRevision) calculate_hazard_rate should return a zero error code on success.
        """

        self.DUT.hazard_rate_active = 0.00000151
        self.DUT.hazard_rate_dormant = 0.0000000152
        self.DUT.hazard_rate_software = 0.0000003
        self.DUT.hazard_rate_mission = 0.000002

        _error_code, _msg = self.DUT.calculate_hazard_rate()
        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Calculating hazard rates for '
                         'Revision ID 1.')
        self.assertAlmostEqual(self.DUT.hazard_rate_logistics, 1.8252e-06)

    @attr(all=True, unit=True)
    def test03b_calculate_mtbf(self):
        """
        (TestRTKRevision) calculate_mtbf should return a zero error code on success.
        """

        self.DUT.hazard_rate_active = 0.00000151
        self.DUT.hazard_rate_dormant = 0.0000000152
        self.DUT.hazard_rate_software = 0.0000003
        self.DUT.hazard_rate_mission = 0.000002
        self.DUT.calculate_hazard_rate()

        _error_code, _msg = self.DUT.calculate_mtbf()
        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Calculating MTBFs for Revision ID 1.')
        self.assertAlmostEqual(self.DUT.mtbf_logistics, 547885.1632698)
        self.assertAlmostEqual(self.DUT.mtbf_mission, 500000.0)

    @attr(all=True, unit=True)
    def test03c_calculate_reliability(self):
        """
        (TestRTKRevision) calculate_reliability should return a zero error code on success.
        """

        self.DUT.hazard_rate_active = 0.00000151
        self.DUT.hazard_rate_dormant = 0.0000000152
        self.DUT.hazard_rate_software = 0.0000003
        self.DUT.hazard_rate_mission = 0.000002
        self.DUT.calculate_hazard_rate()

        _error_code, _msg = self.DUT.calculate_reliability(100.0, 1.0)
        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Calculating reliabilities for ' \
                               'Revision ID 1.')
        self.assertAlmostEqual(self.DUT.reliability_logistics, 0.9998175)
        self.assertAlmostEqual(self.DUT.reliability_mission, 0.9998000)

    @attr(all=True, unit=True)
    def test04a_calculate_availability(self):
        """
        (TestRTKRevision) calculate_availability should return a zero error code on success.
        """

        self.DUT.mpmt = 0.5
        self.DUT.mcmt = 1.2
        self.DUT.mttr = 5.8
        self.DUT.mmt = 0.85
        self.DUT.mtbf_logistics = 547885.1632698
        self.DUT.mtbf_mission = 500000.0

        _error_code, _msg = self.DUT.calculate_availability()
        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Calculating availability ' \
                               'metrics for Revision ID 1.')
        self.assertAlmostEqual(self.DUT.availability_logistics, 0.9999894)
        self.assertAlmostEqual(self.DUT.availability_mission, 0.9999884)

    @attr(all=True, unit=True)
    def test04b_calculate_availability_divide_by_zero(self):
        """
        (TestRTKRevision) calculate_availability should return a non-zero error code when attempting to divide by zero.
        """

        self.DUT.mttr = 0.0
        self.DUT.mtbf_logistics = 547885.1632698
        self.DUT.mtbf_mission = 0.0

        _error_code, _msg = self.DUT.calculate_availability()
        self.assertEqual(_error_code, 102)
        self.assertEqual(
            _msg,
            'RTK ERROR: Zero Division Error when calculating the mission ' \
            'availability for Revision ID 1.  Mission MTBF: 0.000000 ' \
            'MTTR: 0.000000.'
        )

    @attr(all=True, unit=True)
    def test05a_calculate_costs(self):
        """
        (TestRTKRevision) calculate_costs should return a zero error code on success.
        """

        self.DUT.cost = 1252.78
        self.DUT.hazard_rate_logistics = 1.0 / 547885.1632698

        _error_code, _msg = self.DUT.calculate_costs(100.0)
        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Calculating cost metrics for ' \
                               'Revision ID 1.')
        self.assertAlmostEqual(self.DUT.cost_failure, 0.002286574)
        self.assertAlmostEqual(self.DUT.cost_hour, 12.5278)

    @attr(all=True, unit=True)
    def test05b_calculate_costs_divide_by_zero(self):
        """
        (TestRTKRevision) calculate_costs should return a non-zero error code when attempting to divide by zero.
        """

        self.DUT.cost = 1252.78
        self.DUT.hazard_rate_logistics = 1.0 / 547885.1632698

        _error_code, _msg = self.DUT.calculate_costs(0.0)
        self.assertEqual(_error_code, 102)
        self.assertEqual(
            _msg,
            'RTK ERROR: Zero Division Error when calculating the cost per ' \
            'mission hour for Revision ID 1.  Mission time: 0.000000.'
        )
