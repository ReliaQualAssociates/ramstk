#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestRevision.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This is the test class for testing Revision Data Model and Revision Data
Controller algorithms and models.
"""

import sys
import logging
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from revision.Revision import Model, Revision
from dao.DAO import DAO
from dao.RTKRevision import RTKRevision

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'


class Test00RevisionModel(unittest.TestCase):
    """
    Class for testing the Revision model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Revision class.
        """

        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {'host'    : 'localhost',
                                            'socket'  : 3306,
                                            'database': '/tmp/TestDB.rtk',
                                            'user'    : '',
                                            'password': ''}

        self.Configuration.DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG', '/tmp/RTK_debug.log')
        self.Configuration.USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO', '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(bind=self.dao.engine, autoflush=False,
                                       expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)
        self.dao.db_add([RTKRevision(), ], self.session)
        self.dao.db_add([RTKRevision(), ], self.session)

        self.DUT = Model(self.dao)

    @attr(all=True, unit=True)
    def test00_revision_create(self):
        """
        (TestRevisionModel) __init__ should return a Revision model
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))

    @attr(all=True, unit=True)
    def test01_get_all(self):
        """
        (TestRevisionModel): get_all() should return a Tree() object populated with RTKRevision instances on success.
        """

        _tree = self.DUT.get_all()

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKRevision))

    @attr(all=True, unit=True)
    def test02a_get(self):
        """
        (TestRevisionModel): get() should return an instance of the RTKRevision data model on success.
        """

        self.DUT.get_all()
        _revision = self.DUT.get(1)

        self.assertTrue(isinstance(_revision, RTKRevision))
        self.assertEqual(_revision.revision_id, 1)
        self.assertEqual(_revision.availability_logistics, 1.0)

    @attr(all=True, unit=True)
    def test02b_get_non_existent_revision(self):
        """
        (TestRevisionModel): get() should return None when a non-existent Revision ID is requested.
        """

        _revision = self.DUT.get(100)

        self.assertEqual(_revision, None)

    @attr(all=True, unit=True)
    def test03a_add(self):
        """
        (TestRevisionModel): add() should return False on success.
        """

        self.DUT.get_all()

        _error_code, _msg = self.DUT.add()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                               'the RTK Program database.')
        self.assertEqual(self.DUT._last_id, 12)

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """
        (TestRevisionModel): delete() should return a zero error code on success.
        """

        self.DUT.get_all()

        _error_code, _msg = self.DUT.delete(3)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                               'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_revision_id(self):
        """
        (TestRevisionModel): delete() should return a non-zero error code when passed a Revision ID that doesn't exist.
        """

        self.DUT.get_all()

        _error_code, _msg = self.DUT.delete(3)

        self.assertEqual(_error_code, 1000)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to delete non-existent '
                               'Revision ID 3.')

    @attr(all=True, unit=True)
    def test_05a_save(self):
        """
        (TestRevisionModel): save() should return a zero error code on success.
        """

        self.DUT.get_all()
        _revision = self.DUT.tree.get_node(1).data
        _revision.availability_logistics = 0.9832

        _error_code, _msg = self.DUT.save(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test_05b_save_non_existent_revision(self):
        """
        (TestRevisionModel): save() should return a non-zero error code when passed a Revision ID that doesn't exist.
        """

        self.DUT.get_all()

        _error_code, _msg = self.DUT.save(100)

        self.assertEqual(_error_code, 1000)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                               'Revision ID 100.')

    @attr(all=True, unit=True)
    def test_06a_save_all(self):
        """
        (TestRevisionModel): save_all() should return a zero error code on success.
        """

        self.DUT.get_all()

        _error_code, _msg = self.DUT.save_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test07a_calculate_reliability(self):
        """
        (TestRTKRevision) calculate_reliability should return a zero error code on success.
        """

        self.DUT.get_all()

        _revision = self.DUT.tree.get_node(1).data
        _revision.hazard_rate_active = 0.00000151
        _revision.hazard_rate_dormant = 0.0000000152
        _revision.hazard_rate_software = 0.0000003
        _revision.hazard_rate_mission = 0.000002

        _error_code, _msg = self.DUT.calculate_reliability(1, 100.0, 1.0)
        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Calculating reliability ' \
                               'metrics for Revision ID 1.')
        self.assertAlmostEqual(_revision.hazard_rate_logistics, 1.8252e-06)
        self.assertAlmostEqual(_revision.mtbf_logistics, 547885.1632698)
        self.assertAlmostEqual(_revision.mtbf_mission, 500000.0)
        self.assertAlmostEqual(_revision.reliability_logistics, 0.9998175)
        self.assertAlmostEqual(_revision.reliability_mission, 0.9998000)

    @attr(all=True, unit=True)
    def test07b_calculate_reliability_divide_by_zero(self):
        """
        (TestRTKRevision) calculate_reliability should return a non-zero error code when attempting to divide by zero.
        """

        self.DUT.get_all()

        _revision = self.DUT.tree.get_node(1).data
        _revision.hazard_rate_mission = 0.0

        _error_code, _msg = self.DUT.calculate_reliability(1, 100.0, 1.0)
        self.assertEqual(_error_code, 1001)
        self.assertEqual(_msg, 'RTK ERROR: Zero Division or Overflow Error ' \
                               'when calculating the mission MTBF for ' \
                               'Revision ID 1.  Mission hazard rate: ' \
                               '0.000000.')

    @attr(all=True, unit=True)
    def test08a_calculate_availability(self):
        """
        (TestRTKRevision) calculate_availability should return a zero error code on success.
        """

        self.DUT.get_all()

        _revision = self.DUT.tree.get_node(1).data
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
        (TestRTKRevision) calculate_availability should return a non-zero error code when attempting to divide by zero.
        """

        self.DUT.get_all()

        _revision = self.DUT.tree.get_node(1).data
        _revision.mttr = 0.0
        _revision.mtbf_logistics = 547885.1632698
        _revision.mtbf_mission = 0.0

        _error_code, _msg = self.DUT.calculate_availability(1)
        self.assertEqual(_error_code, 1001)
        self.assertEqual(_msg, 'RTK ERROR: Zero Division or Overflow Error ' \
                               'when calculating the mission availability ' \
                               'for Revision ID 1.  Mission MTBF: 0.000000 ' \
                               'and MTTR: 0.000000.')

    @attr(all=True, unit=True)
    def test09a_calculate_costs(self):
        """
        (TestRTKRevision) calculate_costs should return a zero error code on success.
        """

        self.DUT.get_all()

        _revision = self.DUT.tree.get_node(1).data
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

        self.DUT.get_all()

        _revision = self.DUT.tree.get_node(1).data
        _revision.cost = 1252.78
        _revision.hazard_rate_logistics = 1.0 / 547885.1632698

        _error_code, _msg = self.DUT.calculate_costs(1, 0.0)
        self.assertEqual(_error_code, 1001)
        self.assertEqual(_msg, 'RTK ERROR: Zero Division Error or Overflow ' \
                               'Error when calculating the cost per mission ' \
                               'hour for Revision ID 1.  Mission time: ' \
                               '0.000000.')


class Test01RevisionController(unittest.TestCase):
    """
    Class for testing the Revision Data Controller class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Revision Data Controller.
        """

        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {'host'    : 'localhost',
                                            'socket'  : 3306,
                                            'database': '/tmp/TestDB.rtk',
                                            'user'    : '',
                                            'password': ''}

        self.Configuration.RTK_DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", logging.DEBUG,
                                    '/tmp/RTK_debug.log')
        self.Configuration.RTK_USER_LOG = \
            Utilities.create_logger("RTK.user", logging.WARNING,
                                    '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(bind=self.dao.engine, autoflush=False,
                                       expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)
        self.dao.db_add([RTKRevision(), ], self.session)
        self.dao.db_add([RTKRevision(), ], self.session)

        self.DUT = Revision(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """
        (TestRevisionController) __init__ should return a Revision Data Controller
        """

        self.assertTrue(isinstance(self.DUT, Revision))
        self.assertTrue(isinstance(self.DUT._dtm_revision, Model))

    @attr(all=True, unit=True)
    def test01_request_get_all(self):
        """
        (TestRevisionController) request_get_all() should return a Tree of RTKRevision models.
        """

        _tree = self.DUT.request_get_all()

        self.assertTrue(isinstance(_tree.get_node(1).data, RTKRevision))

    @attr(all=True, unit=True)
    def test02a_request_get(self):
        """
        (TestRevisionController) request_get() should return an RTKRevision model.
        """

        self.DUT.request_get_all()

        _revision = self.DUT.request_get(1)

        self.assertTrue(isinstance(_revision, RTKRevision))

    @attr(all=True, unit=True)
    def test02b_request_non_existent_revision(self):
        """
        (TestRevisionController) request_get() should return None when requesting a Revision that doesn't exist.
        """

        _revision = self.DUT.request_get(100)

        self.assertEqual(_revision, None)

    @attr(all=True, unit=True)
    def test03a_request_add(self):
        """
        (TestRevisionController) request_add() should return False on success.
        """

        self.DUT.request_get_all()
        self.assertFalse(self.DUT.request_add())

    @attr(all=True, unit=True)
    def test04a_request_delete(self):
        """
        (TestRevisionController) request_delete() should return False on success.
        """

        self.DUT.request_get_all()

        self.assertFalse(self.DUT.request_delete(5))

    @attr(all=True, unit=True)
    def test04a_request_delete_non_existent_revision(self):
        """
        (TestRevisionController) request_delete() should return True when attempting to delete a non-existent Revision.
        """

        self.DUT.request_get_all()

        self.assertTrue(self.DUT.request_delete(100))

    @attr(all=True, unit=True)
    def test05a_request_save(self):
        """
        (TestRevisionController) request_save() should return False on success.
        """

        self.DUT.request_get_all()

        self.assertFalse(self.DUT.request_save(2))

    @attr(all=True, unit=True)
    def test05b_request_save_non_existent_revision(self):
        """
        (TestRevisionController) request_save() should return True when attempting to save a non-existent Revision.
        """

        self.DUT.request_get_all()

        self.assertTrue(self.DUT.request_save(100))

    @attr(all=True, unit=True)
    def test06a_request_save_all(self):
        """
        (TestRevisionController) request_save_all() should return False on success.
        """

        self.DUT.request_get_all()

        _error_code, _msg = self.DUT.request_save_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test07a_request_calculate_reliability(self):
        """
        (TestRevisionController) request_calculate_reliability() should return False on success.
        """

        self.DUT.request_get_all()

        _revision = self.DUT._dtm_revision.tree.get_node(1).data
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

        self.assertFalse(self.DUT.request_calculate_reliability(1, 100.0))

        self.assertAlmostEqual(_revision.hazard_rate_logistics, 1.8252e-06)
        self.assertAlmostEqual(_revision.mtbf_logistics, 547885.1632698)
        self.assertAlmostEqual(_revision.mtbf_mission, 500000.0)
        self.assertAlmostEqual(_revision.reliability_logistics,
                               0.99999999981748)
        self.assertAlmostEqual(_revision.reliability_mission, 0.9999999998)

    @attr(all=True, unit=True)
    def test07b_request_calculate_availability(self):
        """
        (TestRevisionController) request_calculate_availability() should return False on success.
        """

        self.DUT.request_get_all()

        _revision = self.DUT._dtm_revision.tree.get_node(1).data
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
        #self.assertAlmostEqual(_revision.cost_per_failure, 0.002286574)
        #self.assertAlmostEqual(_revision.cost_per_hour, 12.5278)

    @attr(all=True, unit=True)
    def test07b_request_calculate_cost(self):
        """
        (TestRevisionController) request_calculate_cost() should return False on success.
        """

        self.DUT.request_get_all()

        _revision = self.DUT._dtm_revision.tree.get_node(1).data
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