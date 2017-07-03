#!/usr/bin/env python -O
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
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

from datetime import date, timedelta

import unittest
from nose.plugins.attrib import attr

import Configuration as Configuration
import Utilities as Utilities
from dao.DAO import *

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class Test00DAO(unittest.TestCase):
    """
    Class for testing the DAO class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the DAO class.
        """

        self.DUT = DAO('')

        self._revision = RTKRevision()
        self._mission = RTKMission()
        self._mission.revision_id = 1
        self._phase = RTKMissionPhase()
        self._phase.mission_id = 1
        self._environment = RTKEnvironment()
        self._environment.phase_id = 1

        Configuration.DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/rtk_debug.log')
        Configuration.USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                        '/tmp/rtk_user.log')

    @attr(all=True, unit=True)
    def test00_dao_create(self):
        """
        (TestDAO) __init__ should create a DAO class instance.
        """

        self.assertTrue(isinstance(self.DUT, DAO))
        self.assertEqual(self.DUT.engine, None)
        self.assertEqual(self.DUT.metadata, None)

    @attr(all=True, unit=True)
    def test01_dao_db_connect(self):
        """
        (TestDAO) db_connect should return False on success connecting to an SQLite database.
        """

        _database = 'sqlite:////tmp/TestDB.rtk'

        self.assertFalse(self.DUT.db_connect(_database))

    @attr(all=True, unit=True)
    def test02a_dao_db_create_common(self):
        """
        (TestDAO) db_create_common should return False on success.
        """

        _database = 'sqlite:////tmp/_rtk_common_db.rtk'
        self.DUT.db_connect(_database)

        self.assertFalse(self.DUT.db_create_common(_database))

    @attr(all=True, unit=False)
    def test02b_dao_db_create(self):
        """
        (TestDAO) db_create should return False on success.
        """

        self.assertFalse(self.DUT.db_create())

    @attr(all=True, unit=True)
    def test03a_dao_db_add(self):
        """
        (TestDAO) db_add should return a zero error code on success when adding a single record to the database.
        """

        (_error_code, _msg) = self.DUT.db_add(self._revision)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "SUCCESS: Adding an item to the RTK Program database.")

    @attr(all=True, unit=True)
    def test03b_dao_db_add_no_item(self):
        """
        (TestDAO) db_add should return a 1003 error code on failure.
        """

        (_error_code, _msg) = self.DUT.db_add(None)

        self.assertEqual(_error_code, 1003)
        self.assertEqual(_msg,
                         "ERROR: Adding an item to the RTK Program database.")

    @attr(all=True, unit=True)
    def test04_dao_db_add_many(self):
        """
        (TestDAO) db_add should return a zero error code on success when adding multiple records to the database.
        """

        (_error_code, _msg) = self.DUT.db_add([self._mission, self._phase,
                                               self._environment])

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "SUCCESS: Adding an item to the RTK Program database.")

    @attr(all=True, unit=True)
    def test05_dao_db_update(self):
        """
        (TestDAO) db_update should return a zero error code on success.
        """

        self._revision.availability_logistics = 0.9959
        self._revision.availability_mission = 0.9999
        self._mission.description = 'Big mission'

        (_error_code, _msg) = self.DUT.db_update()

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "SUCCESS: Updating the RTK Program database.")

    @attr(all=True, unit=True)
    def test06a_dao_db_delete(self):
        """
        (TestDAO) db_delete should return a zero error code on success.
        """

        _phase = RTKMissionPhase()
        _phase.mission_id = 1

        self.DUT.db_add(_phase)

        (_error_code, _msg) = self.DUT.db_delete(_phase)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg,
                         "SUCCESS: Deleting an item from the RTK Program database.")

    @attr(all=True, unit=True)
    def test06b_dao_db_delete_no_item(self):
        """
        (TestDAO) db_delete should return a 1005 error code on failure.
        """

        (_error_code, _msg) = self.DUT.db_delete(None)

        self.assertEqual(_error_code, 1005)
        self.assertEqual(_msg,
                         "ERROR: Deleting an item from the RTK Program database.")


