#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._hardware.TestMilHdbkF.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing MilHdbkF module algorithms and models."""

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import rtk.Utilities as Utilities
from rtk.Configuration import Configuration
from rtk.hardware import dtmMilHdbkF
from rtk.dao import DAO
from rtk.dao import RTKMilHdbkF

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestMilHdbkFDataModel(unittest.TestCase):
    """Class for testing the MilHdbkF data model class."""

    def setUp(self):
        """(TestMilHdbkFDataModel) Set up the test fixture for the MilHdbkF class."""
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

        self.DUT = dtmMilHdbkF(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """(TestMilHdbkFDataModel) __init__ should return a MilHdbkF model."""
        self.assertTrue(isinstance(self.DUT, dtmMilHdbkF))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))
        self.assertEqual(self.DUT._tag, 'MilHdbkF')

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """(TestMilHdbkFDataModel) select_all() should return a Tree() object populated with RTKMilHdbkF instances on success."""
        _tree = self.DUT.select_all(2)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(2).data, RTKMilHdbkF))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """(TestMilHdbkFDataModel) select() should return an instance of the RTKMilHdbkF data model on success."""
        self.DUT.select_all(2)
        _mil_hdbk_f = self.DUT.select(2)

        self.assertTrue(isinstance(_mil_hdbk_f, RTKMilHdbkF))
        self.assertEqual(_mil_hdbk_f.hardware_id, 2)
        self.assertEqual(_mil_hdbk_f.piA, 0.0)

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """(TestMilHdbkFDataModel) select() should return None when a non-existent MilHdbkF ID is requested."""
        _design_electric = self.DUT.select(100)

        self.assertEqual(_design_electric, None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """(TestMilHdbkFDataModel) insert() should return False on success when inserting a MilHdbkF record."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.insert(hardware_id=4)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """(TestMilHdbkFDataModel) delete() should return a zero error code on success."""
        self.DUT.select_all(4)

        _error_code, _msg = self.DUT.delete(4)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """(TestMilHdbkFDataModel) delete() should return a non-zero error code when passed a MilHdbkF ID that doesn't exist."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                         'MilHdbkF record ID 300.')

    @attr(all=True, unit=True)
    def test05a_update(self):
        """(TestMilHdbkFDataModel) update() should return a zero error code on success."""
        self.DUT.select_all(3)

        _design_electric = self.DUT.select(3)
        _design_electric.piV = 0.9832

        _error_code, _msg = self.DUT.update(3)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test05b_update_non_existent_id(self):
        """(TestMilHdbkFDataModel) update() should return a non-zero error code when passed a MilHdbkF ID that doesn't exist."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'MilHdbkF record ID 100.')

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """(TestMilHdbkFDataModel) update_all() should return a zero error code on success."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')
