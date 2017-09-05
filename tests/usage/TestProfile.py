#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.usage.TestProfile.py is part of The RTK Project
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

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from dao import DAO
from dao import RTKRevision
from dao import RTKMission
from dao import RTKMissionPhase
from dao import RTKEnvironment
from usage.Mission import Model as Mission
from usage.Phase import Model as Phase
from usage.Environment import Model as Environment
from usage.UsageProfile import Model, UsageProfile

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'


class TestUsageProfileModel(unittest.TestCase):
    """
    Class for testing the Usage Profile model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the USage Profile class.
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
        self.dao.db_add([RTKMission(), ], self.session)
        self.dao.db_add([RTKMission(), ], self.session)

        self.DUT = Model(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestUsageProfileModel) __init__() should create a Usage Profile data model.
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertTrue(isinstance(self.DUT._dtm_mission, Mission))
        self.assertTrue(isinstance(self.DUT._dtm_phase, Phase))
        self.assertTrue(isinstance(self.DUT._dtm_environment, Environment))
        self.assertEqual(self.DUT._last_id, None)

        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertEqual(self.DUT.dao, self.dao)

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """
        (TestUsageProfileModel): select_all() should return an empty Tree() when passed a Revision ID that doesn't exist.
        """

        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertEqual(_tree.get_node(0).tag, 'Usage Profiles')
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKMission))
        self.assertTrue(isinstance(_tree.get_node(11).data, RTKMissionPhase))
        self.assertTrue(isinstance(_tree.get_node(111).data, RTKEnvironment))

    @attr(all=True, unit=True)
    def test01b_select_all_non_existent_id(self):
        """
        (TestUsageProfileModel): select_all() should return an empty Tree() when passed a Revision ID that doesn't exist.
        """

        _tree = self.DUT.select_all(100)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertEqual(_tree.get_node(0).tag, 'Usage Profiles')
        self.assertEqual(_tree.get_node(1), None)

    @attr(all=True, unit=True)
    def test02a_select(self):
        """
        (TestUsageProfileModel): select() should return a Tree() on success.
        """

        self.DUT.select_all(1)

        _entity = self.DUT.select(1)

        self.assertTrue(isinstance(_entity, RTKMission))
        self.assertEqual(_entity.description, 'Description')

    @attr(all=True, unit=True)
    def test03a_insert_mission(self):
        """
        (TestUsageProfileModel): insert() should return a zero error code on success when adding a new Mission.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(1, 0, 'mission')

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding one or more items to the RTK "
                         "Program database.")

        self.assertTrue(isinstance(self.DUT.tree.get_node(2).data, RTKMission))

    @attr(all=True, unit=True)
    def test03b_insert_phase(self):
        """
        (TestUsageProfileModel): insert() should return a zero error code on success when adding a new Mission Phase.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(2, 1, 'phase')

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding one or more items to the RTK "
                         "Program database.")

        self.assertTrue(isinstance(self.DUT.tree.get_node(12).data,
                                   RTKMissionPhase))

    @attr(all=True, unit=True)
    def test03c_insert_environment(self):
        """
        (TestUsageProfileModel): insert() should return a zero error code on success when adding a new Environment.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(2, 11, 'environment')

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding one or more items to the RTK "
                         "Program database.")

        self.assertTrue(isinstance(self.DUT.tree.get_node(112).data,
                                   RTKEnvironment))

    @attr(all=True, unit=True)
    def test03d_insert_non_existent_type(self):
        """
        (TestUsageProfileModel): insert() should return a 2105 error code when attempting to add something other than a Mission, Phase, or Environment.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(1, 0, 'scadamoosh')

        self.assertEqual(_error_code, 2105)
        self.assertEqual(_msg,
                         "RTK ERROR: Attempted to add an item to the Usage " \
                         "Profile with an undefined indenture level.  Level " \
                         "scadamoosh was requested.  Must be one of "
                         "mission, phase, or environment.")

    @attr(all=True, unit=False)
    def test03e_insert_no_parent_in_tree(self):
        """
        (TestUsageProfileModel): insert() should return a 3002 error code when attempting to add something to a non-existant parent Node.
        """

        self.DUT.retrieve_profile(self.dao, 1)

        _error_code, _msg = self.DUT.add_profile(0, 10, 1)

        self.DUT.retrieve_profile(self.dao, 1)

        self.assertEqual(_error_code, 3002)
        self.assertEqual(_msg,
                         "RTK ERROR: Creating a new node in the Usage " \
                         "Profile Tree.")

    @attr(all=True, unit=True)
    def test04a_delete_environment(self):
        """
        (TestUSageProfileModel): delete() should return a zero error code on success when removing an Environment.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(222)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Deleting an item from the RTK Program "
                         "database.")

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_node_id(self):
        """
        (TestUsageProfileModel): delete() should return a 2105 error code when attempting to remove a non-existant item from the Profile.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(4)

        self.assertEqual(_error_code, 2105)
        self.assertEqual(_msg,
                         "RTK ERROR: Attempted to delete a non-existent "
                         "entity with Node ID 4 from the Usage Profile.")

    @attr(all=True, unit=True)
    def test05a_update(self):
        """
        (TestUsageProfileModel): update() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Updating the RTK Program database.")

    @attr(all=True, unit=True)
    def test05a_update_non_existent_node_id(self):
        """
        (TestUsageProfileModel): update() should return a 2106 error code when attempting to update a non-existent Node ID.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2106)
        self.assertEqual(_msg,
                         "RTK ERROR: Attempted to save non-existent Usage "
                         "Profile item with Node ID 100.")

    @attr(all=True, unit=True)
    def test_06a_update_all(self):
        """
        (TestUSageProfileModel): update_all() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')


