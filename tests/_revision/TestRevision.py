#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.revision.TestRevision.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
This is the test class for testing Revision Data Model and Revision Data
Controller algorithms and models.
"""

import sys
from os.path import dirname

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk",
)

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from revision import dtmRevision, dtcRevision
from dao import DAO
from dao import RTKRevision

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'


class TestRevisionDataModel(unittest.TestCase):
    """
    Class for testing the Revision model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Revision class.
        """

        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {
            'host': 'localhost',
            'socket': 3306,
            'database': '/tmp/TestDB.rtk',
            'user': '',
            'password': ''
        }

        self.Configuration.DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG', '/tmp/RTK_debug.log')
        self.Configuration.USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO', '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)

        self.DUT = dtmRevision(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestRevisionModel) __init__ should return a Revision model
        """

        self.assertTrue(isinstance(self.DUT, dtmRevision))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))

    @attr(all=True, unit=True)
    def test01_select_all(self):
        """
        (TestRevisionModel) select_all(None) should return a Tree() object populated with RTKRevision instances on success.
        """

        _tree = self.DUT.select_all(None)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKRevision))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """
        (TestRevisionModel) select() should return an instance of the RTKRevision data model on success.
        """

        self.DUT.select_all(None)
        _revision = self.DUT.select(1)

        self.assertTrue(isinstance(_revision, RTKRevision))
        self.assertEqual(_revision.revision_id, 1)
        self.assertEqual(_revision.availability_logistics, 1.0)

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """
        (TestRevisionModel) select() should return None when a non-existent Revision ID is requested.
        """

        _revision = self.DUT.select(100)

        self.assertEqual(_revision, None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """(TestRevisionModel) insert() should return False on success."""
        self.DUT.select_all(None)

        _error_code, _msg = self.DUT.insert()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 2)

        self.DUT.delete(self.DUT.last_id)

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """(TestRevisionModel) delete() should return a zero error code on success."""
        self.DUT.select_all(None)
        self.DUT.insert()

        _error_code, _msg = self.DUT.delete(self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """(TestRevisionModel) delete() should return a non-zero error code when passed a Revision ID that doesn't exist."""
        self.DUT.select_all(None)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                         'Revision ID 300.')

    @attr(all=True, unit=True)
    def test05a_update(self):
        """(TestRevisionModel) update() should return a zero error code on success."""
        self.DUT.select_all(None)

        _revision = self.DUT.tree.get_node(1).data
        _revision.availability_logistics = 0.9832

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test05b_update_non_existent_id(self):
        """(TestRevisionModel) update() should return a non-zero error code when passed a Revision ID that doesn't exist."""
        self.DUT.select_all(None)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'Revision ID 100.')

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """(TestRevisionModel) update_all() should return a zero error code on success."""
        self.DUT.select_all(None)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test07a_calculate_hazard_rate(self):
        """
        (TestRTKRevision) calculate_hazard_rate should return a zero error code on success.
        """

        self.DUT.select_all(None)

        _revision = self.DUT.select(1)
        _revision.hazard_rate_active = 0.00000151
        _revision.hazard_rate_dormant = 0.0000000152
        _revision.hazard_rate_software = 0.0000003
        _revision.hazard_rate_mission = 0.000002

        _error_code, _msg = self.DUT.calculate_hazard_rate(1)
        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Calculating hazard rates for '
                         'Revision ID 1.')
        self.assertAlmostEqual(_revision.hazard_rate_logistics, 1.8252e-06)

    @attr(all=True, unit=True)
    def test07b_calculate_mtbf(self):
        """
        (TestRTKRevision) calculate_mtbf should return a zero error code on success.
        """

        self.DUT.select_all(None)

        _revision = self.DUT.select(1)
        _revision.hazard_rate_active = 0.00000151
        _revision.hazard_rate_dormant = 0.0000000152
        _revision.hazard_rate_software = 0.0000003
        _revision.hazard_rate_mission = 0.000002
        _revision.calculate_hazard_rate()

        _error_code, _msg = self.DUT.calculate_mtbf(1)
        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Calculating MTBFs for Revision ID 1.')
        self.assertAlmostEqual(_revision.mtbf_logistics, 547885.1632698)
        self.assertAlmostEqual(_revision.mtbf_mission, 500000.0)

    @attr(all=True, unit=True)
    def test07b_calculate_reliability_divide_by_zero(self):
        """
        (TestRevisionModel) calculate_reliability should return a non-zero error code when attempting to divide by zero.
        """

        self.DUT.select_all(None)

        _revision = self.DUT.select(1)
        _revision.hazard_rate_active = 0.00000151
        _revision.hazard_rate_dormant = 0.0000000152
        _revision.hazard_rate_software = 0.0000003
        _revision.hazard_rate_mission = 0.000002

        _error_code, _msg = self.DUT.calculate_reliability(1, 100.0, 0.0)
        self.assertEqual(_error_code, 102)
        self.assertEqual(
            _msg,
            'RTK ERROR: Zero Division Error when calculating the mission '
            'reliability for Revision ID 1.  Hazard rate multiplier: 0.000000.'
        )

    @attr(all=True, unit=True)
    def test08a_calculate_availability(self):
        """
        (TestRevisionModel) calculate_availability should return a zero error code on success.
        """

        self.DUT.select_all(None)

        _revision = self.DUT.select(1)
        _revision.mpmt = 0.5
        _revision.mcmt = 1.2
        _revision.mttr = 5.8
        _revision.mmt = 0.85
        _revision.mtbf_logistics = 547885.1632698
        _revision.mtbf_mission = 500000.0

        _error_code, _msg = self.DUT.calculate_availability(1)
        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Calculating availability ' \
                               'metrics for Revision ID 1.')
        self.assertAlmostEqual(_revision.availability_logistics, 0.9999894)
        self.assertAlmostEqual(_revision.availability_mission, 0.9999884)

    @attr(all=True, unit=True)
    def test08b_calculate_availability_divide_by_zero(self):
        """
        (TestRevisionModel) calculate_availability should return a non-zero error code when attempting to divide by zero.
        """

        self.DUT.select_all(None)

        _revision = self.DUT.select(1)
        _revision.mttr = 0.0
        _revision.mtbf_logistics = 547885.1632698
        _revision.mtbf_mission = 0.0

        _error_code, _msg = self.DUT.calculate_availability(1)
        self.assertEqual(_error_code, 102)
        self.assertEqual(
            _msg,
            'RTK ERROR: Zero Division Error when calculating the mission ' \
            'availability for Revision ID 1.  Mission MTBF: 0.000000 MTTR: ' \
            '0.000000.'
        )

    @attr(all=True, unit=True)
    def test09a_calculate_costs(self):
        """
        (TestRevisionModel) calculate_costs should return a zero error code on success.
        """

        self.DUT.select_all(None)

        _revision = self.DUT.select(1)
        _revision.cost = 1252.78
        _revision.hazard_rate_logistics = 1.0 / 547885.1632698

        _error_code, _msg = self.DUT.calculate_costs(1, 100.0)
        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Calculating cost metrics for ' \
                               'Revision ID 1.')
        self.assertAlmostEqual(_revision.cost_failure, 0.002286574)
        self.assertAlmostEqual(_revision.cost_hour, 12.5278)

    @attr(all=True, unit=True)
    def test09b_calculate_costs_divide_by_zero(self):
        """
        (TestRTKRevision) calculate_costs should return a non-zero error code when attempting to divide by zero.
        """

        self.DUT.select_all(None)

        _revision = self.DUT.select(1)
        _revision.cost = 1252.78
        _revision.hazard_rate_logistics = 1.0 / 547885.1632698

        _error_code, _msg = self.DUT.calculate_costs(1, 0.0)
        self.assertEqual(_error_code, 102)
        self.assertEqual(_msg, 'RTK ERROR: Zero Division Error ' \
                               'when calculating the cost per mission ' \
                               'hour for Revision ID 1.  Mission time: ' \
                               '0.000000.')


