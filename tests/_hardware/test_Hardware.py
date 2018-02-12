#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._hardware.TestHardware.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hardware module algorithms and models."""

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import rtk.Utilities as Utilities
from rtk.Configuration import Configuration
from rtk.hardware import dtmHardware, dtmDesignElectric
from rtk.dao import DAO
from rtk.dao import RTKHardware

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
        """(TestHardwareDataModel) __init__ should return a Hardware model."""
        self.assertTrue(isinstance(self.DUT, dtmHardware))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))
        self.assertEqual(self.DUT._tag, 'Hardware')

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """(TestHardwareDataModel) select_all() should return a Tree() object populated with RTKHardware instances on success."""
        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKHardware))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """(TestHardwareDataModel) select() should return an instance of the RTKHardware data model on success."""
        self.DUT.select_all(1)
        _hardware = self.DUT.select(1)

        self.assertTrue(isinstance(_hardware, RTKHardware))
        self.assertEqual(_hardware.hardware_id, 1)
        self.assertEqual(_hardware.cage_code, '')

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """(TestHardwareDataModel) select() should return None when a non-existent Hardware ID is requested."""
        _hardware = self.DUT.select(100)

        self.assertEqual(_hardware, None)

    @attr(all=True, unit=True)
    def test03a_insert_sibling_assembly(self):
        """(TestHardwareDataModel) insert() should return False on success when inserting a sibling Hardware assembly."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(revision_id=1, parent_id=0, part=0)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 4)

        self.DUT.delete(self.DUT.last_id)

    @attr(all=True, unit=True)
    def test03b_insert_child_assembly(self):
        """(TestHardwareDataModel) insert() should return False on success when inserting a child Hardware assembly."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(revision_id=1, parent_id=1, part=0)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')
        self.assertEqual(self.DUT.last_id, 4)

        self.DUT.delete(self.DUT.last_id)

    @attr(all=True, unit=True)
    def test04a_delete_assembly(self):
        """(TestHardwareDataModel) delete() should return a zero error code on success when deleting a Hardware assembly."""
        self.DUT.select_all(1)
        self.DUT.insert(revision_id=1, parent_id=1, part=0)

        _error_code, _msg = self.DUT.delete(self.DUT.last_id)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_assembly_non_existent_id(self):
        """(TestHardwareDataModel) delete() should return a non-zero error code when passed a Hardware assembly with an ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                         'Hardware ID 300.')

    @attr(all=True, unit=True)
    def test05a_update(self):
        """(TestHardwareDataModel) update() should return a zero error code on success."""
        self.DUT.select_all(1)

        _hardware = self.DUT.tree.get_node(1).data
        _hardware.availability_logistics = 0.9832

        _error_code, _msg = self.DUT.update(1)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test05b_update_non_existent_id(self):
        """(TestHardwareDataModel) update() should return a non-zero error code when passed a Hardware ID that doesn't exist."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'Hardware ID 100.')

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """(TestHardwareDataModel) update_all() should return a zero error code on success."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test07a_make_composite_reference_designator(self):
        """(TestHardwareDataModel) make_composite_ref_des() should return False on success."""
        self.DUT.select_all(1)

        self.assertFalse(self.DUT.make_composite_ref_des())
