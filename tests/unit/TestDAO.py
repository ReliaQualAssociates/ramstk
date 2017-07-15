1#!/usr/bin/env python -O
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
import os
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session

import Configuration as Configuration
import Utilities as Utilities
from dao.RTKCommonDB import Session
from dao.DAO import DAO
from dao.RTKRevision import RTKRevision
from dao.RTKMission import RTKMission
from dao.RTKMissionPhase import RTKMissionPhase
from dao.RTKEnvironment import RTKEnvironment

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
        self.DUT.db_connect('sqlite:////tmp/TestDB.rtk')

        Session.configure(bind=self.DUT.engine, autoflush=False,
                          expire_on_commit=False)
        self.session = scoped_session(Session)

        self._revision = self.session.query(RTKRevision).first()
        self._mission = self.session.query(RTKMission).\
            filter(RTKMission.revision_id ==
                   self._revision.revision_id).first()
        self._phase = self.session.query(RTKMissionPhase).\
            filter(RTKMissionPhase.mission_id ==
                   self._mission.mission_id).first()
        self._environment = self.session.query(RTKEnvironment).\
            filter(RTKEnvironment.phase_id ==
                   self._phase.phase_id).first()

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

    @attr(all=True, unit=True)
    def test01_dao_db_connect(self):
        """
        (TestDAO) db_connect should return False on success connecting to an SQLite database.
        """

        _database = 'sqlite:////tmp/TestDB.rtk'
        _dao = DAO('')

        self.assertFalse(_dao.db_connect(_database))

    @attr(all=True, unit=True)
    def test02a_dao_db_create_common(self):
        """
        (TestDAO) db_create_common should return False on success.
        """

        _database = 'sqlite:////tmp/_rtk_common_db.rtk'
        self.DUT.db_connect(_database)

        self.assertFalse(self.DUT.db_create_common(_database, self.session))

        os.remove('/tmp/_rtk_common_db.rtk')

    @attr(all=True, unit=True)
    def test02b_dao_db_create_program(self):
        """
        (TestDAO) db_create_program should return False on success.
        """

        _database = 'sqlite:////tmp/_rtk_program_db.rtk'
        self.DUT.db_connect(_database)

        self.assertFalse(self.DUT.db_create_program(_database, self.session))

        os.remove('/tmp/_rtk_program_db.rtk')

    @attr(all=True, unit=True)
    def test03a_dao_db_add(self):
        """
        (TestDAO) db_add should return a zero error code on success when adding a single record to the database.
        """

        (_error_code, _msg) = self.DUT.db_add([RTKRevision(), ], self.session)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding one or more items to the RTK Program database.")

    @attr(all=True, unit=True)
    def test03b_dao_db_add_no_item(self):
        """
        (TestDAO) db_add should return a 1003 error code on failure.
        """

        (_error_code, _msg) = self.DUT.db_add([None, ], self.session)

        self.assertEqual(_error_code, 1003)
        self.assertEqual(_msg,
                         "RTK ERROR: Adding one or more items to the RTK Program database.")

    @attr(all=True, unit=True)
    def test04_dao_db_add_many(self):
        """
        (TestDAO) db_add should return a zero error code on success when adding multiple records to the database.
        """

        _mission = RTKMission()
        _mission.revision_id = self._revision.revision_id
        _phase = RTKMissionPhase()
        _phase.mission_id = self._mission.mission_id
        _environment = RTKEnvironment()
        _environment.phase_id = self._phase.phase_id

        (_error_code, _msg) = self.DUT.db_add([_mission, _phase, _environment],
                                              self.session)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding one or more items to the RTK Program database.")

    @attr(all=True, unit=True)
    def test05_dao_db_update(self):
        """
        (TestDAO) db_update should return a zero error code on success.
        """

        self._revision.availability_logistics = 0.9959
        self._revision.availability_mission = 0.9999
        self._mission.description = 'Big mission'

        (_error_code, _msg) = self.DUT.db_update(self.session)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Updating the RTK Program database.")

    @attr(all=True, unit=True)
    def test06a_dao_db_delete(self):
        """
        (TestDAO) db_delete should return a zero error code on success.
        """

        (_error_code, _msg) = self.DUT.db_delete(self._environment,
                                                 self.session)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Deleting an item from the RTK Program database.")

    @attr(all=True, unit=True)
    def test06b_dao_db_delete_no_item(self):
        """
        (TestDAO) db_delete should return a 1005 error code on failure.
        """

        (_error_code, _msg) = self.DUT.db_delete(None, self.session)

        self.assertEqual(_error_code, 1005)
        self.assertEqual(_msg,
                         "RTK ERROR: Deleting an item from the RTK Program database.")