class TestRevisionDataController(unittest.TestCase):
    """
    Class for testing the Revision Data Controller class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Revision Data Controller.
        """

        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {
            'host': 'localhost',
            'socket': 3306,
            'database': '/tmp/TestDB.rtk',
            'user': '',
            'password': ''
        }

        self.Configuration.RTK_DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG',
                                    '/tmp/RTK_debug.log')
        self.Configuration.RTK_USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO',
                                    '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)

        self.DUT = dtcRevision(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """
        (TestRevisionController) __init__ should return a Revision Data Controller
        """

        self.assertTrue(isinstance(self.DUT, dtcRevision))
        self.assertTrue(isinstance(self.DUT._dtm_data_model, dtmRevision))

    @attr(all=True, unit=True)
    def test01a_request_select_all(self):
        """
        (TestRevisionController) request_select_all(None) should return a Tree of RTKRevision models.
        """

        _tree = self.DUT.request_select_all(1)

        self.assertTrue(isinstance(_tree.get_node(1).data, RTKRevision))

    @attr(all=True, unit=True)
    def test02a_request_select(self):
        """
        (TestRevisionController) request_select() should return an RTKRevision model.
        """

        self.DUT.request_select_all(1)

        _revision = self.DUT.request_select(1)

        self.assertTrue(isinstance(_revision, RTKRevision))

    @attr(all=True, unit=True)
    def test02b_request_non_existent_id(self):
        """
        (TestRevisionController) request_select() should return None when requesting a Revision that doesn't exist.
        """

        _revision = self.DUT.request_select(100)

        self.assertEqual(_revision, None)

    @attr(all=True, unit=True)
    def test03a_request_get_attributes(self):
        """
        (TestRevisionController) request_get_attributes() should return a dict of {attribute name:attribute value} pairs.
        """

        self.DUT.request_select_all(None)

        _attributes = self.DUT.request_get_attributes(1)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_attributes['revision_code'], '')

    @attr(all=True, unit=True)
    def test03b_request_set_attributes(self):
        """
        (TestRevisionController) request_set_attributes() should return a dict of {attribute name:attribute value} pairs.
        """

        self.DUT.request_select_all(None)

        _attributes = {
            'revision_id': 1,
            'availability_logistics': 0.9986,
            'availability_mission': 0.99934,
            'cost': 12532.15,
            'cost_per_failure': 0.0000352,
            'cost_per_hour': 1.2532,
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
            'name': 'Original Revision',
            'reliability_logistics': 0.99986,
            'reliability_mission': 0.99992,
            'remarks': 'This is the original revision.',
            'n_parts': 128,
            'revision_code': 'Rev. -',
            'program_time': 2562,
            'program_time_sd': 26.83,
            'program_cost': 26492.83,
            'program_cost_sd': 15.62
        }

        _error_code, _msg = self.DUT.request_set_attributes(1, _attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating RTKRevision 1 attributes.')

    @attr(all=True, unit=True)
    def test03c_request_last_id(self):
        """
        (TestRevisionController) request_last_id() should return the last Revision ID used in the RTK Program database.
        """

        self.DUT.request_select_all(None)

        _last_id = self.DUT.request_last_id()

        self.assertEqual(_last_id, 1)

    @attr(all=True, unit=True)
    def test04a_request_insert(self):
        """(TestRevisionController) request_insert() should return False on success."""
        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_insert())

        self.DUT.request_delete(self.DUT.request_last_id())

    @attr(all=True, unit=True)
    def test05a_request_delete(self):
        """(TestRevisionController) request_delete() should return False on success."""
        self.DUT.request_select_all(1)
        self.DUT.request_insert()

        self.assertFalse(self.DUT.request_delete(self.DUT.request_last_id()))

    @attr(all=True, unit=True)
    def test05b_request_delete_non_existent_id(self):
        """(TestRevisionController) request_delete() should return True when attempting to delete a non-existent Revision."""
        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_delete(100))

    @attr(all=True, unit=True)
    def test06a_request_update(self):
        """
        (TestRevisionController) request_update() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update(self.DUT.request_last_id()))

    @attr(all=True, unit=True)
    def test06b_request_update_non_existent_id(self):
        """
        (TestRevisionController) request_update() should return True when attempting to save a non-existent Revision.
        """

        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_update(100))

    @attr(all=True, unit=True)
    def test07a_request_update_all(self):
        """
        (TestRevisionController) request_update_all() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update_all())

    @attr(all=True, unit=True)
    def test08a_request_calculate_reliability(self):
        """
        (TestRevisionController) request_calculate_reliability() should return False on success.
        """

        self.DUT.request_select_all(1)

        _revision = self.DUT._dtm_data_model.tree.get_node(1).data
        _revision.hazard_rate_active = 0.00000151
        _revision.hazard_rate_dormant = 0.0000000152
        _revision.hazard_rate_software = 0.0000003
        _revision.hazard_rate_logistics = 1.8252e-06
        _revision.hazard_rate_mission = 0.000002
        _revision.mpmt = 0.5
        _revision.mcmt = 1.2
        _revision.mttr = 5.8
        _revision.mmt = 0.85
        _revision.mtbf_logistics = 547885.1632698
        _revision.mtbf_mission = 500000.0
        _revision.cost = 1252.78

        self.assertFalse(self.DUT.request_calculate_reliability(1, 100.0, 1.0))

        self.assertAlmostEqual(_revision.hazard_rate_logistics, 1.8252e-06)
        self.assertAlmostEqual(_revision.mtbf_logistics, 547885.1632698)
        self.assertAlmostEqual(_revision.mtbf_mission, 500000.0)
        self.assertAlmostEqual(_revision.reliability_logistics, 0.9998175)
        self.assertAlmostEqual(_revision.reliability_mission, 0.99980002)

    @attr(all=True, unit=True)
    def test08b_request_calculate_availability(self):
        """
        (TestRevisionController) request_calculate_availability() should return False on success.
        """

        self.DUT.request_select_all(1)

        _revision = self.DUT._dtm_data_model.tree.get_node(1).data
        _revision.hazard_rate_active = 0.00000151
        _revision.hazard_rate_dormant = 0.0000000152
        _revision.hazard_rate_software = 0.0000003
        _revision.hazard_rate_mission = 0.000002
        _revision.mpmt = 0.5
        _revision.mcmt = 1.2
        _revision.mttr = 5.8
        _revision.mmt = 0.85
        _revision.mtbf_logistics = 547885.1632698
        _revision.mtbf_mission = 500000.0
        _revision.cost = 1252.78

        self.assertFalse(self.DUT.request_calculate_availability(1))

        self.assertAlmostEqual(_revision.availability_logistics, 0.9999894)
        self.assertAlmostEqual(_revision.availability_mission, 0.9999884)

    @attr(all=True, unit=True)
    def test08c_request_calculate_cost(self):
        """
        (TestRevisionController) request_calculate_cost() should return False on success.
        """

        self.DUT.request_select_all(1)

        _revision = self.DUT._dtm_data_model.tree.get_node(1).data
        _revision.hazard_rate_active = 0.00000151
        _revision.hazard_rate_dormant = 0.0000000152
        _revision.hazard_rate_software = 0.0000003
        _revision.hazard_rate_mission = 0.000002
        _revision.hazard_rate_logistics = 1.8252e-06
        _revision.mpmt = 0.5
        _revision.mcmt = 1.2
        _revision.mttr = 5.8
        _revision.mmt = 0.85
        _revision.mtbf_logistics = 547885.1632698
        _revision.mtbf_mission = 500000.0
        _revision.cost = 1252.78

        self.assertFalse(self.DUT.request_calculate_costs(1, 100.0))

        self.assertAlmostEqual(_revision.cost_failure, 0.002286574)
        self.assertAlmostEqual(_revision.cost_hour, 12.5278)