class Test01RTKRevision(unittest.TestCase):
    """
    Class for testing the RTKRevision class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKRevision class.
        """

        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestDB.rtk')

        self.DUT = RTKRevision()

        self.dao.db_add(self.DUT)

    @attr(all=True, unit=True)
    def test00_rtkrevision_create(self):
        """
        (TestRTKRevision) DUT should be an RTKRevision model
        """

        self.assertTrue(isinstance(self.DUT, RTKRevision))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_revision')
        self.assertEqual(self.DUT.revision_id, 2)
        self.assertEqual(self.DUT.availability_logistics, 1.0)
        self.assertEqual(self.DUT.availability_mission, 1.0)
        self.assertEqual(self.DUT.cost, 0.0)
        self.assertEqual(self.DUT.cost_failure, 0.0)
        self.assertEqual(self.DUT.cost_hour, 0.0)
        self.assertEqual(self.DUT.hazard_rate_active, 0.0)
        self.assertEqual(self.DUT.hazard_rate_dormant, 0.0)
        self.assertEqual(self.DUT.hazard_rate_logistics, 0.0)
        self.assertEqual(self.DUT.hazard_rate_mission, 0.0)
        self.assertEqual(self.DUT.hazard_rate_software, 0.0)
        self.assertEqual(self.DUT.mmt, 0.0)
        self.assertEqual(self.DUT.mcmt, 0.0)
        self.assertEqual(self.DUT.mpmt, 0.0)
        self.assertEqual(self.DUT.mtbf_logistics, 0.0)
        self.assertEqual(self.DUT.mtbf_mission, 0.0)
        self.assertEqual(self.DUT.mttr, 0.0)
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.reliability_logistics, 1.0)
        self.assertEqual(self.DUT.reliability_mission, 1.0)
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.total_part_count, 1)
        self.assertEqual(self.DUT.revision_code, '')
        self.assertEqual(self.DUT.program_time, 0.0)
        self.assertEqual(self.DUT.program_time_sd, 0.0)
        self.assertEqual(self.DUT.program_cost, 0.0)
        self.assertEqual(self.DUT.program_cost_sd, 0.0)

    @attr(all=True, unit=True)
    def test01a_calculate_reliability(self):
        """
        (TestRTKRevision) calculate_reliability should return False on success.
        """

        self.DUT.hazard_rate_active = 0.00000151
        self.DUT.hazard_rate_dormant = 0.0000000152
        self.DUT.hazard_rate_software = 0.0000003
        self.DUT.hazard_rate_mission = 0.000002

        self.assertFalse(self.DUT.calculate_reliability(100.0))
        self.assertAlmostEqual(self.DUT.hazard_rate_logistics, 1.8252e-06)
        self.assertAlmostEqual(self.DUT.mtbf_logistics, 547885.1632698)
        self.assertAlmostEqual(self.DUT.mtbf_mission, 500000.0)
        self.assertAlmostEqual(self.DUT.reliability_logistics, 0.9998175)
        self.assertAlmostEqual(self.DUT.reliability_mission, 0.9998000)

    @attr(all=True, unit=True)
    def test01b_calculate_reliability_divide_by_zero(self):
        """
        (TestRTKRevision) calculate_reliability should return True when attempting to divide by zero.
        """

        self.DUT.hazard_rate_mission = 0.0

        self.assertTrue(self.DUT.calculate_reliability(100.0))

    @attr(all=True, unit=True)
    def test02a_calculate_availability(self):
        """
        (TestRTKRevision) calculate_availability should return False on success.
        """

        self.DUT.mpmt = 0.5
        self.DUT.mcmt = 1.2
        self.DUT.mttr = 5.8
        self.DUT.mmt = 0.85
        self.DUT.mtbf_logistics = 547885.1632698
        self.DUT.mtbf_mission = 500000.0

        self.assertFalse(self.DUT.calculate_availability())
        self.assertAlmostEqual(self.DUT.availability_logistics, 0.9999894)
        self.assertAlmostEqual(self.DUT.availability_mission, 0.9999884)

    @attr(all=True, unit=True)
    def test02b_calculate_availability_divide_by_zero(self):
        """
        (TestRTKRevision) calculate_availability should return True when attempting to divide by zero.
        """

        self.DUT.mttr = 0.0
        self.DUT.mtbf_logistics = 547885.1632698
        self.DUT.mtbf_mission = 0.0

        self.assertTrue(self.DUT.calculate_availability())

    @attr(all=True, unit=True)
    def test03a_calculate_costs(self):
        """
        (TestRTKRevision) calculate_costs should return False on success.
        """

        self.DUT.cost = 1252.78
        self.DUT.hazard_rate_logistics = 1.0 / 547885.1632698

        self.assertFalse(self.DUT.calculate_costs(100.0))
        self.assertAlmostEqual(self.DUT.cost_per_failure, 0.002286574)
        self.assertAlmostEqual(self.DUT.cost_per_hour, 12.5278)

    @attr(all=True, unit=True)
    def test03b_calculate_costs_divide_by_zero(self):
        """
        (TestRTKRevision) calculate_costs should return True when attempting to divide by zero.
        """

        self.DUT.cost = 1252.78
        self.DUT.hazard_rate_logistics = 1.0 / 547885.1632698

        self.assertTrue(self.DUT.calculate_costs(0.0))

    @attr(all=True, unit=True)
    def test04_get_attributes(self):
        """
        (TestRTKRevision) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (9, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, '', 1.0, 1.0, '', 1,
                          '', 0.0, 0.0, 0.0, 0.0))

    @attr(all=True, unit=True)
    def test05a_set_attributes(self):
        """
        (TestRTKRevision) set_attributes should return a zero error code on success
        """

        _attributes = (0.986, 0.999, 113.25, 1.38, 0.15, 0.000001523,
                       0.0000001523, 0.0000016753, 0.000001018, 0.00000852,
                       32.8, 2.3, 1.8, 59690.8, 982318.3, 12.6,
                       'Revision Name', 0.988, 0.9999, 'Remarks', 12, '-',
                       5688.6, 26812.0, 186238, 255487369.5)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKRevision {0:d} " \
                               "attributes.".format(    self.DUT.revision_id))

    @attr(all=True, unit=True)
    def test05b_set_attributes_wrong_type(self):
        """
        (TestRTKRevision) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = (0.986, 0.999, 113.25, None, 0.15, 0.000001523,
                       0.0000001523, None, 0.000001018, 0.00000852,
                       32.8, 2.3, 1.8, 59690.8, 982318.3, 12.6,
                       'Revision Name', 0.988, 0.9999, 'Remarks', 12, '-',
                       5688.6, 26812.0, 186238, 255487369.5)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKRevision " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test05c_set_attributes_too_few_passed(self):
        """
        (TestRTKRevision) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = (0.986, 0.999, 113.25, 1.38, 0.15, 0.000001523,
                       0.0000001523, 0.0000016753, 0.000001018, 0.00000852,
                       32.8, 2.3, 1.8, 59690.8, 982318.3, 12.6,
                       'Revision Name', 0.988, 0.9999, 'Remarks', 12, '-',
                       5688.6, 26812.0, 186238)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to RTKRevision.set_attributes().")


class Test02RTKMission(unittest.TestCase):
    """
    Class for testing the RTKMission class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKMission class.
        """

        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestDB.rtk')

        self.DUT = RTKMission()
        self.DUT.revision_id = 1

        self.dao.db_add(self.DUT)

    @attr(all=True, unit=True)
    def test00_rtkmission_create(self):
        """
        (TestMission) DUT should create an RTKMission model
        """

        self.assertTrue(isinstance(self.DUT, RTKMission))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_mission')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.mission_id, 2)
        self.assertEqual(self.DUT.description, 'Description')
        self.assertEqual(self.DUT.mission_time, 0.0)
        self.assertEqual(self.DUT.time_units, 'hours')

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKMission) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (1, 3, 'Description', 0.0, 'hours'))

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKMission) set_attributes should return a zero error code on success
        """

        _attributes = ('Mission Description', 216.0, 'hours')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKMission {0:d} " \
                               "attributes.".format(self.DUT.mission_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKMission) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('Mission Description', None, 'hours')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKMission " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKMission) set_attributes should return a zero error code when passed too few attributes
        """

        _attributes = ('Mission Description', 216.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to " \
                               "RTKMission.set_attributes().")


class Test03RTKMissionPhase(unittest.TestCase):
    """
    Class for testing the RTKMissionPhase class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKMissionPhase class.
        """

        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestDB.rtk')

        self.DUT = RTKMissionPhase()
        self.DUT.mission_id = 1

        self.dao.db_add(self.DUT)

    @attr(all=True, unit=True)
    def test00_rtkmissionphase_create(self):
        """
        (TestRTKMissionPhase) DUT should create an RTKMissionPhase model.
        """

        self.assertTrue(isinstance(self.DUT, RTKMissionPhase))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_mission_phase')
        self.assertEqual(self.DUT.mission_id, 1)
        self.assertEqual(self.DUT.phase_id, 2)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.phase_start, 0.0)
        self.assertEqual(self.DUT.phase_end, 0.0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKMissionPhase) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (1, 3, '', '', 0.0, 0.0))

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKMissionPhase) set_attributes should return a zero error code on success
        """

        _attributes = ('Mission Phase', 'Name', 0.0, 216.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKMissionPhase {0:d} " \
                               "attributes.".format(self.DUT.phase_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKEnvironment) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('Mission Phase', 'Name', None, 216.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKMissionPhase " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKMissionPhase) set_attributes should return a zero error code when passed too few attributes
        """

        _attributes = ('Mission Phase', 'Name', 85.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to " \
                               "RTKMissionPhase.set_attributes().")


class Test04RTKEnvironment(unittest.TestCase):
    """
    Class for testing the RTKEnvironment class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKEnvironment class.
        """

        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestDB.rtk')

        self.DUT = RTKEnvironment()
        self.DUT.phase_id = 1

        self.dao.db_add(self.DUT)

    @attr(all=True, unit=True)
    def test00_rtkenvironment_create(self):
        """
        (TestRTKEnvironment) DUT should create an RTKEnvironment model.
        """

        self.assertTrue(isinstance(self.DUT, RTKEnvironment))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_environment')
        self.assertEqual(self.DUT.phase_id, 1)
        self.assertEqual(self.DUT.environment_id, 2)
        self.assertEqual(self.DUT.name, 'Condition Name')
        self.assertEqual(self.DUT.units, 'Units')
        self.assertEqual(self.DUT.minimum, 0.0)
        self.assertEqual(self.DUT.maximum, 0.0)
        self.assertEqual(self.DUT.mean, 0.0)
        self.assertEqual(self.DUT.variance, 0.0)
        self.assertEqual(self.DUT.ramp_rate, 0.0)
        self.assertEqual(self.DUT.low_dwell_time, 0.0)
        self.assertEqual(self.DUT.high_dwell_time, 0.0)

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKEnvironment) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (1, 3, 'Condition Name', 'Units', 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0))

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKEnvironment) set_attributes should return a zero error code on success
        """

        _attributes = ('Failure Def.', 'hours', 4.5, 58.6, 31.4, 544.0, 15.3,
                       25.0, 85.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKEnvironment {0:d} " \
                               "attributes.".format(self.DUT.environment_id))

    @attr(all=True, unit=True)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKEnvironment) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = ('Condition Name', 'hours', 4.5, None, 31.4, 544.0, 15.3,
                       25.0, 85.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKEnvironment " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKEnvironment) set_attributes should return a zero error code when passed too few attributes
        """

        _attributes = ('Condition Name', 'hours', 4.5, 31.4, 544.0, 15.3, 25.0,
                       85.0)

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to " \
                               "RTKEnvironment.set_attributes().")


class Test05RTKFailureDefinition(unittest.TestCase):
    """
    Class for testing the RTKFailureDefinition class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKFailureDefinition class.
        """

        self.dao = DAO('')
        self.dao.db_connect('sqlite:////tmp/TestDB.rtk')

        self.DUT = RTKFailureDefinition()
        self.DUT.revision_id = 1

        self.dao.db_add(self.DUT)

    @attr(all=True, unit=True)
    def test00_rtkfailuredefinition_create(self):
        """
        (TestRTKFailureDefinition) DUT should create an RTKFailureDefinition model.
        """

        self.assertTrue(isinstance(self.DUT, RTKFailureDefinition))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_failure_definition')
        self.assertEqual(self.DUT.revision_id, 1)
        self.assertEqual(self.DUT.definition_id, 1)
        self.assertEqual(self.DUT.definition, 'Failure Definition')

    @attr(all=True, unit=True)
    def test01_get_attributes(self):
        """
        (TestRTKFailureDefinition) get_attributes should return a tuple of attribute values.
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (1, 2, 'Failure Definition'))

    @attr(all=True, unit=True)
    def test02a_set_attributes(self):
        """
        (TestRTKFailureDefinition) set_attributes should return a zero error code on success
        """

        _attributes = ('Failure Def.')

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, "RTK SUCCESS: Updating RTKFailureDefinition " \
                               "{0:d} attributes.".\
                               format(self.DUT.definition_id))

    @attr(all=True, unit=False)
    def test02b_set_attributes_wrong_type(self):
        """
        (TestRTKFailureDefinition) set_attributes should return a 10 error code when passed the wrong type
        """

        _attributes = [None]

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 10)
        self.assertEqual(_msg, "RTK ERROR: Incorrect data type when " \
                               "converting one or more RTKEFailureDefinition " \
                               "attributes.")

    @attr(all=True, unit=True)
    def test02c_set_attributes_too_few_passed(self):
        """
        (TestRTKFailureDefinition) set_attributes should return a 40 error code when passed too few attributes
        """

        _attributes = ()

        _error_code, _msg = self.DUT.set_attributes(_attributes)

        self.assertEqual(_error_code, 40)
        self.assertEqual(_msg, "RTK ERROR: Insufficient number of input " \
                               "values to " \
                               "RTKFailureDefinition.set_attributes().")


class Test055RTKFunction(unittest.TestCase):
    """
    Class for testing the RTKFunction class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKFunction class.
        """

        self.DUT = RTKFunction()
        self.DUT.revision_id = 0

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkfunction_create(self):
        """
        (TestDAO) DUT should create an RTKFunction model.
        """

        self.assertTrue(isinstance(self.DUT, RTKFunction))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_function')
        self.assertEqual(self.DUT.function_id, 1)

        self.assertEqual(self.DUT.availability_logistics, 0.0)
        self.assertEqual(self.DUT.availability_mission, 0.0)
        self.assertEqual(self.DUT.cost, 0.0)
        self.assertEqual(self.DUT.function_code, 'Function Code')
        self.assertEqual(self.DUT.hazard_rate_logistics, 0.0)
        self.assertEqual(self.DUT.hazard_rate_mission, 0.0)
        self.assertEqual(self.DUT.level, 0)
        self.assertEqual(self.DUT.mmt, 0.0)
        self.assertEqual(self.DUT.mcmt, 0.0)
        self.assertEqual(self.DUT.mpmt, 0.0)
        self.assertEqual(self.DUT.mtbf_logistics, 0.0)
        self.assertEqual(self.DUT.mtbf_mission, 0.0)
        self.assertEqual(self.DUT.mttr, 0.0)
        self.assertEqual(self.DUT.name, 'Name')
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.safety_critical, 0)
        self.assertEqual(self.DUT.total_mode_count, 0)
        self.assertEqual(self.DUT.total_part_count, 0)
        self.assertEqual(self.DUT.type_id, 0)


class Test06RTKRequirement(unittest.TestCase):
    """
    Class for testing the RTKRequirement class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKRequirement class.
        """

        self.DUT = RTKRequirement()
        self.DUT.revision_id = 0

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkrequirement_create(self):
        """
        (TestDAO) DUT should create an RTKRequirement model.
        """

        self.assertTrue(isinstance(self.DUT, RTKRequirement))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_requirement')
        self.assertEqual(self.DUT.revision_id, 0)
        self.assertEqual(self.DUT.requirement_id, 1)
        self.assertEqual(self.DUT.requirement_code, '')
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.type_id, 0)
        self.assertEqual(self.DUT.priority, 0)
        self.assertEqual(self.DUT.specification, '')
        self.assertEqual(self.DUT.page_number, '')
        self.assertEqual(self.DUT.figure_number, '')
        self.assertEqual(self.DUT.derived, 0)
        self.assertEqual(self.DUT.owner_id, 0)
        self.assertEqual(self.DUT.validated, 0)
        self.assertEqual(self.DUT.validated_date, date.today())