class TestUsageProfileController(unittest.TestCase):
    """
    Class for testing the Usage Profile controller class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Mission Data Controller.
        """

        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {'host'    : 'localhost',
                                            'socket'  : 3306,
                                            'database': '/tmp/TestDB.rtk',
                                            'user'    : '',
                                            'password': ''}

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

        self.dao.RTK_SESSION.configure(bind=self.dao.engine, autoflush=False,
                                       expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)
        self.dao.db_add([RTKRevision(), ], self.session)
        self.dao.db_add([RTKMission(), ], self.session)
        self.dao.db_add([RTKMissionPhase(), ], self.session)
        self.dao.db_add([RTKEnvironment(), ], self.session)

        self.DUT = UsageProfile(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestUsageProfileController) __init__() should create an instance of a UsageProfile data controller.
        """

        self.assertTrue(isinstance(self.DUT, UsageProfile))
        self.assertTrue(isinstance(self.DUT._dtm_profile, Model))

    @attr(all=True, unit=True)
    def test01a_request_select_all(self):
        """
        (TestUsageProfileController) request_select_all() should return a treelib Tree() with the Usage Profile.
        """

        self.assertTrue(isinstance(self.DUT.request_select_all(1), Tree))

    @attr(all=True, unit=True)
    def test03a_request_insert_mission(self):
        """
        (TestUsageProfileController) request_insert() should return False on success.
        """

        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_insert(1, 0, 'mission'))

    @attr(all=True, unit=True)
    def test04a_request_delete(self):
        """
        (TestUsageProfileController) request_delete() should return False on success.
        """

        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_delete(2))

    @attr(all=True, unit=True)
    def test04a_request_delete_non_existent_id(self):
        """
        (TestUsageProfileController) request_delete() should return True when attempting to delete a non-existent Node ID.
        """

        self.DUT.request_select_all(1)
        self.assertTrue(self.DUT.request_delete(222))

    @attr(all=True, unit=True)
    def test06a_request_update_all(self):
        """
        (TestUsageProfileController) request_update_all() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update_all())
