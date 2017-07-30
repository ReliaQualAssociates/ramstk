1#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestDAO.py is part of The RTK Project

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

from treelib import Tree

from Configuration import Configuration
from dao.RTKCommonDB import RTK_SITE_SESSION, RTK_PROGRAM_SESSION
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

        self.Configuration = Configuration()

        self.Configuration.RTK_SITE_DIR = \
            dirname(dirname(dirname(__file__))) + '/config'
        self.Configuration.RTK_HOME_DIR = '/tmp/RTK'
        self.Configuration.set_site_variables()
        self.Configuration.set_user_variables()
        self.Configuration.create_user_configuration()

        self.Configuration.RTK_COM_BACKEND = 'sqlite'
        self.Configuration.RTK_COM_INFO = {'host'    : 'localhost',
                                           'socket'  : 3306,
                                           'database': '/tmp/TestCommonDB.rtk',
                                           'user'    : '',
                                           'password': ''}
        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {'host'    : 'localhost',
                                            'socket'  : 3306,
                                            'database': '/tmp/TestDB.rtk',
                                            'user'    : '',
                                            'password': ''}

        self.site_dao = DAO()
        _database = self.Configuration.RTK_COM_BACKEND + ':///' + \
                    self.Configuration.RTK_COM_INFO['database']
        self.site_dao.db_connect(_database)

        RTK_SITE_SESSION.configure(bind=self.site_dao.engine, autoflush=False,
                                   expire_on_commit=False)
        self.site_session = scoped_session(RTK_SITE_SESSION)

        self.DUT = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.DUT.db_connect(_database)

        RTK_PROGRAM_SESSION.configure(bind=self.DUT.engine, autoflush=False,
                                      expire_on_commit=False)
        self.program_session = scoped_session(RTK_PROGRAM_SESSION)

        self._revision = self.program_session.query(RTKRevision).first()
        self._mission = self.program_session.query(RTKMission). \
            filter(RTKMission.revision_id ==
                   self._revision.revision_id).first()
        self._phase = self.program_session.query(RTKMissionPhase). \
            filter(RTKMissionPhase.mission_id ==
                   self._mission.mission_id).first()
        self._environment = self.program_session.query(RTKEnvironment). \
            filter(RTKEnvironment.phase_id ==
                   self._phase.phase_id).first()

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

        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        _dao = DAO()

        self.assertFalse(_dao.db_connect(_database))

    @attr(all=True, unit=True)
    def test02a_dao_db_create_common(self):
        """
        (TestDAO) db_create_common should return False on success.
        """

        self.Configuration.RTK_COM_INFO = {'host': 'localhost',
                                           'socket': 3306,
                                           'database': '/tmp/_rtk_common_db.rtk',
                                           'user': '',
                                           'password': ''}
        _database = self.Configuration.RTK_COM_BACKEND + ':///' + \
                    self.Configuration.RTK_COM_INFO['database']
        self.assertFalse(self.DUT.db_create_common(_database,
                                                   self.site_session))

        os.remove('/tmp/_rtk_common_db.rtk')

    @attr(all=True, unit=True)
    def test02b_dao_db_create_common_bad_db_name(self):
        """
        (TestDAO) db_create_common should return True on failure.
        """

        self.Configuration.RTK_COM_INFO = {'host': 'localhost',
                                           'socket': 3306,
                                           'database': 'tmp/_rtk_common_db.rtk',
                                           'user': '',
                                           'password': ''}
        _database = self.Configuration.RTK_COM_BACKEND + ':///' + \
                    self.Configuration.RTK_COM_INFO['database']
        self.assertTrue(self.DUT.db_create_common(_database,
                                                  self.program_session))

    @attr(all=True, unit=True)
    def test02c_dao_db_create_program(self):
        """
        (TestDAO) db_create_program should return False on success.
        """

        self.Configuration.RTK_PROG_INFO = {'host' : 'localhost',
                                            'socket' : 3306,
                                            'database' : '/tmp/_rtk_program_db.rtk',
                                            'type' : 'sqlite',
                                            'user' : '',
                                            'password' : ''}
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.assertFalse(self.DUT.db_create_program(_database,
                                                    self.program_session))

        os.remove('/tmp/_rtk_program_db.rtk')

    @attr(all=True, unit=True)
    def test02d_dao_db_create_program_bad_db_name(self):
        """
        (TestDAO) db_create_program should return True on failure.
        """

        self.Configuration.RTK_PROG_INFO = {'host' : 'localhost',
                                            'socket' : 3306,
                                            'database' : 'tmp/_rtk_program_db.rtk',
                                            'type' : 'sqlite',
                                            'user' : '',
                                            'password' : ''}
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.assertTrue(self.DUT.db_create_program(_database,
                                                   self.program_session))

    @attr(all=True, unit=True)
    def test03a_dao_db_add(self):
        """
        (TestDAO) db_add should return a zero error code on success when adding a single record to the database.
        """

        (_error_code, _msg) = self.DUT.db_add([RTKRevision(), ],
                                              self.program_session)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Adding one or more items to " \
                               "the RTK Program database.")

    @attr(all=True, unit=True)
    def test03b_dao_db_add_no_item(self):
        """
        (TestDAO) db_add should return a 1003 error code on failure.
        """

        (_error_code, _msg) = self.DUT.db_add([None, ],
                                              self.program_session)

        self.assertEqual(_error_code, 1003)
        self.assertEqual(_msg, "RTK ERROR: Adding one or more items to " \
                               "the RTK Program database.")

    @attr(all=True, unit=False)
    def test04_dao_db_add_many(self):
        """
        (TestDAO) db_add should return a zero error code on success when adding multiple records to the database.
        """

        _mission = RTKMission()
        _mission.revision_id = self._revision.revision_id
        _mission.mission_id = 1
        _phase = RTKMissionPhase()
        _phase.mission_id = _mission.mission_id
        _phase.phase_id = 1
        _environment = RTKEnvironment()
        _environment.phase_id = _phase.phase_id
        _environment.environment_id = 1

        (_error_code, _msg) = self.DUT.db_add([_mission, _phase, _environment],
                                              self.program_session)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Adding one or more items to " \
                               "the RTK Program database.")

    @attr(all=True, unit=True)
    def test05_dao_db_update(self):
        """
        (TestDAO) db_update should return a zero error code on success.
        """

        self._revision.availability_logistics = 0.9959
        self._revision.availability_mission = 0.9999
        self._mission.description = 'Big mission'

        (_error_code, _msg) = self.DUT.db_update(self.program_session)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating the RTK Program " \
                               "database.")

    @attr(all=True, unit=True)
    def test06a_dao_db_delete(self):
        """
        (TestDAO) db_delete should return a zero error code on success.
        """

        (_error_code, _msg) = self.DUT.db_delete(self._environment,
                                                 self.program_session)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Deleting an item from the RTK " \
                               "Program database.")

    @attr(all=True, unit=True)
    def test06b_dao_db_delete_no_item(self):
        """
        (TestDAO) db_delete should return a 1005 error code on failure.
        """

        (_error_code, _msg) = self.DUT.db_delete(None, self.program_session)

        self.assertEqual(_error_code, 1005)
        self.assertEqual(_msg, "RTK ERROR: Deleting an item from the RTK " \
                               "Program database.")
