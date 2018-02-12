#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       rtk.tests.usage.TestProfile.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for Usage Profile algorithms and models."""

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree

import rtk.Utilities as Utilities
from rtk.Configuration import Configuration
from rtk.dao import DAO
from rtk.dao import RTKRevision
from rtk.dao import RTKMission
from rtk.dao import RTKMissionPhase
from rtk.dao import RTKEnvironment
from rtk.usage import (dtmEnvironment, dtmMission, dtmMissionPhase,
                       dtmUsageProfile, dtcUsageProfile)

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Doyle "Weibullguy" Rowland'


class TestUsageProfileDataModel(unittest.TestCase):
    """
    Class for testing the Usage Profile model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the USage Profile class.
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

        self.DUT = dtmUsageProfile(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """(TestUsageProfileModel) __init__() should create a Usage Profile data model."""
        self.assertTrue(isinstance(self.DUT, dtmUsageProfile))

        self.assertTrue(isinstance(self.DUT.dtm_mission, dtmMission))
        self.assertTrue(isinstance(self.DUT.dtm_phase, dtmMissionPhase))
        self.assertTrue(isinstance(self.DUT.dtm_environment, dtmEnvironment))
        self.assertEqual(self.DUT.last_id, None)

        self.assertTrue(isinstance(self.DUT.tree, Tree))
        self.assertEqual(self.DUT.dao, self.dao)

    @attr(all=True, unit=True)
    def test01a_select_all(self):
        """(TestUsageProfileModel): select_all() should return an empty Tree() when passed a Revision ID that doesn't exist."""
        _tree = self.DUT.select_all(1)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertEqual(_tree.get_node(0).tag, 'Usage Profiles')
        self.assertTrue(isinstance(_tree.get_node(1).data, RTKMission))
        self.assertTrue(isinstance(_tree.get_node(11).data, RTKMissionPhase))
        self.assertTrue(isinstance(_tree.get_node(111).data, RTKEnvironment))

    @attr(all=True, unit=True)
    def test01b_select_all_non_existent_id(self):
        """(TestUsageProfileModel): select_all() should return an empty Tree() when passed a Revision ID that doesn't exist."""
        _tree = self.DUT.select_all(100)

        self.assertTrue(isinstance(_tree, Tree))
        self.assertEqual(_tree.get_node(0).tag, 'Usage Profiles')
        self.assertEqual(_tree.get_node(1), None)

    @attr(all=True, unit=True)
    def test02a_select(self):
        """(TestUsageProfileModel): select() should return a Tree() on success."""
        self.DUT.select_all(1)

        _entity = self.DUT.select(1)

        self.assertTrue(isinstance(_entity, RTKMission))
        self.assertEqual(_entity.description, 'Test Mission Description')

    @attr(all=True, unit=True)
    def test03a_insert_mission(self):
        """(TestUsageProfileModel): insert() should return a zero error code on success when adding a new Mission."""
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.insert(1, 0, 'mission')

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "RTK SUCCESS: Adding one or more items to the RTK "
                         "Program database.")

        self.assertTrue(isinstance(self.DUT.tree.get_node(2).data, RTKMission))

        self.DUT.delete(self.DUT._dtm_data_model.dtm_mission.last_id)

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

        self.assertTrue(
            isinstance(self.DUT.tree.get_node(12).data, RTKMissionPhase))

        self.DUT.delete(self.DUT._dtm_data_model.dtm_mission_phase.last_id)

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

        self.assertTrue(
            isinstance(self.DUT.tree.get_node(112).data, RTKEnvironment))

        self.DUT.delete(self.DUT._dtm_data_model.dtm_environment.last_id)

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
        (TestUsageProfileModel): delete() should return a 2005 error code when attempting to remove a non-existant item from the Profile.
        """
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.delete(4)

        self.assertEqual(_error_code, 2005)
        self.assertEqual(_msg,
                         "  RTK ERROR: Attempted to delete non-existent " \
                         "Usage Profile entity with Node ID 4.")

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
        (TestUsageProfileModel): update() should return a 2006 error code when attempting to update a non-existent Node ID.
        """
        self.DUT.select_all(1)

        _error_code, _msg = self.DUT.update(100)

        self.assertEqual(_error_code, 2006)
        self.assertEqual(_msg,
                         "RTK ERROR: Attempted to save non-existent Usage " \
                         "Profile entity with Node ID 100.")

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


class TestUsageProfileDataController(unittest.TestCase):
    """
    Class for testing the Usage Profile controller class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Mission Data Controller.
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

        self.dao.RTK_SESSION.configure(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)

        self.DUT = dtcUsageProfile(self.dao, self.Configuration, test='True')

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestUsageProfileController) __init__() should create an instance of a UsageProfile data controller.
        """

        self.assertTrue(isinstance(self.DUT, dtcUsageProfile))
        self.assertTrue(isinstance(self.DUT._dtm_data_model, dtmUsageProfile))

    @attr(all=True, unit=True)
    def test01a_request_select_all(self):
        """
        (TestUsageProfileController) request_select_all() should return a treelib Tree() with the Usage Profile.
        """

        self.assertTrue(isinstance(self.DUT.request_select_all(1), Tree))

    @attr(all=True, unit=True)
    def test03a_request_insert_mission(self):
        """(TestUsageProfileController) request_insert() should return False on success."""
        self.DUT.request_select_all(1)
        self.assertFalse(self.DUT.request_insert(1, 0, 'mission'))

        self.DUT.request_delete(self.DUT.request_last_id('mission'))

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
    def test05a_request_get_attributes(self):
        """
        (TestUsageProfileController) request_get_attributes() should return a dict of {attribute name:attribute value} pairs.
        """
        self.DUT.request_select_all(1)

        _attributes = self.DUT.request_get_attributes(1)

        self.assertTrue(isinstance(_attributes, dict))
        self.assertEqual(_attributes['revision_id'], 1)

    @attr(all=True, unit=True)
    def test05b_request_set_attributes(self):
        """(TestUsageProfileController) request_set_attributes() should return a zero error code on success."""
        self.DUT.request_select_all(1)

        _attributes = {
            'mission_id': 1,
            'revision_id': 1,
            'mission_time': 72.0,
            'description': 'Test Mission Description',
            'time_units': u'minutes'
        }

        _error_code, _msg = self.DUT.request_set_attributes(1, _attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         'RTK SUCCESS: Updating RTKMission 1 attributes.')

    @attr(all=True, unit=True)
    def test05c_request_last_mission_id(self):
        """
        (TestUsageProfileController) request_last_id() should return the last Mission ID used in the RTK Program database.
        """
        self.DUT.request_select_all(1)

        _last_id = self.DUT.request_last_id('mission')

        self.assertEqual(_last_id, 1)

    @attr(all=True, unit=True)
    def test05d_request_last_mission_phase_id(self):
        """
        (TestUsageProfileController) request_last_id() should return the last Mission Phase ID used in the RTK Program database.
        """
        self.DUT.request_select_all(1)

        _last_id = self.DUT.request_last_id('phase')

        self.assertEqual(_last_id, 1)

    @attr(all=True, unit=True)
    def test05e_request_last_environment_id(self):
        """
        (TestUsageProfileController) request_last_id() should return the last Environment ID used in the RTK Program database.
        """
        self.DUT.request_select_all(1)

        _last_id = self.DUT.request_last_id('environment')

        self.assertEqual(_last_id, 1)

    @attr(all=True, unit=True)
    def test06a_request_update_all(self):
        """
        (TestUsageProfileController) request_update_all() should return False on success.
        """

        self.DUT.request_select_all(1)

        self.assertFalse(self.DUT.request_update_all())
