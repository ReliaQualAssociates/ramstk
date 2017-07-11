#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestDAO.py is part of The RTK Project

#
# All rights reserved.

"""
This is the test class for testing Data Access Object (DAO) module algorithms
and models.
"""

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import Configuration as Configuration
import Utilities as Utilities
from dao.DAO import *

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class TestDAO(unittest.TestCase):
    """
    Class for testing the DAO class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the DAO class.
        """

        self.DUT = DAO('')

        self._revision = RTKRevision()
        self._mission = RTKMission()
        self._mission.revision_id = 1
        self._phase = RTKMissionPhase()
        self._phase.mission_id = 1
        self._environment = RTKEnvironment()
        self._environment.phase_id = 1

        Configuration.DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/rtk_debug.log')
        Configuration.USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                        '/tmp/rtk_user.log')

    @attr(all=True, unit=True)
    def test00_dao_create(self):
        """
        (TestDAO) __init__ should create a DAO class instance.
        """

        self.assertTrue(isinstance(self.DUT, DAO))
        self.assertEqual(self.DUT.engine, None)
        self.assertEqual(self.DUT.metadata, None)

    @attr(all=True, unit=True)
    def test01_dao_db_connect(self):
        """
        (TestDAO) db_connect should return False on success connecting to an SQLite database.
        """

        _database = 'sqlite:////tmp/TestDB.rtk'

        self.assertFalse(self.DUT.db_connect(_database))

    @attr(all=True, unit=True)
    def test02a_dao_db_create_common(self):
        """
        (TestDAO) db_create_common should return False on success.
        """

        _database = 'sqlite:////tmp/_rtk_common_db.rtk'
        self.DUT.db_connect(_database   )

        self.assertFalse(self.DUT.db_create_common(_database))

    @attr(all=True, unit=False)
    def test02b_dao_db_create(self):
        """
        (TestDAO) db_create should return False on success.
        """

        self.assertFalse(self.DUT.db_create())

    @attr(all=True, unit=True)
    def test03a_dao_db_add(self):
        """
        (TestDAO) db_add should return a zero error code on success when adding a single record to the database.
        """

        (_error_code, _msg) = self.DUT.db_add(self._revision)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "SUCCESS: Adding an item to the RTK Program database.")

    @attr(all=True, unit=True)
    def test03b_dao_db_add_no_item(self):
        """
        (TestDAO) db_add should return a 1003 error code on failure.
        """

        (_error_code, _msg) = self.DUT.db_add(None)

        self.assertEqual(_error_code, 1003)
        self.assertEqual(_msg,
                         "ERROR: Adding an item to the RTK Program database.")

    @attr(all=True, unit=True)
    def test04_dao_db_add_many(self):
        """
        (TestDAO) db_add should return a zero error code on success when adding multiple records to the database.
        """

        (_error_code, _msg) = self.DUT.db_add([self._mission, self._phase,
                                               self._environment])

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "SUCCESS: Adding an item to the RTK Program database.")

    @attr(all=True, unit=True)
    def test05_dao_db_update(self):
        """
        (TestDAO) db_update should return a zero error code on success.
        """

        self._revision.availability_logistics = 0.9959
        self._revision.availability_mission = 0.9999
        self._mission.description = 'Big mission'

        (_error_code, _msg) = self.DUT.db_update()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "SUCCESS: Updating the RTK Program database.")

    @attr(all=True, unit=True)
    def test06a_dao_db_delete(self):
        """
        (TestDAO) db_delete should return a zero error code on success.
        """

        _phase = RTKMissionPhase()
        _phase.mission_id = 1

        self.DUT.db_add(_phase)

        (_error_code, _msg) = self.DUT.db_delete(_phase)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "SUCCESS: Deleting an item from the RTK Program database.")

    @attr(all=True, unit=True)
    def test06b_dao_db_delete_no_item(self):
        """
        (TestDAO) db_delete should return a 1005 error code on failure.
        """

        (_error_code, _msg) = self.DUT.db_delete(None)

        self.assertEqual(_error_code, 1005)
        self.assertEqual(_msg,
                         "ERROR: Deleting an item from the RTK Program database.")
