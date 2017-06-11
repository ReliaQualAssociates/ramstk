#!/usr/bin/env python -O
"""
This is the test class for testing Revision Data Model and Revision Data
Controller algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestRevision.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import Configuration as Configuration
import Utilities as Utilities
from revision.Revision import Model, Revision
from dao.DAO import DAO, RTKRevision

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

        # Create a data access object and connect to a test database.
        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestDB.rtk')
        self.dao.db_add(RTKRevision())
        self.dao.db_add(RTKRevision())

        self.DUT = Model()
        self.DUT.dao = self.dao

        Configuration.DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/rtk_debug.log')
        Configuration.USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                        '/tmp/rtk_user.log')

    @attr(all=True, unit=True)
    def test00_revision_create(self):
        """
        (TestRevision) __init__ should return a Revision model
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertEqual(self.DUT.dicRevision, {})
        self.assertTrue(isinstance(self.DUT.dao, DAO))

    @attr(all=True, unit=True)
    def test01_retrieve_all_revisions(self):
        """
        (TestRevision): retrieve_all should return False on success.
        """

        _dic_revisions = self.DUT.retrieve_all(self.dao)

        self.assertTrue(isinstance(_dic_revisions, dict))
        self.assertTrue(isinstance(_dic_revisions[1], RTKRevision))

    @attr(all=True, unit=True)
    def test02a_retrieve_single_revision(self):
        """
        (TestRevision): retrieve should return an instance of the RTKRevision data model on success.
        """

        _revision = self.DUT.retrieve(1)

        self.assertTrue(isinstance(_revision, RTKRevision))
        self.assertEqual(_revision.revision_id, 1)
        self.assertEqual(_revision.availability_logistics, 1.0)

    @attr(all=True, unit=True)
    def test02b_retrieve_missing_revision(self):
        """
        (TestRevision): retrieve should return an instance of the RTKRevision data model on success.
        """

        _revision = self.DUT.retrieve(100)

        self.assertEqual(_revision, None)

    @attr(all=True, unit=True)
    def test03a_add_revision(self):
        """
        (TestRevision): add_revision should return False on success.
        """

        self.assertFalse(self.DUT.add_revision())

    @attr(all=True, unit=True)
    def test04a_delete_revision(self):
        """
        (TestRevision): delete_revision should return False on success.
        """

        self.assertFalse(self.DUT.delete_revision(3))

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_revision_id(self):
        """
        (TestRevision): delete_revision should return True when passed a Revision ID that doesn't exist.
        """

        self.assertTrue(self.DUT.delete_revision(100))

    @attr(all=True, unit=True)
    def test_05a_save_revision(self):
        """
        (TestRevision): save_revision should return False on success.
        """

        _revision = self.DUT.dicRevision[1]
        _revision.availability_logistics = 0.9832

        self.assertFalse(self.DUT.save_revision(1))

    @attr(all=True, unit=True)
    def test_05b_save_non_existent_revision(self):
        """
        (TestRevision): save_revision should return True when passed a Revision ID that doesn't exist.
        """

        self.assertTrue(self.DUT.save_revision(100))

    @attr(all=True, unit=True)
    def test_06a_save_all_revisions(self):
        """
        (TestRevision): save_all_revisions should return False on success.
        """

        self.assertFalse(self.DUT.save_all_revisions())

    @attr(all=True, unit=True)
    def test07_revision_get_attributes(self):
        """
        (TestRevision) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(1),
                         (1, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 1.0, 1.0, '', 1,
                          '', 0.0, 0.0, 0.0, 0.0))

    @attr(all=True, unit=True)
    def test08a_calculate(self):
        """
        (TestRevision) calculate should return False on success
        """

        _revision = self.DUT.dicRevision[1]
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

        self.assertFalse(self.DUT.calculate(1, 100.0))

    @attr(all=True, unit=True)
    def test08b_calculate_with_bad_inputs(self):
        """
        (TestRevision) calculate should return True with one or more bad input.
        """

        _revision = self.DUT.dicRevision[1]
        _revision.hazard_rate_active = 0.00000151
        _revision.hazard_rate_dormant = 0.0000000152
        _revision.hazard_rate_software = 0.0000003
        _revision.hazard_rate_mission = 0.0
        _revision.mpmt = 0.5
        _revision.mcmt = 1.2
        _revision.mttr = 5.8
        _revision.mmt = 0.85
        _revision.mtbf_logistics = 547885.1632698
        _revision.mtbf_mission = 500000.0
        _revision.cost = 1252.78

        self.assertTrue(self.DUT.calculate(1, 100.0))


class Test01RevisionController(unittest.TestCase):
    """
    Class for testing the Revision Data Controller class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Revision Data Controller.
        """

        # Create a data access object and connect to a test database.
        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestDB.rtk')
        self.dao.db_add(RTKRevision())
        self.dao.db_add(RTKRevision())

        self.DUT = Revision()
        self.DUT.revision_model.dao = self.dao

        Configuration.DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/rtk_debug.log')
        Configuration.USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                        '/tmp/rtk_user.log')

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """
        (TestRevision) __init__ should return a Revision Data Controller
        """

        self.assertTrue(isinstance(self.DUT, Revision))
        self.assertTrue(isinstance(self.DUT.revision_model, Model))

    @attr(all=True, unit=True)
    def test01_request_revision_tree(self):
        """
        (TestRevision) request_revision_tree should return a dictionary of RTKRevision models.
        """

        _dic_revisions = self.DUT.request_revision_tree(self.dao)

        self.assertTrue(isinstance(_dic_revisions[1], RTKRevision))

    @attr(all=True, unit=True)
    def test02a_request_revision(self):
        """
        (TestRevision) request_revision should return an RTKRevision model.
        """

        _revision = self.DUT.request_revision(1)

        self.assertTrue(isinstance(_revision, RTKRevision))

    @attr(all=True, unit=True)
    def test02b_request_non_existent_revision(self):
        """
        (TestRevision) request_revision should return None when requesting a Revision that doesn't exist.
        """

        _revision = self.DUT.request_revision(100)

        self.assertEqual(_revision, None)

    @attr(all=True, unit=True)
    def test03a_request_add_revision(self):
        """
        (TestRevision) request_add_revision should return False on success.
        """

        self.assertFalse(self.DUT.request_add_revision())

    @attr(all=True, unit=True)
    def test04a_request_delete_revision(self):
        """
        (TestRevision) request_delete_revision should return False on success.
        """

        self.assertFalse(self.DUT.request_delete_revision(1))

    @attr(all=True, unit=True)
    def test04a_request_delete_non_existent_revision(self):
        """
        (TestRevision) request_delete_revision should return True when attempting to delete a non-existent Revision.
        """

        self.assertTrue(self.DUT.request_delete_revision(100))

    @attr(all=True, unit=True)
    def test05a_request_save_revision(self):
        """
        (TestRevision) request_save_revision should return False on success.
        """

        self.assertFalse(self.DUT.request_save_revision(2))

    @attr(all=True, unit=True)
    def test05b_request_save_non_existent_revision(self):
        """
        (TestRevision) request_save_revision should return True when attempting to save a non-existent Revision.
        """

        self.assertTrue(self.DUT.request_save_revision(100))

    @attr(all=True, unit=True)
    def test06a_request_save_all_revisions(self):
        """
        (TestRevision) request_save_all_revisions should return False on success.
        """

        self.assertFalse(self.DUT.request_save_all_revisions())

    @attr(all=True, unit=True)
    def test07a_request_calculate_revision(self):
        """
        (TestRevision) request_calculate_revision should return False on success.
        """

        _revision = self.DUT.revision_model.dicRevision[2]

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

        self.assertFalse(self.DUT.request_calculate_revision(2, 100.0))

        self.assertAlmostEqual(_revision.hazard_rate_logistics, 1.8252e-06)
        self.assertAlmostEqual(_revision.mtbf_logistics, 547885.1632698)
        self.assertAlmostEqual(_revision.mtbf_mission, 500000.0)
        self.assertAlmostEqual(_revision.reliability_logistics, 0.9998175)
        self.assertAlmostEqual(_revision.reliability_mission, 0.9998000)
        self.assertAlmostEqual(_revision.availability_logistics, 0.9999894)
        self.assertAlmostEqual(_revision.availability_mission, 0.9999884)
        self.assertAlmostEqual(_revision.cost_per_failure, 0.002286574)
        self.assertAlmostEqual(_revision.cost_per_hour, 12.5278)
