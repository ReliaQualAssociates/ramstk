#!/usr/bin/env python -O
"""
This is the test class for testing the Phase class.
"""

# -*- coding: utf-8 -*-
#
#       TestPhase.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

# We add this to ensure the imports within the rtk packages will work.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import Configuration as Configuration
import Utilities as Utilities
from usage.Phase import Model, Phase
from dao.DAO import DAO, RTKRevision, RTKMission, RTKMissionPhase

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestPhaseModel(unittest.TestCase):
    """
    Class for testing the Phase model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Phase model class.
        """

        # Create a data access object and connect to a test database.
        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestDB.rtk')

        _revision = RTKRevision()
        self.dao.db_add(_revision)

        _mission = RTKMission()
        _mission.revision_id = _revision.revision_id
        self.dao.db_add(_mission)

        _phase = RTKMissionPhase()
        _phase.mission_id = _mission.mission_id
        self.dao.db_add(_phase)

        self.DUT = Model()
        self.DUT.dao = self.dao

        Configuration.DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/RTK_debug.log')
        Configuration.USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                        '/tmp/RTK_user.log')

    @attr(all=True, unit=True)
    def test00_phase_create(self):
        """
        (TestMissionPhase) __init__ should create a MissionPhase data model.
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertEqual(self.DUT.dicPhase, {})
        self.assertTrue(isinstance(self.DUT.dao, DAO))

        self.assertEqual(self.DUT.last_id, None)

    @attr(all=True, unit=True)
    def test01a_retrieve_all_phases(self):
        """
        (TestMissionPhase): retrieve_all should return False on success.
        """

        _dic_phases = self.DUT.retrieve_all(self.dao, 1)

        self.assertTrue(isinstance(_dic_phases, dict))
        self.assertTrue(isinstance(_dic_phases[1], RTKMissionPhase))

    @attr(all=True, unit=True)
    def test01b_retrieve_all_phases_nonexistent_mission(self):
        """
        (TestMissionPhase): retrieve_all should return an empty dictionary when passed a Mission ID that doesn't exist.
        """

        self.DUT.retrieve_all(self.dao, 1)

        _dic_phases = self.DUT.retrieve_all(self.dao, 100)

        self.assertEqual(_dic_phases, {})

    @attr(all=True, unit=True)
    def test02a_retrieve_single_phase(self):
        """
        (TestMissionPhase): retrieve should return an instance of the RTKMissionPhase data model on success.
        """

        self.DUT.retrieve_all(self.dao, 1)

        _phase = self.DUT.retrieve(1)

        self.assertTrue(isinstance(_phase, RTKMissionPhase))
        self.assertEqual(_phase.mission_id, 1)
        self.assertEqual(_phase.phase_id, 1)

    @attr(all=True, unit=True)
    def test02b_retrieve_missing_phase(self):
        """
        (TestMissionPhase): retrieve should return None when passed a Phase ID that doesn't exist.
        """

        _phase = self.DUT.retrieve(100)

        self.assertEqual(_phase, None)

    @attr(all=True, unit=True)
    def test03a_add_phase(self):
        """
        (TestMissionPhase): add_phase should return False on success.
        """

        _phase = self.DUT.add_phase(1)

        self.assertTrue(isinstance(_phase, RTKMissionPhase))
        self.assertEqual(_phase.mission_id, 1)

    @attr(all=True, unit=True)
    def test04a_delete_phase(self):
        """
        (TestMissionPhase): delete_phase should return False on success.
        """

        self.DUT.retrieve_all(self.dao, 1)

        self.assertFalse(self.DUT.delete_phase(7))

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_phase_id(self):
        """
        (TestMissionPhase): delete_phase should return True when passed a Phase ID that doesn't exist.
        """

        self.DUT.retrieve_all(self.dao, 1)

        self.assertTrue(self.DUT.delete_phase(100))

    @attr(all=True, unit=True)
    def test_05a_save_phase(self):
        """
        (TestMissionPhase): save_phase should return False on success.
        """

        self.DUT.retrieve_all(self.dao, 1)

        _phase = self.DUT.dicPhase[1]
        _phase.description = 'Phase to save'

        self.assertFalse(self.DUT.save_phase(1))

    @attr(all=True, unit=True)
    def test_05b_save_non_existent_phase(self):
        """
        (TestMissionPhase): save_phase should return True when passed a Phase ID that doesn't exist.
        """

        self.DUT.retrieve_all(self.dao, 1)

        self.assertTrue(self.DUT.save_phase(100))

    @attr(all=True, unit=True)
    def test_06a_save_all_phases(self):
        """
        (TestMissionPhase): save_all_phases should return False on success.
        """

        self.assertFalse(self.DUT.save_all_phases())


class Test01MissionPhaseController(unittest.TestCase):
    """
    Class for testing the Mission Phase Data Controller class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Mission Phase Data Controller.
        """

        # Create a data access object and connect to a test database.
        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestDB.rtk')
        self.dao.db_add(RTKMissionPhase())
        self.dao.db_add(RTKMissionPhase())

        self.DUT = Phase()

        Configuration.DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/RTK_debug.log')
        Configuration.USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                        '/tmp/RTK_user.log')

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """
        (TestRevision) __init__ should return a Mission Phase Data Controller
        """

        self.assertTrue(isinstance(self.DUT, Phase))