class Test07RTKStakeholderInput(unittest.TestCase):
    """
    Class for testing the RTKStakeholderInput class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKStakeholderInput class.
        """

        self.DUT = RTKStakeholderInput()
        self.DUT.revision_id = 0

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkstakeholder_create(self):
        """
        (TestDAO) DUT should create an RTKStakeholderInput model.
        """

        self.assertTrue(isinstance(self.DUT, RTKStakeholderInput))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_stakeholder_input')
        self.assertEqual(self.DUT.revision_id, 0)
        self.assertEqual(self.DUT.input_id, 1)
        self.assertEqual(self.DUT.customer_rank, 1)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.group, '')
        self.assertEqual(self.DUT.improvement, 0.0)
        self.assertEqual(self.DUT.overall_weight, 0.0)
        self.assertEqual(self.DUT.planned_rank, 1)
        self.assertEqual(self.DUT.priority, 1)
        self.assertEqual(self.DUT.requirement_id, 0)
        self.assertEqual(self.DUT.stakeholder, '')
        self.assertEqual(self.DUT.user_Float_1, 0.0)
        self.assertEqual(self.DUT.user_Float_2, 0.0)
        self.assertEqual(self.DUT.user_Float_3, 0.0)
        self.assertEqual(self.DUT.user_Float_4, 0.0)
        self.assertEqual(self.DUT.user_Float_5, 0.0)


class Test08RTKMatrix(unittest.TestCase):
    """
    Class for testing the RTKMatrix class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKMatrix class.
        """

        self.DUT = RTKMatrix()
        self.DUT.revision_id = 0

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkmatrix_create(self):
        """
        (TestDAO) DUT should create an RTKMatrix model.
        """

        self.assertTrue(isinstance(self.DUT, RTKMatrix))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_matrix')
        self.assertEqual(self.DUT.revision_id, 0)
        self.assertEqual(self.DUT.matrix_id, 1)
        self.assertEqual(self.DUT.column_id, 0)
        self.assertEqual(self.DUT.column_item_id, 0)
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.row_id, 0)
        self.assertEqual(self.DUT.row_item_id, 0)
        self.assertEqual(self.DUT.type_id, 0)
        self.assertEqual(self.DUT.value, 0.0)


class Test09RTKHardware(unittest.TestCase):
    """
    Class for testing the RTKHardware class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKHardware class.
        """

        self.DUT = RTKHardware()
        self.DUT.revision_id = 0

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkhardware_create(self):
        """
        (TestDAO) DUT should create an RTKHardware model.
        """

        self.assertTrue(isinstance(self.DUT, RTKHardware))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_hardware')
        self.assertEqual(self.DUT.revision_id, 0)
        self.assertEqual(self.DUT.hardware_id, 1)
        self.assertEqual(self.DUT.alt_part_number, '')
        self.assertEqual(self.DUT.attachments, '')
        self.assertEqual(self.DUT.cage_code, '')
        self.assertEqual(self.DUT.comp_ref_des, '')
        self.assertEqual(self.DUT.category_id, 0)
        self.assertEqual(self.DUT.cost, 0.0)
        self.assertEqual(self.DUT.cost_failure, 0.0)
        self.assertEqual(self.DUT.cost_hour, 0.0)
        self.assertEqual(self.DUT.cost_type_id, 0)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.duty_cycle, 100.0)
        self.assertEqual(self.DUT.figure_number, '')
        self.assertEqual(self.DUT.lcn, '')
        self.assertEqual(self.DUT.level, 0)
        self.assertEqual(self.DUT.manufacturer_id, 0)
        self.assertEqual(self.DUT.mission_time, 100.0)
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.nsn, '')
        self.assertEqual(self.DUT.page_number, '')
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.part, 0)
        self.assertEqual(self.DUT.part_number, '')
        self.assertEqual(self.DUT.quantity, 1)
        self.assertEqual(self.DUT.ref_des, '')
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.repairable, 0)
        self.assertEqual(self.DUT.specification_number, '')
        self.assertEqual(self.DUT.subcategory_id, 0)
        self.assertEqual(self.DUT.tagged_part, 0)
        self.assertEqual(self.DUT.total_part_count, 0)
        self.assertEqual(self.DUT.total_power_dissipation, 0.0)
        self.assertEqual(self.DUT.year_of_manufacture, date.today().year)


class Test10RTKAllocation(unittest.TestCase):
    """
    Class for testing the RTKAllocation class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKAllocation class.
        """

        self.DUT = RTKAllocation()
        self.DUT.hardware_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkallocation_create(self):
        """
        (TestDAO) DUT should create an RTKAllocation model.
        """

        self.assertTrue(isinstance(self.DUT, RTKAllocation))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_allocation')

        self.assertEqual(self.DUT.availability_alloc, 0.0)
        self.assertEqual(self.DUT.env_factor, 1)
        self.assertEqual(self.DUT.goal_measure_id, 1)
        self.assertEqual(self.DUT.hazard_rate_alloc, 0.0)
        self.assertEqual(self.DUT.hazard_rate_goal, 0.0)
        self.assertEqual(self.DUT.included, 1)
        self.assertEqual(self.DUT.int_factor, 1)
        self.assertEqual(self.DUT.method_id, 1)
        self.assertEqual(self.DUT.mtbf_alloc, 0.0)
        self.assertEqual(self.DUT.mtbf_goal, 0.0)
        self.assertEqual(self.DUT.n_sub_systems, 1)
        self.assertEqual(self.DUT.n_sub_elements, 1)
        self.assertEqual(self.DUT.parent_id, 1)
        self.assertEqual(self.DUT.percent_weight_factor, 0.0)
        self.assertEqual(self.DUT.reliability_alloc, 0.0)
        self.assertEqual(self.DUT.reliability_goal, 1.0)
        self.assertEqual(self.DUT.op_time_factor, 1)
        self.assertEqual(self.DUT.soa_factor, 1)
        self.assertEqual(self.DUT.weight_factor, 1)


class Test11RTKHazard(unittest.TestCase):
    """
    Class for testing the RTKHazard class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKHazard class.
        """

        self.DUT = RTKHazard()
        self.DUT.hardware_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkhazard_create(self):
        """
        (TestDAO) DUT should create an RTKHazard model.
        """

        self.assertTrue(isinstance(self.DUT, RTKHazard))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_hazard')
        self.assertEqual(self.DUT.hazard_id, 1)
        self.assertEqual(self.DUT.potential_hazard, '')
        self.assertEqual(self.DUT.potential_cause, '')
        self.assertEqual(self.DUT.assembly_effect, '')
        self.assertEqual(self.DUT.assembly_severity_id, 4)
        self.assertEqual(self.DUT.assembly_probability_id, 5)
        self.assertEqual(self.DUT.assembly_hri, 20)
        self.assertEqual(self.DUT.assembly_mitigation, '')
        self.assertEqual(self.DUT.assembly_severity_id_f, 4)
        self.assertEqual(self.DUT.assembly_probability_id_f, 5)
        self.assertEqual(self.DUT.assembly_hri_id_f, 4)
        self.assertEqual(self.DUT.system_effect, '')
        self.assertEqual(self.DUT.system_severity, 4)
        self.assertEqual(self.DUT.system_probability, 5)
        self.assertEqual(self.DUT.system_hri, 20)
        self.assertEqual(self.DUT.system_mitigation, '')
        self.assertEqual(self.DUT.system_severity_f, 4)
        self.assertEqual(self.DUT.system_probability_f, 5)
        self.assertEqual(self.DUT.system_hri_f, 20)
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.function_1, '')
        self.assertEqual(self.DUT.function_2, '')
        self.assertEqual(self.DUT.function_3, '')
        self.assertEqual(self.DUT.function_4, '')
        self.assertEqual(self.DUT.function_5, '')
        self.assertEqual(self.DUT.result_1, 0.0)
        self.assertEqual(self.DUT.result_2, 0.0)
        self.assertEqual(self.DUT.result_3, 0.0)
        self.assertEqual(self.DUT.result_4, 0.0)
        self.assertEqual(self.DUT.result_5, 0.0)
        self.assertEqual(self.DUT.user_blob_1, '')
        self.assertEqual(self.DUT.user_blob_2, '')
        self.assertEqual(self.DUT.user_blob_3, '')
        self.assertEqual(self.DUT.user_Float_1, 0.0)
        self.assertEqual(self.DUT.user_Float_2, 0.0)
        self.assertEqual(self.DUT.user_Float_3, 0.0)
        self.assertEqual(self.DUT.user_int_1, 0)
        self.assertEqual(self.DUT.user_int_2, 0)
        self.assertEqual(self.DUT.user_int_3, 0)


class Test12RTKSimilarItem(unittest.TestCase):
    """
    Class for testing the RTKSimilarItem class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKSimilarItem class.
        """

        self.DUT = RTKSimilarItem()
        self.DUT.hardware_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtksimilaritem_create(self):
        """
        (TestDAO) DUT should create an RTKSimilarItem model.
        """

        self.assertTrue(isinstance(self.DUT, RTKSimilarItem))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_similar_item')
        self.assertEqual(self.DUT.change_description_1, '')
        self.assertEqual(self.DUT.change_description_2, '')
        self.assertEqual(self.DUT.change_description_3, '')
        self.assertEqual(self.DUT.change_description_4, '')
        self.assertEqual(self.DUT.change_description_5, '')
        self.assertEqual(self.DUT.change_description_6, '')
        self.assertEqual(self.DUT.change_description_7, '')
        self.assertEqual(self.DUT.change_description_8, '')
        self.assertEqual(self.DUT.change_description_9, '')
        self.assertEqual(self.DUT.change_description_10, '')
        self.assertEqual(self.DUT.change_factor_1, 1.0)
        self.assertEqual(self.DUT.change_factor_2, 1.0)
        self.assertEqual(self.DUT.change_factor_3, 1.0)
        self.assertEqual(self.DUT.change_factor_4, 1.0)
        self.assertEqual(self.DUT.change_factor_5, 1.0)
        self.assertEqual(self.DUT.change_factor_6, 1.0)
        self.assertEqual(self.DUT.change_factor_7, 1.0)
        self.assertEqual(self.DUT.change_factor_8, 1.0)
        self.assertEqual(self.DUT.change_factor_9, 1.0)
        self.assertEqual(self.DUT.change_factor_10, 1.0)
        self.assertEqual(self.DUT.environment_from_id, 0)
        self.assertEqual(self.DUT.environment_to_id, 0)
        self.assertEqual(self.DUT.function_1, '')
        self.assertEqual(self.DUT.function_2, '')
        self.assertEqual(self.DUT.function_3, '')
        self.assertEqual(self.DUT.function_4, '')
        self.assertEqual(self.DUT.function_5, '')
        self.assertEqual(self.DUT.method_id, 0)
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.quality_from_id, 0)
        self.assertEqual(self.DUT.quality_to_id, 0)
        self.assertEqual(self.DUT.result_1, 0.0)
        self.assertEqual(self.DUT.result_2, 0.0)
        self.assertEqual(self.DUT.result_3, 0.0)
        self.assertEqual(self.DUT.result_4, 0.0)
        self.assertEqual(self.DUT.result_5, 0.0)
        self.assertEqual(self.DUT.temperature_from, 30.0)
        self.assertEqual(self.DUT.temperature_to, 30.0)
        self.assertEqual(self.DUT.user_blob_1, '')
        self.assertEqual(self.DUT.user_blob_2, '')
        self.assertEqual(self.DUT.user_blob_3, '')
        self.assertEqual(self.DUT.user_blob_4, '')
        self.assertEqual(self.DUT.user_blob_5, '')
        self.assertEqual(self.DUT.user_float_1, 0.0)
        self.assertEqual(self.DUT.user_float_2, 0.0)
        self.assertEqual(self.DUT.user_float_3, 0.0)
        self.assertEqual(self.DUT.user_float_4, 0.0)
        self.assertEqual(self.DUT.user_float_5, 0.0)
        self.assertEqual(self.DUT.user_int_1, 0)
        self.assertEqual(self.DUT.user_int_2, 0)
        self.assertEqual(self.DUT.user_int_3, 0)
        self.assertEqual(self.DUT.user_int_4, 0)
        self.assertEqual(self.DUT.user_int_5, 0)


