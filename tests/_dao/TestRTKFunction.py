#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit._dao.TestRTKFunction.py is part of The RTK Project

#
# All rights reserved.
"""Test class for testing the RTKFunction module algorithms and models."""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import unittest
from nose.plugins.attrib import attr

from rtk.dao.RTKFunction import RTKFunction

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestRTKFunction(unittest.TestCase):
    """
    Class for testing the RTKFunction class.
    """

    _attributes = {
        'type_id': 0,
        'total_part_count': 0,
        'availability_mission': 1.0,
        'cost': 0.0,
        'hazard_rate_mission': 0.0,
        'mpmt': 0.0,
        'parent_id': 0,
        'mtbf_logistics': 0.0,
        'safety_critical': 0,
        'mmt': 0.0,
        'hazard_rate_logistics': 0.0,
        'remarks': '',
        'function_id': 1,
        'mtbf_mission': 0.0,
        'function_code': 'PRESS-001',
        'name': u'Function Name',
        'level': 0,
        'mttr': 0.0,
        'mcmt': 0.0,
        'revision_id': 1,
        'availability_logistics': 1.0,
        'total_mode_count': 0
    }

    def setUp(self):
        """
        Sets up the test fixture for the RTKFunction class.
        """
        engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
        session = scoped_session(sessionmaker())

        session.remove()
        session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        self.DUT = session.query(RTKFunction).first()
        self.DUT.function_code = self._attributes['function_code']

        session.commit()

    @attr(all=True, unit=True)
    def test00_rtkfunction_create(self):
        """
        (TestRTKFunction) __init__ should create an RTKFunction model.
        """
        self.assertTrue(isinstance(self.DUT, RTKFunction))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_function')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.function_id, 1)
        self.assertEqual(self.DUT.availability_logistics, 1.0)
        self.assertEqual(self.DUT.availability_mission, 1.0)
        self.assertEqual(self.DUT.cost, 0.0)
        self.assertEqual(self.DUT.function_code, 'PRESS-001')
        self.assertEqual(self.DUT.hazard_rate_logistics, 0.0)
        self.assertEqual(self.DUT.hazard_rate_mission, 0.0)
        self.assertEqual(self.DUT.level, 0)
        self.assertEqual(self.DUT.mmt, 0.0)
        self.assertEqual(self.DUT.mcmt, 0.0)
        self.assertEqual(self.DUT.mpmt, 0.0)
        self.assertEqual(self.DUT.mtbf_logistics, 0.0)
        self.assertEqual(self.DUT.mtbf_mission, 0.0)
        self.assertEqual(self.DUT.mttr, 0.0)
        self.assertEqual(self.DUT.name, 'Function Name')
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.safety_critical, 0)
        self.assertEqual(self.DUT.total_mode_count, 0)
        self.assertEqual(self.DUT.total_part_count, 0)
        self.assertEqual(self.DUT.type_id, 0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKFunction) get_attributes should return a dict of {attribute name:attribute value} pairs.
        """
        self.assertEqual(self.DUT.get_attributes(), self._attributes)

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKFunction) set_attributes should return a zero error code on success
        """
        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKFunction {0:d} " \
                               "attributes.".format(self.DUT.function_id))

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKFunction) set_attributes should return a 40 error code when passed too few attributes
        """
        self._attributes.pop('type_id')

        _error_code, _msg = self.DUT.set_attributes(self._attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Missing attribute 'type_id' in " \
                               "attribute dictionary passed to " \
                               "RTKFunction.set_attributes().")

    @attr(all=True, unit=True)
    def test03a_calculate_mtbf(self):
        """
        (TestRTKFunction) calculate_mtbf should return a zero error code on success.
        """
        self.DUT.hazard_rate_logistics = 0.0000003
        self.DUT.hazard_rate_mission = 0.000002

        _error_code, _msg = self.DUT.calculate_mtbf()
        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Calculating MTBF metrics for ' \
                         'Function ID 1.')
        self.assertAlmostEqual(self.DUT.mtbf_logistics, 3333333.3333333)
        self.assertAlmostEqual(self.DUT.mtbf_mission, 500000.0)

    @attr(all=True, unit=True)
    def test04a_calculate_availability(self):
        """
        (TestRTKFunction) calculate_availability should return a zero error code on success.
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
                               'metrics for Function ID 1.')
        self.assertAlmostEqual(self.DUT.availability_logistics, 0.9999894)
        self.assertAlmostEqual(self.DUT.availability_mission, 0.9999884)

    @attr(all=True, unit=True)
    def test04b_calculate_availability_divide_by_zero(self):
        """
        (TestRTKFunction) calculate_availability should return a non-zero error code when attempting to divide by zero.
        """

        self.DUT.mttr = 0.0
        self.DUT.mtbf_logistics = 547885.1632698
        self.DUT.mtbf_mission = 0.0

        _error_code, _msg = self.DUT.calculate_availability()
        self.assertEqual(_error_code, 102)
        self.assertEqual(
            _msg,
            'RTK ERROR: Zero Division Error when calculating the mission ' \
            'availability for Function ID 1.  Mission MTBF: 0.000000 ' \
            'MTTR: 0.000000.'
        )
