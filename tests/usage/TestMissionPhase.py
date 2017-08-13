#!/usr/bin/env python -O
"""
This is the test class for testing the Phase class.
"""

# -*- coding: utf-8 -*-
#
#       TestPhase.py is part of The RTK Project
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

# We add this to ensure the imports within the rtk packages will work.
import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import Utilities as Utilities
from Configuration import Configuration
from usage.Phase import Model, MissionPhase
from dao import DAO
from dao import RTKMissionPhase

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
        self.dao.db_add([RTKMissionPhase(), ], self.session)
        self.dao.db_add([RTKMissionPhase(), ], self.session)

        self.DUT = Model(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestMissionPhaseModel) __init__() should return a Mission model
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertEqual(self.DUT._last_id, None)
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """
        (TestMissionPhaseModel): select_all() should return a Tree() object populated with RTKMissionPhase instances on success.
        """

        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKMissionPhase))

    @attr(all=True, unit=True)
    def test01b_select_all_non_existent_id(self):
        """
        (TestMissionPhaseModel): select_all() should return an empty Tree() when passed a Mission ID that doesn't exist.
        """

        _tree = self.DUT.select_all(100)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertEqual(len(_tree.all_nodes()), 1)

    @attr(all=True, unit=True)
    def test02a_select(self):
        """
        (TestMissionPhaseModel): select() should return an instance of the RTKMissionPhase data model on success.
        """

        self.DUT.select_all(1)
        _phase = self.DUT.select(1)

        self.assertTrue(isinstance(_phase, RTKMissionPhase))
        self.assertEqual(_phase.phase_id, 1)
        self.assertEqual(_phase.description, '')

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """
        (TestMissionPhaseModel): select() should return None when passed a Phase ID that doesn't exist.
        """

        self.DUT.select_all(1)
        self.assertEqual(self.DUT.select(100), None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """
        (TestMissionPhaseModel): insert() should return False on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                               'the RTK Program database.')
        self.assertEqual(self.DUT._last_id, 2)

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """
        (TestMissionPhaseModel): delete() should return False on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(2)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                               'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """
        (TestMissionPhaseModel): delete() should return True when passed a Phase ID that doesn't exist.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2225)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to delete non-existent '
                               'Mission Phase ID 300.')

    @attr(all=True, unit=True)
    def test_05a_update(self):
        """
        (TestMissionPhaseModel): update() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _phase = self.DUT.tree.get_node(1).data
        _phase.description = 'Test Mission Phase Description'

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test_05b_update_non_existent_id(self):
        """
        (TestMissionPhaseModel): update() should return a non-zero error code when passed a Mission Phase ID that doesn't exist.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2226)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                               'Mission Phase ID 100.')

    @attr(all=True, unit=True)
    def test_06a_update_all(self):
        """

        (TestMissionPhaseModel): update_all() should return a zero error code on success.
        """

        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')


class Test01MissionPhaseController(unittest.TestCase):
    """
    Class for testing the Mission Phase Data Controller class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Mission Phase Data Controller.
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
        self.dao.db_add([RTKMissionPhase(), ], self.session)
        self.dao.db_add([RTKMissionPhase(), ], self.session)

        self.DUT = MissionPhase(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_controller_create(self):
        """
        (TestMissionPhaseController) __init__() should return a Mission Phase Data Controller
        """

        self.assertTrue(isinstance(self.DUT, MissionPhase))
        self.assertTrue(isinstance(self.DUT._dtm_phase, Model))

    @attr(all=True, unit=False)
    def test01_request_select_all(self):
        """
        (TestMissionPhaseController) request_select_all() should return a Tree of RTKMissionPhase models.
        """

        _tree = self.DUT.request_select_all(1)

        self.assertTrue(isinstance(_tree.get_node(1).data, RTKMissionPhase))

    @attr(all=True, unit=False)
    def test02a_request_select(self):
        """
        (TestMissionPhaseController) request_select() should return an RTKv model.
        """

        self.DUT.request_select_all(1)

        self.assertTrue(isinstance(self.DUT.request_select(1), RTKMissionPhase))

    @attr(all=True, unit=False)
    def test02b_request_non_existent_id(self):
        """
        (TestMissionPhaseController) request_select() should return None when requesting a Mission that doesn't exist.
        """

        self.assertEqual(self.DUT.request_select(100), None)

    @attr(all=True, unit=False)
    def test03a_request_insert(self):
        """
        (TestMissionPhaseController) request_insert() should return False on success.
        """

        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_insert(1))

    @attr(all=True, unit=False)
    def test04a_request_delete(self):
        """
        (TestMissionPhaseController) request_delete() should return False on success.
        """

        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_delete(2))

    @attr(all=True, unit=False)
    def test04a_request_delete_non_existent_id(self):
        """
        (TestMissionPhaseController) request_delete() should return True when attempting to delete a non-existent Mission.
        """

        self.DUT.request_select_all(1)
        self.assertTrue(self.DUT.request_delete(100))

    @attr(all=True, unit=False)
    def test05a_request_update(self):
        """
        (TestMissionPhaseController) request_update() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update(1))

    @attr(all=True, unit=False)
    def test05b_request_update_non_existent_id(self):
        """
        (TestMissionPhaseController) request_update() should return True when attempting to save a non-existent Mission.
        """

        self.DUT.request_select_all(1)

        self.assertTrue(self.DUT.request_update(100))

    @attr(all=True, unit=False)
    def test06a_request_update_all(self):
        """
        (TestMissionPhaseController) request_update_all() should return False on success.
        """

        self.DUT.request_select_all(1)

        _error_code, _msg = self.DUT.request_update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')
