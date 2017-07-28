1#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestDAO.py is part of The RTK Project

#
# All rights reserved.

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

import Configuration as Configuration
import Utilities as Utilities
from dao.RTKCommonDB import SiteSession, ProgSession
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

        self.site_dao = DAO('')
        self.site_dao.db_connect('sqlite:////tmp/TestCommonDB.rtk')

        SiteSession.configure(bind=self.site_dao.engine, autoflush=False,
                          expire_on_commit=False)
        self.site_session = scoped_session(SiteSession)

        self.DUT = DAO('')
        self.DUT.db_connect('sqlite:////tmp/TestDB.rtk')

        ProgSession.configure(bind=self.DUT.engine, autoflush=False,
                          expire_on_commit=False)
        self.program_session = scoped_session(ProgSession)

        self._revision = self.program_session.query(RTKRevision).first()
        self._mission = self.program_session.query(RTKMission).\
            filter(RTKMission.revision_id ==
                   self._revision.revision_id).first()
        self._phase = self.program_session.query(RTKMissionPhase).\
            filter(RTKMissionPhase.mission_id ==
                   self._mission.mission_id).first()
        self._environment = self.program_session.query(RTKEnvironment).\
            filter(RTKEnvironment.phase_id ==
                   self._phase.phase_id).first()

        Configuration.DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/RTK_debug.log')
        Configuration.USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                        '/tmp/RTK_user.log')

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

        _database = 'sqlite:////tmp/TestDB.rtk'
        _dao = DAO('')

        self.assertFalse(_dao.db_connect(_database))

    @attr(all=True, unit=True)
    def test02a_dao_db_create_common(self):
        """
        (TestDAO) db_create_common should return False on success.
        """

        Configuration.RTK_COM_INFO = {'host' : 'localhost',
                                      'socket' : 3306,
                                      'database' : '/tmp/_rtk_common_db.rtk',
                                      'type' : 'sqlite',
                                      'user' : '',
                                      'password' : ''}
        self.assertFalse(self.DUT.db_create_common(self.program_session))

        os.remove('/tmp/_rtk_common_db.rtk')

    @attr(all=True, unit=True)
    def test02b_dao_db_create_common_bad_db_name(self):
        """
        (TestDAO) db_create_common should return True on failure.
        """

        Configuration.RTK_COM_INFO = {'host' : 'localhost',
                                      'socket' : 3306,
                                      'database' : 'tmp/_rtk_common_db.rtk',
                                      'type' : 'sqlite',
                                      'user' : '',
                                      'password' : ''}
        self.assertTrue(self.DUT.db_create_common(self.program_session))

    @attr(all=True, unit=True)
    def test02c_dao_db_create_program(self):
        """
        (TestDAO) db_create_program should return False on success.
        """

        Configuration.RTK_PROG_INFO = {'host' : 'localhost',
                                       'socket' : 3306,
                                       'database' : '/tmp/_rtk_program_db.rtk',
                                       'type' : 'sqlite',
                                       'user' : '',
                                       'password' : ''}
        self.assertFalse(self.DUT.db_create_program(self.program_session))

        os.remove('/tmp/_rtk_program_db.rtk')

    @attr(all=True, unit=True)
    def test02d_dao_db_create_program_bad_db_name(self):
        """
        (TestDAO) db_create_program should return True on failure.
        """

        Configuration.RTK_PROG_INFO = {'host' : 'localhost',
                                       'socket' : 3306,
                                       'database' : 'tmp/_rtk_program_db.rtk',
                                       'type' : 'sqlite',
                                       'user' : '',
                                       'password' : ''}
        self.assertTrue(self.DUT.db_create_program(self.program_session))

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

    @attr(all=True, unit=True)
    def test04_dao_db_add_many(self):
        """
        (TestDAO) db_add should return a zero error code on success when adding multiple records to the database.
        """

        _mission = RTKMission()
        _mission.revision_id = self._revision.revision_id
        _phase = RTKMissionPhase()
        _phase.mission_id = self._mission.mission_id
        _environment = RTKEnvironment()
        _environment.phase_id = self._phase.phase_id

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

    @attr(all=True, unit=True)
    def test07a_dao_db_load_globals(self):
        """
        (TestDAO) db_load_globals returns False on success
        """

        self.assertFalse(self.DUT.db_load_globals(self.site_session))

        self.assertTrue(isinstance(self.DUT.tree, Tree))

        self.assertEqual(Configuration.RTK_ACTION_CATEGORY, {})
        self.assertEqual(Configuration.RTK_INCIDENT_CATEGORY,
                         {34: (u'HW', u'Hardware', u'incident', 1),
                          35: (u'SW', u'Software', u'incident', 1),
                          36: (u'PROC', u'Process', u'incident', 1)})
        self.assertEqual(Configuration.RTK_SEVERITY,
                         {10: (u'INS', u'Insignificant', u'risk', 1),
                          11: (u'SLT', u'Slight', u'risk', 2),
                          12: (u'LOW', u'Low', u'risk', 3),
                          13: (u'MED', u'Medium', u'risk', 4),
                          14: (u'HI', u'High', u'risk', 5),
                          15: (u'MAJ', u'Major', u'risk', 6)})

        self.assertEqual(Configuration.RTK_ACTIVE_ENVIRONMENTS, {})
        self.assertEqual(Configuration.RTK_DORMANT_ENVIRONMENTS, {})
        self.assertEqual(Configuration.RTK_SW_DEV_ENVIRONMENTS, {})

        self.assertEqual(Configuration.RTK_AFFINITY_GROUPS, {})
        self.assertEqual(Configuration.RTK_WORKGROUPS[1],
                         (u'Engineering, Systems', u'workgroup'))

        self.assertEqual(Configuration.RTK_FAILURE_PROBABILITY, {})
        self.assertEqual(Configuration.RTK_SW_LEVELS, {})

        self.assertEqual(Configuration.RTK_DETECTION_METHODS, {})
        self.assertEqual(Configuration.RTK_SW_TEST_METHODS, {})

        self.assertEqual(Configuration.RTK_ALLOCATION_MODELS, {})
        self.assertEqual(Configuration.RTK_DAMAGE_MODELS, {})
        self.assertEqual(Configuration.RTK_HR_MODEL, {})

        self.assertEqual(Configuration.RTK_LIFECYCLE, {})
        self.assertEqual(Configuration.RTK_SW_DEV_PHASES, {})

        self.assertEqual(Configuration.RTK_RPN_DETECTION, {})
        self.assertEqual(Configuration.RTK_RPN_SEVERITY, {})
        self.assertEqual(Configuration.RTK_RPN_OCCURRENCE, {})

        self.assertEqual(Configuration.RTK_ACTION_STATUS, {})
        self.assertEqual(Configuration.RTK_INCIDENT_STATUS, {})

        self.assertEqual(Configuration.RTK_CONTROL_TYPES,
                         [u'Prevention', u'Detection'])
        self.assertEqual(Configuration.RTK_COST_TYPE, {})
        self.assertEqual(Configuration.RTK_HR_TYPE, {})
        self.assertEqual(Configuration.RTK_INCIDENT_TYPE, {})
        self.assertEqual(Configuration.RTK_MTTR_TYPE, {})
        self.assertEqual(Configuration.RTK_REQUIREMENT_TYPE,
                         {1: (u'Type Code', u'Test Type of Requirement',
                              u'requirement')})
        self.assertEqual(Configuration.RTK_VALIDATION_TYPE, {})

        self.assertEqual(Configuration.RTK_SW_APPLICATION,
                         {1: (u'Application Description', 1.0, 1.0)})
        self.assertEqual(Configuration.RTK_CATEGORIES, {})
        self.assertEqual(Configuration.RTK_CRITICALITY,
                         {1: (u'Criticality Name', u'Criticality Description',
                              u'', 0)})
        self.assertEqual(Configuration.RTK_FAILURE_MODES, {})
        self.assertEqual(Configuration.RTK_HAZARDS,
                         {1: (u'Hazard Category', u'Hazard Subcategory')})
        self.assertEqual(Configuration.RTK_MANUFACTURERS,
                         {1: (u'Distribution Description', u'unknown',
                              u'CAGE Code')})
        self.assertEqual(Configuration.RTK_MEASUREMENT_UNITS, {})
        self.assertEqual(Configuration.RTK_OPERATING_PARAMETERS, {})
        self.assertEqual(Configuration.RTK_S_DIST,
                         {1: (u'Distribution Description', u'unknown')})
        self.assertEqual(Configuration.RTK_STAKEHOLDERS,
                         {1: (u'Stakeholder',)})
        self.assertEqual(Configuration.RTK_SUBCATEGORIES, {})
        self.assertEqual(Configuration.RTK_USERS[1],
                         (u'Last Name', u'First Name', u'EMail', u'867.5309',
                          u'0'))