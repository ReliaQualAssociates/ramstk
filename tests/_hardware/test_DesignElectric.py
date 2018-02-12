#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._hardware.TestDesignElectric.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing DesignElectric module algorithms and models."""

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import rtk.Utilities as Utilities
from rtk.Configuration import Configuration
from rtk.hardware import dtmDesignElectric
from rtk.dao import DAO
from rtk.dao import RTKDesignElectric

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestDesignElectricDataModel(unittest.TestCase):
    """Class for testing the DesignElectric data model class."""

    def setUp(self):
        """(TestDesignElectric) Set up the test fixture for the DesignElectric class."""
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

        self.DUT = dtmDesignElectric(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """(TestDesignElectricDataModel) __init__ should return a DesignElectric model."""
        self.assertTrue(isinstance(self.DUT, dtmDesignElectric))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))
        self.assertEqual(self.DUT._tag, 'DesignElectric')

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """(TestDesignElectricDataModel) select_all() should return a Tree() object populated with RTKDesignElectric instances on success."""
        _tree = self.DUT.select_all(2)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(2).data, RTKDesignElectric))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """(TestDesignElectricDataModel) select() should return an instance of the RTKDesignElectric data model on success."""
        self.DUT.select_all(2)
        _design_electric = self.DUT.select(2)

        self.assertTrue(isinstance(_design_electric, RTKDesignElectric))
        self.assertEqual(_design_electric.hardware_id, 2)
        self.assertEqual(_design_electric.area, 0.0)

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """(TestDesignElectricDataModel) select() should return None when a non-existent DesignElectric ID is requested."""
        _design_electric = self.DUT.select(100)

        self.assertEqual(_design_electric, None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """(TestDesignElectricDataModel) insert() should return False on success when inserting a DesignElectric record."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.insert(hardware_id=4)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """(TestDesignElectricDataModel) delete() should return a zero error code on success."""
        self.DUT.select_all(4)

        _error_code, _msg = self.DUT.delete(4)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """(TestDesignElectricDataModel) delete() should return a non-zero error code when passed a DesignElectric ID that doesn't exist."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                         'DesignElectric record ID 300.')

    @attr(all=True, unit=True)
    def test05a_update(self):
        """(TestDesignElectricDataModel) update() should return a zero error code on success."""
        self.DUT.select_all(3)

        _design_electric = self.DUT.select(3)
        _design_electric.resistance = 0.9832

        _error_code, _msg = self.DUT.update(3)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test05b_update_non_existent_id(self):
        """(TestDesignElectricDataModel) update() should return a non-zero error code when passed a DesignElectric ID that doesn't exist."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'DesignElectric record ID 100.')

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """(TestDesignElectricDataModel) update_all() should return a zero error code on success."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')
