#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._hardware.TestDesignMechanic.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing DesignMechanic module algorithms and models."""

import sys
from os.path import dirname

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import Utilities as Utilities  # pylint: disable=import-error
from Configuration import Configuration  # pylint: disable=import-error
from hardware import dtmDesignMechanic  # pylint: disable=import-error
from dao import DAO  # pylint: disable=import-error
from dao import RTKDesignMechanic  # pylint: disable=import-error

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestDesignMechanicDataModel(unittest.TestCase):
    """Class for testing the DesignMechanic data model class."""

    def setUp(self):
        """(TestDesignMechanic) Set up the test fixture for the DesignMechanic class."""
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

        self.DUT = dtmDesignMechanic(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """(TestDesignMechanicModel) __init__ should return a DesignMechanic model."""
        self.assertTrue(isinstance(self.DUT, dtmDesignMechanic))
        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertTrue(isinstance(self.DUT.dao, DAO))
        self.assertEqual(self.DUT._tag, 'DesignMechanic')

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """(TestDesignMechanicModel) select_all() should return a Tree() object populated with RTKDesignMechanic instances on success."""
        _tree = self.DUT.select_all(2)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertTrue(isinstance(_tree.get_node(2).data, RTKDesignMechanic))

    @attr(all=True, unit=True)
    def test02a_select(self):
        """(TestDesignMechanicModel) select() should return an instance of the RTKDesignMechanic data model on success."""
        self.DUT.select_all(2)
        _design_mechanic = self.DUT.select(2)

        self.assertTrue(isinstance(_design_mechanic, RTKDesignMechanic))
        self.assertEqual(_design_mechanic.hardware_id, 2)
        self.assertEqual(_design_mechanic.lubrication_id, 0)

    @attr(all=True, unit=True)
    def test02b_select_non_existent_id(self):
        """(TestDesignMechanicModel) select() should return None when a non-existent DesignMechanic ID is requested."""
        _design_electric = self.DUT.select(100)

        self.assertEqual(_design_electric, None)

    @attr(all=True, unit=True)
    def test03a_insert(self):
        """(TestDesignMechanicModel) insert() should return False on success when inserting a DesignMechanic record."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.insert(hardware_id=4)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Adding one or more items to '
                         'the RTK Program database.')

    @attr(all=True, unit=True)
    def test04a_delete(self):
        """(TestDesignMechanicModel) delete() should return a zero error code on success."""
        self.DUT.select_all(4)

        _error_code, _msg = self.DUT.delete(4)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Deleting an item from the RTK '
                         'Program database.')

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_id(self):
        """(TestDesignMechanicModel) delete() should return a non-zero error code when passed a DesignMechanic ID that doesn't exist."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.delete(300)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg, '  RTK ERROR: Attempted to delete non-existent '
                         'DesignMechanic record ID 300.')

    @attr(all=True, unit=True)
    def test05a_update(self):
        """(TestDesignMechanicModel) update() should return a zero error code on success."""
        self.DUT.select_all(3)

        _design_electric = self.DUT.select(3)
        _design_electric.resistance = 0.9832

        _error_code, _msg = self.DUT.update(3)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')

    @attr(all=True, unit=True)
    def test05b_update_non_existent_id(self):
        """(TestDesignMechanicModel) update() should return a non-zero error code when passed a DesignMechanic ID that doesn't exist."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to save non-existent '
                         'DesignMechanic record ID 100.')

    @attr(all=True, unit=True)
    def test06a_update_all(self):
        """(TestDesignMechanicModel) update_all() should return a zero error code on success."""
        self.DUT.select_all(3)

        _error_code, _msg = self.DUT.update_all()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating the RTK Program database.')