class Test13RTKReliability(unittest.TestCase):
    """
    Class for testing the RTKReliability class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKReliability class.
        """

        self.DUT = RTKReliability()
        self.DUT.hardware_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkreliability_create(self):
        """
        (TestDAO) DUT should create an RTKReliability model.
        """

        self.assertTrue(isinstance(self.DUT, RTKReliability))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_reliability')
        self.assertEqual(self.DUT.add_adj_factor, 0.0)
        self.assertEqual(self.DUT.availability_logistics, 1.0)
        self.assertEqual(self.DUT.availability_mission, 1.0)
        self.assertEqual(self.DUT.avail_log_variance, 0.0)
        self.assertEqual(self.DUT.avail_mis_variance, 0.0)
        self.assertEqual(self.DUT.failure_distribution_id, 0)
        self.assertEqual(self.DUT.hazard_rate_active, 0.0)
        self.assertEqual(self.DUT.hazard_rate_dormant, 0.0)
        self.assertEqual(self.DUT.hazard_rate_logistics, 0.0)
        self.assertEqual(self.DUT.hazard_rate_method_id, 0)
        self.assertEqual(self.DUT.hazard_rate_mission, 0.0)
        self.assertEqual(self.DUT.hazard_rate_model, '')
        self.assertEqual(self.DUT.hazard_rate_percent, 0.0)
        self.assertEqual(self.DUT.hazard_rate_software, 0.0)
        self.assertEqual(self.DUT.hazard_rate_specified, 0.0)
        self.assertEqual(self.DUT.hazard_rate_type_id, 0)
        self.assertEqual(self.DUT.hr_active_variance, 0.0)
        self.assertEqual(self.DUT.hr_dormant_variance, 0.0)
        self.assertEqual(self.DUT.hr_logistics_variance, 0.0)
        self.assertEqual(self.DUT.hr_mission_variance, 0.0)
        self.assertEqual(self.DUT.hr_specified_variance, 0.0)
        self.assertEqual(self.DUT.lambda_b, 0.0)
        self.assertEqual(self.DUT.location_parameter, 0.0)
        self.assertEqual(self.DUT.mtbf_logistics, 0.0)
        self.assertEqual(self.DUT.mtbf_mission, 0.0)
        self.assertEqual(self.DUT.mtbf_specified, 0.0)
        self.assertEqual(self.DUT.mtbf_log_variance, 0.0)
        self.assertEqual(self.DUT.mtbf_mis_variance, 0.0)
        self.assertEqual(self.DUT.mtbf_spec_variance, 0.0)
        self.assertEqual(self.DUT.mult_adj_factor, 0.0)
        self.assertEqual(self.DUT.quality_id, 0)
        self.assertEqual(self.DUT.reliability_goal, 0.0)
        self.assertEqual(self.DUT.reliability_goal_meassure_id, 0)
        self.assertEqual(self.DUT.reliability_logistics, 0.0)
        self.assertEqual(self.DUT.reliability_mission, 0.0)
        self.assertEqual(self.DUT.reliability_log_variance, 0.0)
        self.assertEqual(self.DUT.reliability_mis_variance, 0.0)
        self.assertEqual(self.DUT.scale_parameter, 0.0)
        self.assertEqual(self.DUT.shape_parameter, 0.0)
        self.assertEqual(self.DUT.survival_analysis_id, 0)


class Test14RTKMilHdbkF(unittest.TestCase):
    """
    Class for testing the RTKMilHdbkF class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKMilHdbkF class.
        """

        self.DUT = RTKMilHdbkF()
        self.DUT.hardware_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkmilhdbkf_create(self):
        """
        (TestDAO) DUT should create an RTKMilHdbkF model.
        """

        self.assertTrue(isinstance(self.DUT, RTKMilHdbkF))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_mil_hdbk_f')
        self.assertEqual(self.DUT.A1, 0.0)
        self.assertEqual(self.DUT.A2, 0.0)
        self.assertEqual(self.DUT.B1, 0.0)
        self.assertEqual(self.DUT.B2, 0.0)
        self.assertEqual(self.DUT.C1, 0.0)
        self.assertEqual(self.DUT.C2, 0.0)
        self.assertEqual(self.DUT.lambdaDB, 0.0)
        self.assertEqual(self.DUT.lambdaBP, 0.0)
        self.assertEqual(self.DUT.lambdaCYC, 0.0)
        self.assertEqual(self.DUT.lambdaEOS, 0.0)
        self.assertEqual(self.DUT.piA, 0.0)
        self.assertEqual(self.DUT.piC, 0.0)
        self.assertEqual(self.DUT.piCD, 0.0)
        self.assertEqual(self.DUT.piCF, 0.0)
        self.assertEqual(self.DUT.piCR, 0.0)
        self.assertEqual(self.DUT.piCV, 0.0)
        self.assertEqual(self.DUT.piCYC, 0.0)
        self.assertEqual(self.DUT.piE, 0.0)
        self.assertEqual(self.DUT.piF, 0.0)
        self.assertEqual(self.DUT.piI, 0.0)
        self.assertEqual(self.DUT.piK, 0.0)
        self.assertEqual(self.DUT.piL, 0.0)
        self.assertEqual(self.DUT.piM, 0.0)
        self.assertEqual(self.DUT.piMFG, 0.0)
        self.assertEqual(self.DUT.piN, 0.0)
        self.assertEqual(self.DUT.piNR, 0.0)
        self.assertEqual(self.DUT.piP, 0.0)
        self.assertEqual(self.DUT.piPT, 0.0)
        self.assertEqual(self.DUT.piQ, 0.0)
        self.assertEqual(self.DUT.piR, 0.0)
        self.assertEqual(self.DUT.piS, 0.0)
        self.assertEqual(self.DUT.piT, 0.0)
        self.assertEqual(self.DUT.piTAPS, 0.0)
        self.assertEqual(self.DUT.pi_u, 0.0)
        self.assertEqual(self.DUT.pi_v, 0.0)


class Test15RTKNSWC(unittest.TestCase):
    """
    Class for testing the RTKNSWC class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKNSWC class.
        """

        self.DUT = RTKNSWC()
        self.DUT.hardware_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtknswc_create(self):
        """
        (TestDAO) DUT should create an RTKNSWC model.
        """

        self.assertTrue(isinstance(self.DUT, RTKNSWC))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_nswc')
        self.assertEqual(self.DUT.Cac, 0.0)
        self.assertEqual(self.DUT.Calt, 0.0)
        self.assertEqual(self.DUT.Cb, 0.0)
        self.assertEqual(self.DUT.Cbl, 0.0)
        self.assertEqual(self.DUT.Cbt, 0.0)
        self.assertEqual(self.DUT.Cbv, 0.0)
        self.assertEqual(self.DUT.Cc, 0.0)
        self.assertEqual(self.DUT.Ccf, 0.0)
        self.assertEqual(self.DUT.Ccp, 0.0)
        self.assertEqual(self.DUT.Ccs, 0.0)
        self.assertEqual(self.DUT.Ccv, 0.0)
        self.assertEqual(self.DUT.Ccw, 0.0)
        self.assertEqual(self.DUT.Cd, 0.0)
        self.assertEqual(self.DUT.Cdc, 0.0)
        self.assertEqual(self.DUT.Cdl, 0.0)
        self.assertEqual(self.DUT.Cdp, 0.0)
        self.assertEqual(self.DUT.Cds, 0.0)
        self.assertEqual(self.DUT.Cdt, 0.0)
        self.assertEqual(self.DUT.Cdw, 0.0)
        self.assertEqual(self.DUT.Cdy, 0.0)
        self.assertEqual(self.DUT.Ce, 0.0)
        self.assertEqual(self.DUT.Cf, 0.0)
        self.assertEqual(self.DUT.Cg, 0.0)
        self.assertEqual(self.DUT.Cga, 0.0)
        self.assertEqual(self.DUT.Cgl, 0.0)
        self.assertEqual(self.DUT.Cgp, 0.0)
        self.assertEqual(self.DUT.Cgs, 0.0)
        self.assertEqual(self.DUT.Cgt, 0.0)
        self.assertEqual(self.DUT.Cgv, 0.0)
        self.assertEqual(self.DUT.Ch, 0.0)
        self.assertEqual(self.DUT.Ci, 0.0)
        self.assertEqual(self.DUT.Ck, 0.0)
        self.assertEqual(self.DUT.Cl, 0.0)
        self.assertEqual(self.DUT.Clc, 0.0)
        self.assertEqual(self.DUT.Cm, 0.0)
        self.assertEqual(self.DUT.Cmu, 0.0)
        self.assertEqual(self.DUT.Cn, 0.0)
        self.assertEqual(self.DUT.Cnp, 0.0)
        self.assertEqual(self.DUT.Cnw, 0.0)
        self.assertEqual(self.DUT.Cp, 0.0)
        self.assertEqual(self.DUT.Cpd, 0.0)
        self.assertEqual(self.DUT.Cpf, 0.0)
        self.assertEqual(self.DUT.Cpv, 0.0)
        self.assertEqual(self.DUT.Cq, 0.0)
        self.assertEqual(self.DUT.Cr, 0.0)
        self.assertEqual(self.DUT.Crd, 0.0)
        self.assertEqual(self.DUT.Cs, 0.0)
        self.assertEqual(self.DUT.Csc, 0.0)
        self.assertEqual(self.DUT.Csf, 0.0)
        self.assertEqual(self.DUT.Cst, 0.0)
        self.assertEqual(self.DUT.Csv, 0.0)
        self.assertEqual(self.DUT.Csw, 0.0)
        self.assertEqual(self.DUT.Csz, 0.0)
        self.assertEqual(self.DUT.Ct, 0.0)
        self.assertEqual(self.DUT.Cv, 0.0)
        self.assertEqual(self.DUT.Cw, 0.0)
        self.assertEqual(self.DUT.Cy, 0.0)


