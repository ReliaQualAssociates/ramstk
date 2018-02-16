#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       TestPhase.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Mission Phase class."""

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import rtk.Utilities as Utilities
from rtk.Configuration import Configuration
from rtk.usage import dtmMissionPhase
from rtk.dao import DAO
from rtk.dao import RTKMissionPhase

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestMissionPhaseDataModel(unittest.TestCase):
    """
    Class for testing the Phase model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Phase model class.
        """
        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {
            'host': 'localhost',
            'socket': 3306,
            'database': '/tmp/TestDB.rtk',
            'user': '',
            'password': ''
        }

        self.Configuration.DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG', '/tmp/RTK_debug.log')
        self.Configuration.USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO', '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)

        self.DUT = dtmMissionPhase(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestMissionPhaseModel) __init__() should return a Mission model
        """
        self.assertTrue(isinstance(self.DUT, dtmMissionPhase))
        self.assertEqual(self.DUT.last_id, None)
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
        self.assertEqual(_phase.description, 'Test Mission Phase')

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """
        (TestMissionPhaseModel): select() should return None when passed a Phase ID that doesn't exist.
        """
        self.DUT.select_all(1)
        self.assertEqual(self.DUT.select(100), None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """(TestMissionPhaseModel): insert() should return False on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(mission_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 2)

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

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
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

        self.assertEqual(_error_code, 2006)
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
