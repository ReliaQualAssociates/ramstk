#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestProfile.py is part of The RTK Project
#
# All rights reserved.

"""
This is the test class for testing the Usage Profile module algorithms and
models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from treelib import Tree

import Configuration as Configuration
import Utilities as Utilities
from usage.UsageProfile import Model, UsageProfile
from dao.DAO import DAO, RTKRevision, RTKMission, RTKMissionPhase, \
    RTKEnvironment
from usage.Mission import Model as Mission
from usage.Phase import Model as Phase
from usage.Environment import Model as Environment

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestUsageProfileModel(unittest.TestCase):
    """
    Class for testing the Usage Profile model class.
    """

    def setUp(self):

        # Create a data access object and connect to a test database.
        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestDB.rtk')

        _revision = RTKRevision()
        self.dao.db_add(_revision)

        _mission = RTKMission()
        _mission.revision_id = _revision.revision_id
        _mission.description = 'Test Mission 1'
        self.dao.db_add(_mission)

        _phase = RTKMissionPhase()
        _phase.mission_id = _mission.mission_id
        _phase.description = 'Test Phase 11'
        self.dao.db_add(_phase)

        _environment = RTKEnvironment()
        _environment.phase_id = _phase.phase_id
        _environment.name = 'Test Environment 111'
        self.dao.db_add(_environment)

        self.DUT = Model()

        Configuration.DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/rtk_debug.log')
        Configuration.USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                        '/tmp/rtk_user.log')

    @attr(all=True, unit=True)
    def test01_profile_create(self):
        """
        (TestProfile) __init__ should create a Usage Profile data model.
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.dao, None)
        self.assertEqual(self.DUT.last_id, None)
        self.assertTrue(isinstance(self.DUT.mission, Mission))
        self.assertTrue(isinstance(self.DUT.phase, Phase))
        self.assertTrue(isinstance(self.DUT.environment, Environment))

    @attr(all=True, unit=True)
    def test02a_retrieve_profile(self):
        """
        (TestProfile): retrieve_profile should return a Tree() on success.
        """

        _tre_profile = self.DUT.retrieve_profile(self.dao, 1)

        self.assertTrue(isinstance(_tre_profile, Tree))
        self.assertTrue(isinstance(_tre_profile.get_node(1).data, RTKMission))
        self.assertEqual(_tre_profile.get_node(1).data.description,
                         'Test Mission 1')
        self.assertTrue(isinstance(_tre_profile.get_node(11).data,
                                   RTKMissionPhase))
        self.assertEqual(_tre_profile.get_node(11).data.description,
                     'Test Phase 11')
        self.assertTrue(isinstance(_tre_profile.get_node(111).data,
                                   RTKEnvironment))
        self.assertEqual(_tre_profile.get_node(111).data.name,
                     'Test Environment 111')

    @attr(all=True, unit=True)
    def test02b_retrieve_all_profile_nonexistent_revision(self):
        """
        (TestProfile): retrieve_all should return an empty Tree() when passed a Revision ID that doesn't exist.
        """

        _tre_profile = self.DUT.retrieve_profile(self.dao, 100)

        self.assertTrue(isinstance(_tre_profile, Tree))
        self.assertEqual(_tre_profile.get_node(0).tag, 'Usage Profiles')
        self.assertEqual(_tre_profile.get_node(1), None)

    @attr(all=True, unit=True)
    def test03a_add_mission_to_profile(self):
        """
        (TestProfile): add_profile should return a zero error code on success when adding a new Mission.
        """

        self.DUT.retrieve_profile(self.dao, 1)

        _error_code, _msg = self.DUT.add_profile(0, 0, 1)

        _tre_profile = self.DUT.retrieve_profile(self.dao, 1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding a new item to the Usage Profile.")

        self.assertTrue(isinstance(_tre_profile.get_node(5).data, RTKMission))

    @attr(all=True, unit=True)
    def test03b_add_phase_to_profile(self):
        """
        (TestProfile): add_profile should return a zero error code on success when adding a new Mission Phase.
        """

        self.DUT.retrieve_profile(self.dao, 1)

        _error_code, _msg = self.DUT.add_profile(1, 1, 1)

        _tre_profile = self.DUT.retrieve_profile(self.dao, 1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding a new item to the Usage Profile.")

        self.assertTrue(isinstance(_tre_profile.get_node(16).data,
                                   RTKMissionPhase))

    @attr(all=True, unit=True)
    def test03c_add_environment_to_profile(self):
        """
        (TestProfile): add_profile should return a zero error code on success when adding a new Environment.
        """

        self.DUT.retrieve_profile(self.dao, 1)

        _error_code, _msg = self.DUT.add_profile(2, 16, 6)

        _tre_profile = self.DUT.retrieve_profile(self.dao, 1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding a new item to the Usage Profile.")
        self.assertTrue(isinstance(_tre_profile.get_node(167).data,
                                   RTKEnvironment))

    @attr(all=True, unit=True)
    def test03d_add_unknown_to_profile(self):
        """
        (TestProfile): add_profile should return a 3001 error code when attempting to add something other than a Mission, Phase, or Environment.
        """

        self.DUT.retrieve_profile(self.dao, 1)

        _error_code, _msg = self.DUT.add_profile(4, 0, 1)

        self.DUT.retrieve_profile(self.dao, 1)

        self.assertEqual(_error_code, 3001)
        self.assertEqual(_msg,
                         "RTK ERROR: Attempted to add an item to the Usage " \
                         "Profile with an undefined indenture level.  Level " \
                         "4 was requested.  Must be one of 0 = Mission, " \
                         "1 = Mission Phase, and 2 = Environment.")

    @attr(all=True, unit=True)
    def test03e_add_to_profile_no_parent_in_tree(self):
        """
        (TestProfile): add_profile should return a 3002 error code when attempting to add something to a non-existant parent Node.
        """

        self.DUT.retrieve_profile(self.dao, 1)

        _error_code, _msg = self.DUT.add_profile(0, 10, 1)

        self.DUT.retrieve_profile(self.dao, 1)

        self.assertEqual(_error_code, 3002)
        self.assertEqual(_msg,
                         "RTK ERROR: Creating a new node in the Usage " \
                         "Profile Tree.")

    @attr(all=True, unit=True)
    def test04a_delete_mission_from_profile(self):
        """
        (TestProfile): delete_profile should return a zero error code on success when removing a Mission.
        """

        self.DUT.retrieve_profile(self.dao, 1)

        _error_code, _msg = self.DUT.delete_profile(0, 1)

        self.DUT.retrieve_profile(self.dao, 1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Deleting an item from the Usage Profile.")

    @attr(all=True, unit=True)
    def test04b_delete_unknown_from_profile(self):
        """
        (TestProfile): delete_profile should return a 3003 error code when attempting to remove an unkown item from the Profile.
        """

        self.DUT.retrieve_profile(self.dao, 1)

        _error_code, _msg = self.DUT.delete_profile(4, 1)

        self.DUT.retrieve_profile(self.dao, 1)

        self.assertEqual(_error_code, 3003)
        self.assertEqual(_msg,
                         "RTK ERROR: Attempted to delete an item from the " \
                         "Usage Profile with an undefined indenture level.  " \
                         "Level 4 was requested.  Must be one of 0 = " \
                         "Mission, 1 = Mission Phase, and 2 = Environment.")

    @attr(all=True, unit=True)
    def test04c_delete_non_existant_item_from_profile(self):
        """
        (TestProfile): delete_profile should return a 3004 error code when attempting to remove a non-existant item from the Profile.
        """

        self.DUT.retrieve_profile(self.dao, 1)

        _error_code, _msg = self.DUT.delete_profile(0, 100)

        self.DUT.retrieve_profile(self.dao, 1)

        self.assertEqual(_error_code, 3004)
        self.assertEqual(_msg,
                         "RTK ERROR: Failed to delete Node 100 from the " \
                         "Usage Profile.")

    @attr(all=True, unit=True)
    def test05a_save_profile(self):
        """
        (TestProfile): save_profile should return a zero error code on success.
        """

        self.DUT.retrieve_profile(self.dao, 1)

        _error_code, _msg = self.DUT.save_profile()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "SUCCESS: Updating the RTK Program database.")


class TestUsageProfileController(unittest.TestCase):
    """
    Class for testing the Usage Profile controller class.
    """

    def setUp(self):

        # Create a data access object and connect to a test database.
        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestDB.rtk')

        _revision = RTKRevision()
        self.dao.db_add(_revision)

        _mission = RTKMission()
        _mission.revision_id = _revision.revision_id
        _mission.description = 'Test Mission 1'
        self.dao.db_add(_mission)

        _phase = RTKMissionPhase()
        _phase.mission_id = _mission.mission_id
        _phase.description = 'Test Phase 11'
        self.dao.db_add(_phase)

        _environment = RTKEnvironment()
        _environment.phase_id = _phase.phase_id
        _environment.name = 'Test Environment 111'
        self.dao.db_add(_environment)

        self.DUT = UsageProfile()

        Configuration.DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/rtk_debug.log')
        Configuration.USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                        '/tmp/rtk_user.log')

    @attr(all=True, unit=True)
    def test01_create_controller(self):
        """
        (TestProfile) __init__ should create an instance of a UsageProfile data controller.
        """

        self.assertTrue(isinstance(self.DUT, UsageProfile))
        self.assertTrue(isinstance(self.DUT.usage_model, Model))