class Test16RTKDesignElectric(unittest.TestCase):
    """
    Class for testing the RTKDesignElectric class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKDesignElectric class.
        """

        self.DUT = RTKDesignElectric()
        self.DUT.hardware_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkdesignelectric_create(self):
        """
        (TestDAO) DUT should create an RTKDesignElectric model.
        """

        self.assertTrue(isinstance(self.DUT, RTKDesignElectric))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_design_electric')
        self.assertEqual(self.DUT.application_id, 0)
        self.assertEqual(self.DUT.area, 0.0)
        self.assertEqual(self.DUT.capacitance, 0.0)
        self.assertEqual(self.DUT.configuration_id, 0)
        self.assertEqual(self.DUT.construction_id, 0)
        self.assertEqual(self.DUT.contact_form_id, 0)
        self.assertEqual(self.DUT.contact_gauge, 0)
        self.assertEqual(self.DUT.contact_rating_id, 0)
        self.assertEqual(self.DUT.current_operating, 0.0)
        self.assertEqual(self.DUT.current_rated, 0.0)
        self.assertEqual(self.DUT.current_ratio, 0.0)
        self.assertEqual(self.DUT.environment_active_id, 0)
        self.assertEqual(self.DUT.environment_dormant_id, 0)
        self.assertEqual(self.DUT.family_id, 0)
        self.assertEqual(self.DUT.feature_size, 0.0)
        self.assertEqual(self.DUT.frequency_operating, 0.0)
        self.assertEqual(self.DUT.insert_id, 0)
        self.assertEqual(self.DUT.insulation_id, 0)
        self.assertEqual(self.DUT.manufacturing_id, 0)
        self.assertEqual(self.DUT.matching_id, 0)
        self.assertEqual(self.DUT.n_active_pins, 0)
        self.assertEqual(self.DUT.n_circuit_planes, 1)
        self.assertEqual(self.DUT.n_cycles, 0)
        self.assertEqual(self.DUT.n_elements, 0)
        self.assertEqual(self.DUT.n_hand_soldered, 0)
        self.assertEqual(self.DUT.n_wave_soldered, 0)
        self.assertEqual(self.DUT.operating_life, 0.0)
        self.assertEqual(self.DUT.overstress, 0)
        self.assertEqual(self.DUT.package_id, 0)
        self.assertEqual(self.DUT.power_operating, 0.0)
        self.assertEqual(self.DUT.power_rated, 0.0)
        self.assertEqual(self.DUT.power_ratio, 0.0)
        self.assertEqual(self.DUT.reason, '')
        self.assertEqual(self.DUT.resistance, 0.0)
        self.assertEqual(self.DUT.specification_id, 0)
        self.assertEqual(self.DUT.technology_id, 0)
        self.assertEqual(self.DUT.temperature_case, 0.0)
        self.assertEqual(self.DUT.temperature_hot_spot, 0.0)
        self.assertEqual(self.DUT.temperature_junction, 0.0)
        self.assertEqual(self.DUT.temperature_rated_max, 0.0)
        self.assertEqual(self.DUT.temperature_rated_min, 0.0)
        self.assertEqual(self.DUT.temperature_rise, 0.0)
        self.assertEqual(self.DUT.theta_jc, 0.0)
        self.assertEqual(self.DUT.type_id, 0)
        self.assertEqual(self.DUT.voltage_ac_operating, 0.0)
        self.assertEqual(self.DUT.voltage_dc_operating, 0.0)
        self.assertEqual(self.DUT.voltage_esd, 0.0)
        self.assertEqual(self.DUT.voltage_rated, 0.0)
        self.assertEqual(self.DUT.voltage_ratio, 0.0)
        self.assertEqual(self.DUT.weight, 0.0)
        self.assertEqual(self.DUT.years_in_production, 1)


class Test17RTKDesignMechanic(unittest.TestCase):
    """
    Class for testing the RTKDesignMechanic class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKDesignMechanic class.
        """

        self.DUT = RTKDesignMechanic()
        self.DUT.hardware_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkdesignmechanic_create(self):
        """
        (TestDAO) DUT should create an RTKDesignMechanic model.
        """

        self.assertTrue(isinstance(self.DUT, RTKDesignMechanic))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_design_mechanic')
        self.assertEqual(self.DUT.altitude_operating, 0.0)
        self.assertEqual(self.DUT.application_id, 0)
        self.assertEqual(self.DUT.balance_id, 0)
        self.assertEqual(self.DUT.clearance, 0.0)
        self.assertEqual(self.DUT.casing_id, 0)
        self.assertEqual(self.DUT.contact_pressure, 0.0)
        self.assertEqual(self.DUT.deflection, 0.0)
        self.assertEqual(self.DUT.diameter_coil, 0.0)
        self.assertEqual(self.DUT.diameter_inner, 0.0)
        self.assertEqual(self.DUT.diameter_outer, 0.0)
        self.assertEqual(self.DUT.diameter_wire, 0.0)
        self.assertEqual(self.DUT.filter_size, 0.0)
        self.assertEqual(self.DUT.flow_design, 0.0)
        self.assertEqual(self.DUT.flow_operating, 0.0)
        self.assertEqual(self.DUT.frequency_operating, 0.0)
        self.assertEqual(self.DUT.friction, 0.0)
        self.assertEqual(self.DUT.impact_id, 0)
        self.assertEqual(self.DUT.leakage_allowable, 0.0)
        self.assertEqual(self.DUT.length, 0.0)
        self.assertEqual(self.DUT.length_compressed, 0.0)
        self.assertEqual(self.DUT.length_relaxed, 0.0)
        self.assertEqual(self.DUT.load_design, 0.0)
        self.assertEqual(self.DUT.load_id, 0)
        self.assertEqual(self.DUT.load_operating, 0.0)
        self.assertEqual(self.DUT.lubrication_id, 0)
        self.assertEqual(self.DUT.manufacturing_id, 0)
        self.assertEqual(self.DUT.material_id, 0)
        self.assertEqual(self.DUT.meyer_hardness, 0.0)
        self.assertEqual(self.DUT.misalignment_angle, 0.0)
        self.assertEqual(self.DUT.n_ten, 0)
        self.assertEqual(self.DUT.n_cycles, 0)
        self.assertEqual(self.DUT.n_elements, 0)
        self.assertEqual(self.DUT.offset, 0.0)
        self.assertEqual(self.DUT.particle_size, 0.0)
        self.assertEqual(self.DUT.pressure_contact, 0.0)
        self.assertEqual(self.DUT.pressure_delta, 0.0)
        self.assertEqual(self.DUT.pressure_downstream, 0.0)
        self.assertEqual(self.DUT.pressure_rated, 0.0)
        self.assertEqual(self.DUT.pressure_upstream, 0.0)
        self.assertEqual(self.DUT.rpm_design, 0.0)
        self.assertEqual(self.DUT.rpm_operating, 0.0)
        self.assertEqual(self.DUT.service_id, 0)
        self.assertEqual(self.DUT.spring_index, 0.0)
        self.assertEqual(self.DUT.surface_finish, 0.0)
        self.assertEqual(self.DUT.technology_id, 0)
        self.assertEqual(self.DUT.thickness, 0.0)
        self.assertEqual(self.DUT.torque_id, 0)
        self.assertEqual(self.DUT.type_id, 0)
        self.assertEqual(self.DUT.viscosity_design, 0.0)
        self.assertEqual(self.DUT.viscosity_dynamic, 0.0)
        self.assertEqual(self.DUT.water_per_cent, 0.0)
        self.assertEqual(self.DUT.width_minimum, 0.0)


class Test18RTKMode(unittest.TestCase):
    """
    Class for testing the RTKMode class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKMode class.
        """

        self.DUT = RTKMode()
        self.DUT.function_id = 1
        self.DUT.hardware_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkmode_create(self):
        """
        (TestDAO) DUT should create an RTKMode model.
        """

        self.assertTrue(isinstance(self.DUT, RTKMode))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_mode')
        self.assertEqual(self.DUT.mode_id, 1)
        self.assertEqual(self.DUT.critical_item, 0)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.design_provisions, '')
        self.assertEqual(self.DUT.detection_method, '')
        self.assertEqual(self.DUT.effect_end, '')
        self.assertEqual(self.DUT.effect_local, '')
        self.assertEqual(self.DUT.effect_next, '')
        self.assertEqual(self.DUT.effect_probability, 0.0)
        self.assertEqual(self.DUT.hazard_rate_source, '')
        self.assertEqual(self.DUT.isolation_method, '')
        self.assertEqual(self.DUT.mission, 'Default Mission')
        self.assertEqual(self.DUT.mission_phase, '')
        self.assertEqual(self.DUT.mode_criticality, 0.0)
        self.assertEqual(self.DUT.mode_hazard_rate, 0.0)
        self.assertEqual(self.DUT.mode_op_time, 0.0)
        self.assertEqual(self.DUT.mode_probability, '')
        self.assertEqual(self.DUT.mode_ratio, 0.0)
        self.assertEqual(self.DUT.operator_actions, '')
        self.assertEqual(self.DUT.other_indications, '')
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.rpn_severity, '')
        self.assertEqual(self.DUT.rpn_severity_new, '')
        self.assertEqual(self.DUT.severity_class, '')
        self.assertEqual(self.DUT.single_point, 0)
        self.assertEqual(self.DUT.type_id, 0)


