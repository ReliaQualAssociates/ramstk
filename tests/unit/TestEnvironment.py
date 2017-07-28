#!/usr/bin/env python -O
"""
This is the test class for testing the Environment class.
"""

# -*- coding: utf-8 -*-
#
#       TestEnvironment.py is part of The RTK Project
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

import unittest
from nose.plugins.attrib import attr

# We add this to ensure the imports within the rtk packages will work.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import Configuration as Configuration
import Utilities as Utilities
from usage.Environment import Model, Environment
from dao.DAO import DAO, RTKRevision, RTKMission, RTKMissionPhase, \
    RTKEnvironment

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestEnvironmentModel(unittest.TestCase):
    """
    Class for testing the Environment model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Environment model class.
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

        _environment = RTKEnvironment()
        _environment.phase_id = _phase.phase_id
        self.dao.db_add(_environment)

        self.DUT = Model()
        self.DUT.dao = self.dao

        Configuration.DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/RTK_debug.log')
        Configuration.USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                        '/tmp/RTK_user.log')

    @attr(all=True, unit=True)
    def test00_environment_create(self):
        """
        (TestEnvironment) __init__ should create an Environment data model.
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertEqual(self.DUT.dicEnvironment, {})
        self.assertTrue(isinstance(self.DUT.dao, DAO))

        self.assertEqual(self.DUT.last_id, None)

    @attr(all=True, unit=True)
    def test01a_retrieve_all_environments(self):
        """
        (TestEnvironment): retrieve_all should return False on success.
        """

        _dic_environments = self.DUT.retrieve_all(self.dao, 1)

        self.assertTrue(isinstance(_dic_environments, dict))
        self.assertTrue(isinstance(_dic_environments[1], RTKEnvironment))

    @attr(all=True, unit=True)
    def test01b_retrieve_all_environments_nonexistent_phase(self):
        """
        (TestEnvironment): retrieve_all should return an empty dictionary when passed a Pase ID that doesn't exist.
        """

        self.DUT.retrieve_all(self.dao, 1)

        _dic_environments = self.DUT.retrieve_all(self.dao, 100)

        self.assertEqual(_dic_environments, {})

    @attr(all=True, unit=True)
    def test02a_retrieve_single_environment(self):
        """
        (TestEnvironment): retrieve should return an instance of the RTKEnvironment data model on success.
        """

        self.DUT.retrieve_all(self.dao, 1)

        _environment = self.DUT.retrieve(1)

        self.assertTrue(isinstance(_environment, RTKEnvironment))
        self.assertEqual(_environment.environment_id, 1)
        self.assertEqual(_environment.phase_id, 1)

    @attr(all=True, unit=True)
    def test02b_retrieve_missing_environment(self):
        """
        (TestEnvironment): retrieve should return None when passed an Environment ID that doesn't exist.
        """

        _environment = self.DUT.retrieve(100)

        self.assertEqual(_environment, None)

    @attr(all=True, unit=True)
    def test03a_add_environment(self):
        """
        (TestEnvironment): add_environment should return False on success.
        """

        _environment = self.DUT.add_environment(1)

        self.assertTrue(isinstance(_environment, RTKEnvironment))
        self.assertEqual(_environment.phase_id, 1)

    @attr(all=True, unit=True)
    def test04a_delete_environment(self):
        """
        (TestEnvironment): delete_environment should return False on success.
        """

        self.DUT.retrieve_all(self.dao, 1)

        self.assertFalse(self.DUT.delete_environment(7))

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_environment_id(self):
        """
        (TestEnvironment): delete_environment should return True when passed a Environment ID that doesn't exist.
        """

        self.DUT.retrieve_all(self.dao, 1)

        self.assertTrue(self.DUT.delete_environment(100))

    @attr(all=True, unit=True)
    def test_05a_save_environment(self):
        """
        (TestEnvironment): save_environment should return False on success.
        """

        self.DUT.retrieve_all(self.dao, 1)

        _environment = self.DUT.dicEnvironment[1]
        _environment.description = 'Environment to save'

        self.assertFalse(self.DUT.save_environment(1))

    @attr(all=True, unit=True)
    def test_05b_save_non_existent_environment(self):
        """
        (TestEnvironment): save_phase should return True when passed a Environment ID that doesn't exist.
        """

        self.DUT.retrieve_all(self.dao, 1)

        self.assertTrue(self.DUT.save_environment(100))

    @attr(all=True, unit=True)
    def test_06a_save_all_environments(self):
        """
        (TestEnvironment): save_all_environments should return False on success.
        """

        self.assertFalse(self.DUT.save_all_environments())
