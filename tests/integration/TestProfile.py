#!/usr/bin/env python -O
"""
This is the test class for testing the Usage Profile module algorithms and
models.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.TestProfile.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from usage.UsageProfile import UsageProfile
from usage.Mission import Model as Mission
from usage.Phase import Model as Phase
from usage.Environment import Model as Environment

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestUsageProfileController(unittest.TestCase):
    """
    Class for testing the Usage Profile controller class.
    """

    def setUp(self):

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = UsageProfile()
        self.DUT._dao = self._dao

    @attr(all=True, integration=True)
    def test00_request_profile(self):
        """
        (TestProfile) request_profile should return False on success
        """

        self.assertFalse(self.DUT.request_profile(0, self._dao))

    @attr(all=True, integration=True)
    def test01_add_mission(self):
        """
        (TestProfile) add_mission should return (True, 0, last_id) on success
        """

        self.DUT.request_profile(0, self._dao)

        (_results, _error_code, _last_id) = self.DUT.add_mission(0)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

        _mission = self.DUT.dicProfiles[0].dicMissions[_last_id]
        self.assertTrue(isinstance(_mission, Mission))

    @attr(all=True, integration=True)
    def test02_save_mission(self):
        """
        (TestProfile) _save_mission should return a 0 error code on success
        """

        self.DUT.request_profile(0, self._dao)
        _mission = self.DUT.dicProfiles[0].dicMissions[0]

        _error_code = self.DUT._save_mission(_mission)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test03_delete_mission(self):
        """
        (TestProfile) delete_mission should return (True, 0) on success
        """

        self.DUT.request_profile(0, self._dao)
        _n = len(self.DUT.dicProfiles[0].dicMissions)

        (_results, _error_code) = self.DUT.delete_mission(0, _n - 1)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test04_add_phase(self):
        """
        (TestProfile) add_phase should return (True, 0, last_id) on success
        """

        self.DUT.request_profile(0, self._dao)

        (_results, _error_code, _last_id) = self.DUT.add_phase(0, 0)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

        _phase = self.DUT.dicProfiles[0].dicMissions[0].dicPhases[_last_id]
        self.assertTrue(isinstance(_phase, Phase))

    @attr(all=True, integration=True)
    def test05_save_phase(self):
        """
        (TestProfile) _save_phase should return (True, 0) on success
        """

        self.DUT.request_profile(0, self._dao)
        _phase = self.DUT.dicProfiles[0].dicMissions[0].dicPhases[1]

        (_results, _error_code) = self.DUT._save_phase(_phase)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test06_delete_phase(self):
        """
        (TestProfile) delete_phase should return (True, 0) on success
        """

        self.DUT.request_profile(0, self._dao)
        _n = len(self.DUT.dicProfiles[0].dicMissions[0].dicPhases)

        (_results, _error_code) = self.DUT.delete_phase(0, 0, _n - 1)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test07_add_environment(self):
        """
        (TestProfile) add_environment should return (True, 0, last_id) on success
        """

        self.DUT.request_profile(0, self._dao)

        (_results, _error_code, _last_id) = self.DUT.add_environment(0, 0, 1)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

        _mission = self.DUT.dicProfiles[0].dicMissions[0]
        _environment = _mission.dicPhases[1].dicEnvironments[_last_id]
        self.assertTrue(isinstance(_environment, Environment))

    @attr(all=True, integration=True)
    def test08_save_environment(self):
        """
        (TestProfile) _save_environment should return (True, 0) on success
        """

        self.DUT.request_profile(0, self._dao)

        _mission = self.DUT.dicProfiles[0].dicMissions[0]
        _environment = _mission.dicPhases[1].dicEnvironments[1]

        (_results, _error_code) = self.DUT._save_environment(_environment)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test09_delete_environment(self):
        """
        (TestProfile) delete_environment should return (True, 0) on success
        """

        self.DUT.request_profile(0, self._dao)
        _mission = self.DUT.dicProfiles[0].dicMissions[0]
        _n = len(_mission.dicPhases[1].dicEnvironments)

        (_results, _error_code) = self.DUT.delete_environment(0, 0, 1, _n - 1)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)