class Test19RTKMechanism(unittest.TestCase):
    """
    Class for testing the RTKMechanism class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKMechanism class.
        """

        self.DUT = RTKMechanism()
        self.DUT.mode_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkmechanism_create(self):
        """
        (TestDAO) DUT should create an RTKMechanism model.
        """

        self.assertTrue(isinstance(self.DUT, RTKMechanism))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_mechanism')
        self.assertEqual(self.DUT.mechanism_id, 1)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.pof_include, 1)
        self.assertEqual(self.DUT.rpn, 0)
        self.assertEqual(self.DUT.rpn_detection, 0)
        self.assertEqual(self.DUT.rpn_detction_new, 0)
        self.assertEqual(self.DUT.rpn_new, 0)
        self.assertEqual(self.DUT.rpn_occurrence, 0)
        self.assertEqual(self.DUT.rpn_occurrence_new, 0)


class Test20RTKCause(unittest.TestCase):
    """
    Class for testing the RTKCause class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKCause class.
        """

        self.DUT = RTKCause()
        self.DUT.mechanism_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkcause_create(self):
        """
        (TestDAO) DUT should create an RTKCause model.
        """

        self.assertTrue(isinstance(self.DUT, RTKCause))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_cause')
        self.assertEqual(self.DUT.cause_id, 1)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.rpn, 0)
        self.assertEqual(self.DUT.rpn_detection, 0)
        self.assertEqual(self.DUT.rpn_detction_new, 0)
        self.assertEqual(self.DUT.rpn_new, 0)
        self.assertEqual(self.DUT.rpn_occurrence, 0)
        self.assertEqual(self.DUT.rpn_occurrence_new, 0)


class Test21RTKControl(unittest.TestCase):
    """
    Class for testing the RTKControl class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKControl class.
        """

        self.DUT = RTKControl()
        self.DUT.cause_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkcontrol_create(self):
        """
        (TestDAO) DUT should create an RTKControl model.
        """

        self.assertTrue(isinstance(self.DUT, RTKControl))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_control')
        self.assertEqual(self.DUT.control_id, 1)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.type_id, 0)


class Test22RTKAction(unittest.TestCase):
    """
    Class for testing the RTKAction class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKAction class.
        """

        self.DUT = RTKAction()
        self.DUT.cause_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkaction_create(self):
        """
        (TestDAO) DUT should create an RTKAction model.
        """

        self.assertTrue(isinstance(self.DUT, RTKAction))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_action')
        self.assertEqual(self.DUT.action_id, 1)
        self.assertEqual(self.DUT.action_recommended, '')
        self.assertEqual(self.DUT.action_category, 0)
        self.assertEqual(self.DUT.action_owner, 0)
        self.assertEqual(self.DUT.action_due_date,
                         date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.action_status_id, 0)
        self.assertEqual(self.DUT.action_taken, '')
        self.assertEqual(self.DUT.action_approved, 0)
        self.assertEqual(self.DUT.action_approve_date,
                         date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.action_closed, 0)
        self.assertEqual(self.DUT.action_close_date,
                         date.today() + timedelta(days=30))


class Test23RTKOpLoad(unittest.TestCase):
    """
    Class for testing the RTKOpLoad class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKOpLoad class.
        """

        self.DUT = RTKOpLoad()
        self.DUT.mechanism_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkopload_create(self):
        """
        (TestDAO) DUT should create an RTKOpLoad model.
        """

        self.assertTrue(isinstance(self.DUT, RTKOpLoad))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_op_load')
        self.assertEqual(self.DUT.load_id, 1)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.damage_model, 0)
        self.assertEqual(self.DUT.priority_id, 0)


class Test24RTKOpStress(unittest.TestCase):
    """
    Class for testing the RTKOpStress class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKOpStress class.
        """

        self.DUT = RTKOpStress()
        self.DUT.load_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkopstress_create(self):
        """
        (TestDAO) DUT should create an RTKOpStress model.
        """

        self.assertTrue(isinstance(self.DUT, RTKOpStress))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_op_stress')
        self.assertEqual(self.DUT.stress_id, 1)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.measurable_parameter, 0)
        self.assertEqual(self.DUT.load_history, 0)
        self.assertEqual(self.DUT.remarks, '')


class Test25RTKTestMethod(unittest.TestCase):
    """
    Class for testing the RTKTestMethod class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKTestMethod class.
        """

        self.DUT = RTKTestMethod()
        self.DUT.stress_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtktestmethod_create(self):
        """
        (TestDAO) DUT should create an RTKTestMethod model.
        """

        self.assertTrue(isinstance(self.DUT, RTKTestMethod))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_test_method')
        self.assertEqual(self.DUT.test_id, 1)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.boundary_conditions, '')
        self.assertEqual(self.DUT.remarks, '')


class Test26RTKSoftware(unittest.TestCase):
    """
    Class for testing the RTKSoftware class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKSoftware class.
        """

        self.DUT = RTKSoftware()
        self.DUT.revision_id = 0

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtksoftware_create(self):
        """
        (TestDAO) DUT should create an RTKSoftware model.
        """

        self.assertTrue(isinstance(self.DUT, RTKSoftware))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_software')
        self.assertEqual(self.DUT.software_id, 1)
        self.assertEqual(self.DUT.a, 0.0)
        self.assertEqual(self.DUT.aloc, 0)
        self.assertEqual(self.DUT.am, 0.0)
        self.assertEqual(self.DUT.application_id, 0)
        self.assertEqual(self.DUT.ax, 0)
        self.assertEqual(self.DUT.budget_test, 0.0)
        self.assertEqual(self.DUT.budget_dev, 0.0)
        self.assertEqual(self.DUT.bx, 0)
        self.assertEqual(self.DUT.category_id, 0)
        self.assertEqual(self.DUT.cb, 0)
        self.assertEqual(self.DUT.cx, 0)
        self.assertEqual(self.DUT.d, 0.0)
        self.assertEqual(self.DUT.dc, 0.0)
        self.assertEqual(self.DUT.dd, 0)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.development_id, 0)
        self.assertEqual(self.DUT.dev_assess_type_id, 0)
        self.assertEqual(self.DUT.df, 0.0)
        self.assertEqual(self.DUT.do, 0.0)
        self.assertEqual(self.DUT.dr, 0.0)
        self.assertEqual(self.DUT.dr_eot, 0)
        self.assertEqual(self.DUT.dr_test, 0)
        self.assertEqual(self.DUT.e, 0.0)
        self.assertEqual(self.DUT.ec, 0.0)
        self.assertEqual(self.DUT.et, 0.0)
        self.assertEqual(self.DUT.ev, 0.0)
        self.assertEqual(self.DUT.ew, 0.0)
        self.assertEqual(self.DUT.f, 0.0)
        self.assertEqual(self.DUT.ft1, 0.0)
        self.assertEqual(self.DUT.ft2, 0.0)
        self.assertEqual(self.DUT.hloc, 0)
        self.assertEqual(self.DUT.labor_hours_dev, 0.0)
        self.assertEqual(self.DUT.labor_hours_test, 0.0)
        self.assertEqual(self.DUT.level, 0)
        self.assertEqual(self.DUT.loc, 0)
        self.assertEqual(self.DUT.n_branches, 0)
        self.assertEqual(self.DUT.n_branches_test, 0)
        self.assertEqual(self.DUT.n_inputs, 0)
        self.assertEqual(self.DUT.n_inputs_test, 0)
        self.assertEqual(self.DUT.n_interfaces, 0)
        self.assertEqual(self.DUT.n_interfaces_test, 0)
        self.assertEqual(self.DUT.ncb, 0)
        self.assertEqual(self.DUT.nm, 0)
        self.assertEqual(self.DUT.nm_test, 0)
        self.assertEqual(self.DUT.os, 0.0)
        self.assertEqual(self.DUT.parent_id, 0)
        self.assertEqual(self.DUT.phase_id, 0)
        self.assertEqual(self.DUT.ren_avg, 0.0)
        self.assertEqual(self.DUT.ren_eot, 0.0)
        self.assertEqual(self.DUT.rpfom, 0.0)
        self.assertEqual(self.DUT.s1, 0.0)
        self.assertEqual(self.DUT.s2, 0.0)
        self.assertEqual(self.DUT.sa, 0.0)
        self.assertEqual(self.DUT.schedule_dev, 0.0)
        self.assertEqual(self.DUT.schedule_test, 0.0)
        self.assertEqual(self.DUT.sl, 0.0)
        self.assertEqual(self.DUT.sm, 0.0)
        self.assertEqual(self.DUT.sq, 0.0)
        self.assertEqual(self.DUT.sr, 0.0)
        self.assertEqual(self.DUT.st, 0.0)
        self.assertEqual(self.DUT.sx, 0.0)
        self.assertEqual(self.DUT.t, 0.0)
        self.assertEqual(self.DUT.tc, 0.0)
        self.assertEqual(self.DUT.tcl, 0)
        self.assertEqual(self.DUT.te, 0.0)
        self.assertEqual(self.DUT.test_approach, 0)
        self.assertEqual(self.DUT.test_effort, 0)
        self.assertEqual(self.DUT.test_path, 0)
        self.assertEqual(self.DUT.test_time, 0.0)
        self.assertEqual(self.DUT.test_time_eot, 0.0)
        self.assertEqual(self.DUT.tm, 0.0)
        self.assertEqual(self.DUT.um, 0)
        self.assertEqual(self.DUT.wm, 0)
        self.assertEqual(self.DUT.xm, 0)


class Test27RTKSoftwareDevelopment(unittest.TestCase):
    """
    Class for testing the RTKSoftwareDevelopment class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKSoftwareDevelopment class.
        """

        self.DUT = RTKSoftwareDevelopment()
        self.DUT.software_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtksoftwaredevelopment_create(self):
        """
        (TestDAO) DUT should create an RTKSoftwareDevelopment model.
        """

        self.assertTrue(isinstance(self.DUT, RTKSoftwareDevelopment))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_software_development')
        self.assertEqual(self.DUT.question_id, 1)
        self.assertEqual(self.DUT.answer, 0)


