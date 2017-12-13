#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestHardware.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hardware module algorithms and models."""

import sys
from os.path import dirname

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import Utilities as Utilities  # pylint: disable=import-error
from Configuration import Configuration  # pylint: disable=import-error
from hardware import dtmHardware  # pylint: disable=import-error
from dao import DAO  # pylint: disable=import-error
from dao import RTKHardware  # pylint: disable=import-error

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestHardwareDataModel(unittest.TestCase):
    """Class for testing the Hardware data model class."""

    def setUp(self):
        """(TestHardware) Set up the test fixture for the Hardware class."""
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

        self.DUT = dtmHardware(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """(TestHardwareModel) __init__ should return a Hardware model."""
        self.assertTrue(isinstance(self.DUT, dtmHardware))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """(TestHardwareModel) select_all() should return a Tree() object populated with RTKHardware instances on success."""
        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKHardware))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """(TestHardwareModel) select() should return an instance of the RTKHardware data model on success."""
        self.DUT.select_all(1)
        _hardware = self.DUT.select(1)

        self.assertTrue(isinstance(_hardware, RTKHardware))
        self.assertEqual(_hardware.hardware_id, 1)
        self.assertEqual(_hardware.cage_code, '')

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """(TestHardwareModel) select() should return None when a non-existent Hardware ID is requested."""
        _hardware = self.DUT.select(100)

        self.assertEqual(_hardware, None)

    @attr(all=True, unit=True)
    def test03a_insert_sibling(self):
        """(TestHardwareModel) insert() should return False on success when inserting a sibling Hardware."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(revision_id=1, parent_id=0)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 4)

        self.DUT.delete(self.DUT.last_id)

    @attr(all=True, unit=True)
    def test03b_insert_child(self):
        """(TestHardwareModel) insert() should return False on success when inserting a child Hardware."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(revision_id=1, parent_id=1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 4)

        self.DUT.delete(self.DUT.last_id)

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """(TestHardwareModel) delete() should return a zero error code on success."""
        self.DUT.select_all(1)
        self.DUT.insert(revision_id=1, parent_id=1)

        _error_code, _msg = self.DUT.delete(self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """(TestHardwareModel) delete() should return a non-zero error code when passed a Hardware ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                         'Hardware ID 300.')

    @attr(all=True, unit=True)
    def test_05a_update(self):
        """(TestHardwareModel) update() should return a zero error code on success."""
        self.DUT.select_all(1)

        _hardware = self.DUT.tree.get_node(1).data
        _hardware.availability_logistics = 0.9832

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test_05b_update_non_existent_id(self):
        """(TestHardwareModel) update() should return a non-zero error code when passed a Hardware ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'Hardware ID 100.')

    @attr(all=True, unit=True)
    def test_06a_update_all(self):
        """(TestHardwareModel) update_all() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')