class Test28RTKSRRSSR(unittest.TestCase):
    """
    Class for testing the RTKSRRSSR class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKSRRSSR class.
        """

        self.DUT = RTKSRRSSR()
        self.DUT.software_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkssrsrr_create(self):
        """
        (TestDAO) DUT should create an RTKSRRSSR model.
        """

        self.assertTrue(isinstance(self.DUT, RTKSRRSSR))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_srr_ssr')
        self.assertEqual(self.DUT.question_id, 1)
        self.assertEqual(self.DUT.answer, 0)
        self.assertEqual(self.DUT.value, 0)


class Test29RTKPDR(unittest.TestCase):
    """
    Class for testing the RTKPDR class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKPDR class.
        """

        self.DUT = RTKPDR()
        self.DUT.software_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkpdr_create(self):
        """
        (TestDAO) DUT should create an RTKPDR model.
        """

        self.assertTrue(isinstance(self.DUT, RTKPDR))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_pdr')
        self.assertEqual(self.DUT.question_id, 1)
        self.assertEqual(self.DUT.answer, 0)
        self.assertEqual(self.DUT.value, 0)


class Test30RTKCDR(unittest.TestCase):
    """
    Class for testing the RTKCDR class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKCDR class.
        """

        self.DUT = RTKCDR()
        self.DUT.software_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkcdr_create(self):
        """
        (TestDAO) DUT should create an RTKCDR model.
        """

        self.assertTrue(isinstance(self.DUT, RTKCDR))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_cdr')
        self.assertEqual(self.DUT.question_id, 1)
        self.assertEqual(self.DUT.answer, 0)
        self.assertEqual(self.DUT.value, 0)


class Test31RTKTRR(unittest.TestCase):
    """
    Class for testing the RTKTRR class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKTRR class.
        """

        self.DUT = RTKTRR()
        self.DUT.software_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtktrr_create(self):
        """
        (TestDAO) DUT should create an RTKTRR model.
        """

        self.assertTrue(isinstance(self.DUT, RTKTRR))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_trr')
        self.assertEqual(self.DUT.question_id, 1)
        self.assertEqual(self.DUT.answer, 0)
        self.assertEqual(self.DUT.value, 0)


class Test32RTKSoftwareTest(unittest.TestCase):
    """
    Class for testing the RTKSoftwareTest class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKSoftwareTest class.
        """

        self.DUT = RTKSoftwareTest()
        self.DUT.software_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtksoftwaretest_create(self):
        """
        (TestDAO) DUT should create an RTKSoftwareTest model.
        """

        self.assertTrue(isinstance(self.DUT, RTKSoftwareTest))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_software_test')
        self.assertEqual(self.DUT.technique_id, 1)
        self.assertEqual(self.DUT.recommended, 0)
        self.assertEqual(self.DUT.used, 0)


class Test33RTKValidation(unittest.TestCase):
    """
    Class for testing the RTKValidation class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKValidation class.
        """

        self.DUT = RTKValidation()
        self.DUT.revision_id = 0

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkvalidation_create(self):
        """
        (TestDAO) DUT should create an RTKValidation model.
        """

        self.assertTrue(isinstance(self.DUT, RTKValidation))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_validation')
        self.assertEqual(self.DUT.validation_id, 1)
        self.assertEqual(self.DUT.acceptable_maximum, 0.0)
        self.assertEqual(self.DUT.acceptable_mean, 0.0)
        self.assertEqual(self.DUT.acceptable_minimum, 0.0)
        self.assertEqual(self.DUT.acceptable_variance, 0.0)
        self.assertEqual(self.DUT.confidence, 95.0)
        self.assertEqual(self.DUT.cost_average, 0.0)
        self.assertEqual(self.DUT.cost_maximum, 0.0)
        self.assertEqual(self.DUT.cost_mean, 0.0)
        self.assertEqual(self.DUT.cost_minimum, 0.0)
        self.assertEqual(self.DUT.cost_variance, 0.0)
        self.assertEqual(self.DUT.date_end, date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.date_start, date.today())
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.measurement_unit_id, 0)
        self.assertEqual(self.DUT.status_id, 0.0)
        self.assertEqual(self.DUT.task_type_id, 0)
        self.assertEqual(self.DUT.task_specification, '')
        self.assertEqual(self.DUT.time_average, 0.0)
        self.assertEqual(self.DUT.time_maximum, 0.0)
        self.assertEqual(self.DUT.time_mean, 0.0)
        self.assertEqual(self.DUT.time_minimum, 0.0)
        self.assertEqual(self.DUT.time_variance, 0.0)


class Test34RTKIncident(unittest.TestCase):
    """
    Class for testing the RTKIncident class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKIncident class.
        """

        self.DUT = RTKIncident()
        self.DUT.revision_id = 0

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkincident_create(self):
        """
        (TestDAO) DUT should create an RTKIncident model.
        """

        self.assertTrue(isinstance(self.DUT, RTKIncident))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_incident')
        self.assertEqual(self.DUT.incident_id, 1)
        self.assertEqual(self.DUT.accepted, 0)
        self.assertEqual(self.DUT.approved, 0)
        self.assertEqual(self.DUT.approved_by, 0)
        self.assertEqual(self.DUT.analysis, '')
        self.assertEqual(self.DUT.category_id, 0)
        self.assertEqual(self.DUT.chargeable, -1)
        self.assertEqual(self.DUT.chargeable_1, -1)
        self.assertEqual(self.DUT.chargeable_2, -1)
        self.assertEqual(self.DUT.chargeable_3, -1)
        self.assertEqual(self.DUT.chargeable_4, -1)
        self.assertEqual(self.DUT.chargeable_5, -1)
        self.assertEqual(self.DUT.chargeable_6, -1)
        self.assertEqual(self.DUT.chargeable_7, -1)
        self.assertEqual(self.DUT.chargeable_8, -1)
        self.assertEqual(self.DUT.chargeable_9, -1)
        self.assertEqual(self.DUT.chargeable_10, -1)
        self.assertEqual(self.DUT.complete, 0)
        self.assertEqual(self.DUT.complete_by, 0)
        self.assertEqual(self.DUT.cost, 0)
        self.assertEqual(self.DUT.criticality_id, 0)
        self.assertEqual(self.DUT.date_approved,
                         date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.date_complete,
                         date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.date_requested, date.today())
        self.assertEqual(self.DUT.date_reviewed,
                         date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.description_long, '')
        self.assertEqual(self.DUT.description_short, '')
        self.assertEqual(self.DUT.detection_method_id, 0)
        self.assertEqual(self.DUT.execution_time, 0)
        self.assertEqual(self.DUT.hardware_id, 0)
        self.assertEqual(self.DUT.incident_age, 0)
        self.assertEqual(self.DUT.life_cycle_id, 0)
        self.assertEqual(self.DUT.relevant, -1)
        self.assertEqual(self.DUT.relevant_1, -1)
        self.assertEqual(self.DUT.relevant_2, -1)
        self.assertEqual(self.DUT.relevant_3, -1)
        self.assertEqual(self.DUT.relevant_4, -1)
        self.assertEqual(self.DUT.relevant_5, -1)
        self.assertEqual(self.DUT.relevant_6, -1)
        self.assertEqual(self.DUT.relevant_7, -1)
        self.assertEqual(self.DUT.relevant_8, -1)
        self.assertEqual(self.DUT.relevant_9, -1)
        self.assertEqual(self.DUT.relevant_10, -1)
        self.assertEqual(self.DUT.relevant_11, -1)
        self.assertEqual(self.DUT.relevant_12, -1)
        self.assertEqual(self.DUT.relevant_13, -1)
        self.assertEqual(self.DUT.relevant_14, -1)
        self.assertEqual(self.DUT.relevant_15, -1)
        self.assertEqual(self.DUT.relevant_16, -1)
        self.assertEqual(self.DUT.relevant_17, -1)
        self.assertEqual(self.DUT.relevant_18, -1)
        self.assertEqual(self.DUT.relevant_19, -1)
        self.assertEqual(self.DUT.relevant_20, -1)
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.request_by, 0)
        self.assertEqual(self.DUT.reviewed, 0)
        self.assertEqual(self.DUT.reviewed_by, 0)
        self.assertEqual(self.DUT.software_id, 0)
        self.assertEqual(self.DUT.status_id, 0)
        self.assertEqual(self.DUT.test_case, '')
        self.assertEqual(self.DUT.test_found, '')
        self.assertEqual(self.DUT.type_id, 0)
        self.assertEqual(self.DUT.unit, '')


class Test35RTKIncidentDetail(unittest.TestCase):
    """
    Class for testing the RTKIncidentDetail class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKIncidentDetail class.
        """

        self.DUT = RTKIncidentDetail()
        self.DUT.incident_id = 1
        self.DUT.hardware_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkincidentdetail_create(self):
        """
        (TestDAO) DUT should create an RTKIncidentDetail model.
        """

        self.assertTrue(isinstance(self.DUT, RTKIncidentDetail))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_incident_detail')
        self.assertEqual(self.DUT.hardware_id, 1)
        self.assertEqual(self.DUT.fld_age_at_incident, 0)
        self.assertEqual(self.DUT.fld_failure, 0)
        self.assertEqual(self.DUT.fld_suspension, 0)
        self.assertEqual(self.DUT.fld_cnd_nff, 0)
        self.assertEqual(self.DUT.fld_occ_fault, 0)
        self.assertEqual(self.DUT.fld_initial_installation, 0)
        self.assertEqual(self.DUT.fld_interval_censored, 0)
        self.assertEqual(self.DUT.fld_use_op_time, 0)
        self.assertEqual(self.DUT.fld_use_cal_time, 0)
        self.assertEqual(self.DUT.fld_ttf, 0.0)
        self.assertEqual(self.DUT.fld_mode_type_id, 0)


class Test36RTKIncidentAction(unittest.TestCase):
    """
    Class for testing the RTKIncidentAction class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKIncidentAction class.
        """

        self.DUT = RTKIncidentAction()
        self.DUT.incident_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkincidentaction_create(self):
        """
        (TestDAO) DUT should create an RTKIncidentAction model.
        """

        self.assertTrue(isinstance(self.DUT, RTKIncidentAction))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_incident_action')
        self.assertEqual(self.DUT.action_id, 1)
        self.assertEqual(self.DUT.action_owner, 0)
        self.assertEqual(self.DUT.action_prescribed, '')
        self.assertEqual(self.DUT.action_taken, '')
        self.assertEqual(self.DUT.approved, 0)
        self.assertEqual(self.DUT.approved_by, 0)
        self.assertEqual(self.DUT.approved_date,
                         date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.closed, 0)
        self.assertEqual(self.DUT.closed_by, 0)
        self.assertEqual(self.DUT.closed_date,
                         date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.due_date, date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.status_id, 0)


class Test37RTKTest(unittest.TestCase):
    """
    Class for testing the RTKTest class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKTest class.
        """

        self.DUT = RTKTest()
        self.DUT.revision_id = 0

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtktest_create(self):
        """
        (TestDAO) DUT should create an RTKTest model.
        """

        self.assertTrue(isinstance(self.DUT, RTKTest))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_test')
        self.assertEqual(self.DUT.test_id, 1)
        self.assertEqual(self.DUT.assess_model_id, 0)
        self.assertEqual(self.DUT.attachment, '')
        self.assertEqual(self.DUT.avg_fef, 0.0)
        self.assertEqual(self.DUT.avg_growth, 0.0)
        self.assertEqual(self.DUT.avg_ms, 0.0)
        self.assertEqual(self.DUT.chi_square, 0.0)
        self.assertEqual(self.DUT.confidence, 0.0)
        self.assertEqual(self.DUT.consumer_risk, 0.0)
        self.assertEqual(self.DUT.cramer_vonmises, 0.0)
        self.assertEqual(self.DUT.cum_failures, 0)
        self.assertEqual(self.DUT.cum_mean, 0.0)
        self.assertEqual(self.DUT.cum_mean_ll, 0.0)
        self.assertEqual(self.DUT.cum_mean_se, 0.0)
        self.assertEqual(self.DUT.cum_mean_ul, 0.0)
        self.assertEqual(self.DUT.cum_time, 0.0)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.grouped, 0)
        self.assertEqual(self.DUT.group_interval, 0.0)
        self.assertEqual(self.DUT.inst_mean, 0.0)
        self.assertEqual(self.DUT.inst_mean_ll, 0.0)
        self.assertEqual(self.DUT.inst_mean_se, 0.0)
        self.assertEqual(self.DUT.inst_mean_ul, 0.0)
        self.assertEqual(self.DUT.mg, 0.0)
        self.assertEqual(self.DUT.mgp, 0.0)
        self.assertEqual(self.DUT.n_phases, 1)
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.plan_model_id, 0)
        self.assertEqual(self.DUT.prob, 75.0)
        self.assertEqual(self.DUT.producer_risk, 0.0)
        self.assertEqual(self.DUT.scale, 0.0)
        self.assertEqual(self.DUT.scale_ll, 0.0)
        self.assertEqual(self.DUT.scale_se, 0.0)
        self.assertEqual(self.DUT.scale_ul, 0.0)
        self.assertEqual(self.DUT.shape, 0.0)
        self.assertEqual(self.DUT.shape_ll, 0.0)
        self.assertEqual(self.DUT.shape_se, 0.0)
        self.assertEqual(self.DUT.shape_ul, 0.0)
        self.assertEqual(self.DUT.tr, 0.0)
        self.assertEqual(self.DUT.ttt, 0.0)
        self.assertEqual(self.DUT.ttff, 0.0)
        self.assertEqual(self.DUT.type_id, 0)


class Test38RTKGrowthTest(unittest.TestCase):
    """
    Class for testing the RTKGrowthTest class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKGrowthTest class.
        """

        self.DUT = RTKGrowthTest()
        self.DUT.test_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtkgrowthtest_create(self):
        """
        (TestDAO) DUT should create an RTKGrowthTest model.
        """

        self.assertTrue(isinstance(self.DUT, RTKGrowthTest))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_growth_test')
        self.assertEqual(self.DUT.phase_id, 1)
        self.assertEqual(self.DUT.i_mi, 0.0)
        self.assertEqual(self.DUT.i_mf, 0.0)
        self.assertEqual(self.DUT.i_ma, 0.0)
        self.assertEqual(self.DUT.i_num_fails, 0)
        self.assertEqual(self.DUT.p_growth_rate, 0.0)
        self.assertEqual(self.DUT.p_ms, 0.0)
        self.assertEqual(self.DUT.p_fef_avg, 0.0)
        self.assertEqual(self.DUT.p_prob, 0.0)
        self.assertEqual(self.DUT.p_mi, 0.0)
        self.assertEqual(self.DUT.p_mf, 0.0)
        self.assertEqual(self.DUT.p_ma, 0.0)
        self.assertEqual(self.DUT.p_test_time, 0.0)
        self.assertEqual(self.DUT.p_num_fails, 0)
        self.assertEqual(self.DUT.p_start_date, date.today())
        self.assertEqual(self.DUT.p_end_date, date.today())
        self.assertEqual(self.DUT.p_weeks, 0.0)
        self.assertEqual(self.DUT.p_test_units, 0)
        self.assertEqual(self.DUT.p_tpu, 0.0)
        self.assertEqual(self.DUT.p_tpupw, 0.0)
        self.assertEqual(self.DUT.o_growth_rate, 0.0)
        self.assertEqual(self.DUT.o_ms, 0.0)
        self.assertEqual(self.DUT.o_fef_avg, 0.0)
        self.assertEqual(self.DUT.o_mi, 0.0)
        self.assertEqual(self.DUT.o_mf, 0.0)
        self.assertEqual(self.DUT.o_ma, 0.0)
        self.assertEqual(self.DUT.o_test_time, 0.0)
        self.assertEqual(self.DUT.o_num_fails, 0)
        self.assertEqual(self.DUT.o_ttff, 0.0)


class Test39RTKSurvival(unittest.TestCase):
    """
    Class for testing the RTKSurvival class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKSurvival class.
        """

        self.DUT = RTKSurvival()
        self.DUT.revision_id = 0

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtksurvival_create(self):
        """
        (TestDAO) DUT should create an RTKSurvival model.
        """

        self.assertTrue(isinstance(self.DUT, RTKSurvival))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_survival')
        self.assertEqual(self.DUT.survival_id, 1)
        self.assertEqual(self.DUT.hardware_id, 0)
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.source_id, 0)
        self.assertEqual(self.DUT.distribution_id, 0)
        self.assertEqual(self.DUT.confidence, 75.0)
        self.assertEqual(self.DUT.confidence_type_id, 0)
        self.assertEqual(self.DUT.confidence_method_id, 0)
        self.assertEqual(self.DUT.fit_method_id, 0)
        self.assertEqual(self.DUT.rel_time, 0.0)
        self.assertEqual(self.DUT.n_rel_points, 0)
        self.assertEqual(self.DUT.n_suspension, 0)
        self.assertEqual(self.DUT.n_failures, 0)
        self.assertEqual(self.DUT.scale_ll, 0.0)
        self.assertEqual(self.DUT.scale, 0.0)
        self.assertEqual(self.DUT.scale_ul, 0.0)
        self.assertEqual(self.DUT.shape_ll, 0.0)
        self.assertEqual(self.DUT.shape, 0.0)
        self.assertEqual(self.DUT.shape_ul, 0.0)
        self.assertEqual(self.DUT.location_ll, 0.0)
        self.assertEqual(self.DUT.location, 0.0)
        self.assertEqual(self.DUT.location_ul, 0.0)
        self.assertEqual(self.DUT.variance_1, 0.0)
        self.assertEqual(self.DUT.variance_2, 0.0)
        self.assertEqual(self.DUT.variance_3, 0.0)
        self.assertEqual(self.DUT.covariance_1, 0.0)
        self.assertEqual(self.DUT.covariance_2, 0.0)
        self.assertEqual(self.DUT.covariance_3, 0.0)
        self.assertEqual(self.DUT.mhb, 0.0)
        self.assertEqual(self.DUT.lp, 0.0)
        self.assertEqual(self.DUT.lr, 0.0)
        self.assertEqual(self.DUT.aic, 0.0)
        self.assertEqual(self.DUT.bic, 0.0)
        self.assertEqual(self.DUT.mle, 0.0)
        self.assertEqual(self.DUT.start_time, 0.0)
        self.assertEqual(self.DUT.start_date, date.today())
        self.assertEqual(self.DUT.end_date, date.today() + timedelta(days=30))
        self.assertEqual(self.DUT.nevada_chart, 0)


class Test39RTKSurvivalData(unittest.TestCase):
    """
    Class for testing the RTKSurvivalData class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the RTKSurvivalData class.
        """

        self.DUT = RTKSurvivalData()
        self.DUT.survival_id = 1

        session.add(self.DUT)
        session.commit()

    @attr(all=True, dynamic=True)
    def test00_rtksurvivaldata_create(self):
        """
        (TestDAO) DUT should create an RTKSurvivalData model.
        """

        self.assertTrue(isinstance(self.DUT, RTKSurvivalData))

        # Verify class attributes are properly initialized.
        self.assertEqual(self.DUT.__tablename__, 'rtk_survival_data')
        self.assertEqual(self.DUT.record_id, 1)
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.source_id, 0)
        self.assertEqual(self.DUT.failure_date, date.today())
        self.assertEqual(self.DUT.left_interval, 0.0)
        self.assertEqual(self.DUT.right_interval, 0.0)
        self.assertEqual(self.DUT.status_id, 0)
        self.assertEqual(self.DUT.quantity, 0)
        self.assertEqual(self.DUT.tbf, 0.0)
        self.assertEqual(self.DUT.mode_type_id, 0)
        self.assertEqual(self.DUT.nevada_chart, 0)
        self.assertEqual(self.DUT.ship_date, date.today())
        self.assertEqual(self.DUT.number_shipped, 0)
        self.assertEqual(self.DUT.return_date, date.today())
        self.assertEqual(self.DUT.number_returned, 0)
        self.assertEqual(self.DUT.user_float_1, 0.0)
        self.assertEqual(self.DUT.user_float_2, 0.0)
        self.assertEqual(self.DUT.user_float_3, 0.0)
        self.assertEqual(self.DUT.user_integer_1, 0)
        self.assertEqual(self.DUT.user_integer_2, 0)
        self.assertEqual(self.DUT.user_integer_3, 0)
        self.assertEqual(self.DUT.user_string_1, '')
        self.assertEqual(self.DUT.user_string_2, '')
        self.assertEqual(self.DUT.user_string_3, '')
