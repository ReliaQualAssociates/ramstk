# pylint: disable=protected-access
# -*- coding: utf-8 -*-
#
#       ramstk.tests.modules.test_preferences.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2018 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Preferences class. """

# Standard Library Imports
import glob
import os
import platform
import sys

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.dao import DAO
from ramstk.dao.commondb import RAMSTKUser
from ramstk.modules.preferences import dtcPreferences, dtmPreferences
from ramstk.modules.preferences.Model import (
    SitePreferencesDataModel, UserPreferencesDataModel,
)

ATTRIBUTES = {'revision_id': 1, 'site_dao': '', 'site': True, 'user': True}

try:
    VIRTUAL_ENV = glob.glob(os.environ['VIRTUAL_ENV'])[0]
except KeyError:
    if platform.system() == 'Linux':
        VIRTUAL_ENV = os.getenv('HOME') + '/.local'
    elif platform.system() == 'Windows':
        VIRTUAL_ENV = os.getenv('TEMP')
    else:
        print((
            "The {0:s} system platform is not "
            "supported."
        ).format(platform.system()))
        sys.exit(1)

CONF_DIR = VIRTUAL_ENV + '/share/RAMSTK'
DATA_DIR = CONF_DIR + '/layouts'
ICON_DIR = CONF_DIR + '/icons'
TMP_DIR = VIRTUAL_ENV + '/tmp'
LOG_DIR = TMP_DIR + '/logs'
TEST_COMMON_DB_PATH = VIRTUAL_ENV + '/share/RAMSTK/ramstk_common.ramstk'
TEST_PROGRAM_DB_PATH = TMP_DIR + '/TestDB.ramstk'


@pytest.mark.integration
def test_create_preferences_data_model(
        test_dao, test_common_dao,
        test_configuration,
):
    """ __init__() should return an instance of the Preferences data model. """
    DUT = dtmPreferences(test_dao, test_common_dao, test_configuration)

    assert isinstance(DUT, dtmPreferences)
    assert isinstance(DUT.dao, DAO)
    assert isinstance(DUT.dtm_site_preferences, SitePreferencesDataModel)
    assert isinstance(DUT.dtm_user_preferences, UserPreferencesDataModel)
    assert isinstance(DUT.site_preferences, dict)
    assert isinstance(DUT.user_preferences, dict)


@pytest.mark.integration
def test_do_select_all_site_preferences(
        test_dao, test_common_dao,
        test_configuration,
):
    """ do_select_all() should return None on success when selecting site Preferences. """
    DUT = dtmPreferences(test_dao, test_common_dao, test_configuration)
    DUT.do_select_all(site=True, user=False)

    assert isinstance(DUT.site_preferences, dict)

    assert isinstance(DUT.site_preferences['action_category'], list)
    assert isinstance(DUT.site_preferences['incident_category'], list)
    assert isinstance(DUT.site_preferences['damaging_conditions'], list)
    assert isinstance(DUT.site_preferences['environment_conditions'], list)
    assert isinstance(DUT.site_preferences['failure_modes'], list)
    assert isinstance(DUT.site_preferences['affinity_groups'], list)
    assert isinstance(DUT.site_preferences['workgroups'], list)
    assert isinstance(DUT.site_preferences['hazards'], list)
    assert isinstance(DUT.site_preferences['load_history'], list)
    assert isinstance(DUT.site_preferences['manufacturers'], list)
    assert isinstance(DUT.site_preferences['measurement_units'], list)
    assert isinstance(DUT.site_preferences['measureable_parameters'], list)
    assert isinstance(DUT.site_preferences['detection_methods'], list)
    assert isinstance(DUT.site_preferences['damage_models'], list)
    assert isinstance(DUT.site_preferences['rpn_detection'], list)
    assert isinstance(DUT.site_preferences['rpn_occurrence'], list)
    assert isinstance(DUT.site_preferences['rpn_severity'], list)
    assert isinstance(DUT.site_preferences['stakeholders'], list)
    assert isinstance(DUT.site_preferences['action_status'], list)
    assert isinstance(DUT.site_preferences['incident_status'], list)
    assert isinstance(DUT.site_preferences['requirement_types'], list)
    assert isinstance(DUT.site_preferences['validation_types'], list)
    assert isinstance(DUT.site_preferences['incident_types'], list)
    assert isinstance(DUT.site_preferences['users'], list)


@pytest.mark.integration
def test_do_select_all_user_preferences(
        test_dao, test_common_dao,
        test_configuration,
):
    """ do_select_all() should return None on success when selecting program Preferences. """
    DUT = dtmPreferences(test_dao, test_common_dao, test_configuration)
    DUT.do_select_all(site=False, user=True)

    assert DUT.user_preferences['common_db_info'] == {
        'type': 'sqlite',
        'host': 'localhost',
        'socket': '3306',
        'database': TEST_COMMON_DB_PATH,
        'user': 'ramstkcom',
        'password': 'ramstkcom',
        'path': 'ramstkcom',
    }
    assert DUT.user_preferences['program_db_info'] == {
        'type': 'sqlite',
        'host': 'localhost',
        'socket': '3306',
        'database': TEST_PROGRAM_DB_PATH,
        'user': 'johnny.tester',
        'password': 'clear.text.password',
    }
    assert DUT.user_preferences['report_size'] == 'letter'
    assert float(DUT.user_preferences['hr_multiplier']) == 1000000.0
    assert int(DUT.user_preferences['decimal']) == 6
    assert float(DUT.user_preferences['calcreltime']) == 100.0
    assert DUT.user_preferences['tabpos'] == {
        'modulebook': 'top',
        'listbook': 'bottom',
        'workbook': 'bottom',
    }
    assert DUT.user_preferences['sitedir'] == VIRTUAL_ENV + '/share/RAMSTK'
    assert DUT.user_preferences['datadir'] == DATA_DIR
    assert DUT.user_preferences[
        'icondir'
    ] == VIRTUAL_ENV + '/share/RAMSTK/icons'
    assert DUT.user_preferences['logdir'] == LOG_DIR
    assert DUT.user_preferences['progdir'] == TMP_DIR
    assert DUT.user_preferences['format_files'] == {
        'allocation': 'Allocation.xml',
        'failure_definition': 'FailureDefinition.xml',
        'fmea': 'FMEA.xml',
        'function': 'Function.xml',
        'hardware': 'Hardware.xml',
        'hazops': 'HazOps.xml',
        'pof': 'PoF.xml',
        'requirement': 'Requirement.xml',
        'revision': 'Revision.xml',
        'similaritem': 'SimilarItem.xml',
        'stakeholder': 'Stakeholder.xml',
        'validation': 'Validation.xml',
    }
    assert DUT.user_preferences['colors'] == {
        'functionbg': '#FFFFFF',
        'functionfg': '#000000',
        'hardwarebg': '#FFFFFF',
        'hardwarefg': '#000000',
        'requirementbg': '#FFFFFF',
        'requirementfg': '#000000',
        'revisionbg': '#FFFFFF',
        'revisionfg': '#000000',
        'stakeholderbg': '#FFFFFF',
        'stakeholderfg': '#000000',
        'validationbg': '#FFFFFF',
        'validationfg': '#000000',
    }


@pytest.mark.integration
def test_do_update_site_preferences(
        test_dao, test_common_dao,
        test_configuration,
):
    """ do_update() should return a zero error code on success when updating site preferences. """
    DUT = dtmPreferences(test_dao, test_common_dao, test_configuration)
    DUT.do_select_all(site=True, user=True)

    _model = DUT.site_preferences['damage_models'][0]
    _model.description = 'Damage Model #9'
    assert not DUT.do_update()

    DUT.do_select_all(site=True, user=True)
    assert DUT.site_preferences['damage_models'][
        0
    ].description == 'Damage Model #9'


@pytest.mark.integration
def test_do_update_user_preferences(
        test_dao, test_common_dao,
        test_configuration,
):
    """ do_update() should return a zero error code on success when updating user preferences. """
    DUT = dtmPreferences(test_dao, test_common_dao, test_configuration)
    DUT.do_select_all(site=True, user=True)

    DUT.user_preferences['report_size'] = 'A4'
    assert not DUT.do_update()

    DUT.do_select_all(site=True, user=True)
    assert DUT.user_preferences['report_size'] == 'A4'


@pytest.mark.integration
def test_create_preferences_data_controller(
        test_dao, test_common_dao,
        test_configuration,
):
    """ __init__() should return instance of Preferences data controller. """
    DUT = dtcPreferences(
        test_dao, test_configuration, site_dao=test_common_dao, test='True',
    )

    assert isinstance(DUT, dtcPreferences)
    assert isinstance(DUT._dtm_data_model, dtmPreferences)


@pytest.mark.integration
def test_request_do_select_all(test_dao, test_common_dao, test_configuration):
    """ request_do_select_all() should return a Tree of RAMSTKPreferences data models. """
    DUT = dtcPreferences(
        test_dao, test_configuration, site_dao=test_common_dao, test='True',
    )

    assert not DUT.request_do_select_all(ATTRIBUTES)


@pytest.mark.integration
def test_request_get_preferences_site(
        test_dao, test_common_dao,
        test_configuration,
):
    """ request_get_preferences() should return a dict of dicts of site option:value pairs. """
    DUT = dtcPreferences(
        test_dao, test_configuration, site_dao=test_common_dao, test='True',
    )
    DUT.request_do_select_all(ATTRIBUTES)

    _preferences = DUT.request_get_preferences(site=True, user=False)

    assert isinstance(_preferences, dict)
    assert 'detection_methods' in list(_preferences.keys())
    assert 'incident_status' in list(_preferences.keys())
    assert 'environment_conditions' in list(_preferences.keys())
    assert 'action_status' in list(_preferences.keys())
    assert 'measurement_units' in list(_preferences.keys())
    assert 'damage_models' in list(_preferences.keys())
    assert 'workgroups' in list(_preferences.keys())
    assert 'users' in list(_preferences.keys())
    assert 'hazards' in list(_preferences.keys())
    assert 'action_category' in list(_preferences.keys())
    assert 'load_history' in list(_preferences.keys())
    assert 'stakeholders' in list(_preferences.keys())
    assert 'rpn_detection' in list(_preferences.keys())
    assert 'manufacturers' in list(_preferences.keys())
    assert 'rpn_occurrence' in list(_preferences.keys())
    assert 'failure_modes' in list(_preferences.keys())
    assert 'validation_types' in list(_preferences.keys())
    assert 'damaging_conditions' in list(_preferences.keys())
    assert 'measureable_parameters' in list(_preferences.keys())
    assert 'incident_types' in list(_preferences.keys())
    assert 'rpn_severity' in list(_preferences.keys())
    assert 'requirement_types' in list(_preferences.keys())
    assert 'incident_category' in list(_preferences.keys())
    assert 'affinity_groups' in list(_preferences.keys())


@pytest.mark.integration
def test_request_get_preferences_user(
        test_dao, test_common_dao,
        test_configuration,
):
    """ request_get_preferences() should return a dict of program option:value pairs. """
    DUT = dtcPreferences(
        test_dao, test_configuration, site_dao=test_common_dao, test='True',
    )
    DUT.request_do_select_all(ATTRIBUTES)

    _preferences = DUT.request_get_preferences(site=False, user=True)

    assert isinstance(_preferences, dict)
    assert 'hr_multiplier' in list(_preferences.keys())
    assert 'report_size' in list(_preferences.keys())
    assert 'decimal' in list(_preferences.keys())
    assert 'icondir' in list(_preferences.keys())
    assert 'colors' in list(_preferences.keys())
    assert 'common_db_info' in list(_preferences.keys())
    assert 'datadir' in list(_preferences.keys())
    assert 'tabpos' in list(_preferences.keys())
    assert 'calcreltime' in list(_preferences.keys())
    assert 'logdir' in list(_preferences.keys())
    assert 'sitedir' in list(_preferences.keys())
    assert 'program_db_info' in list(_preferences.keys())
    assert 'format_files' in list(_preferences.keys())
    assert 'progdir' in list(_preferences.keys())


@pytest.mark.integration
def test_request_do_update(test_dao, test_common_dao, test_configuration):
    """ request_do_update() should return False on success. """
    DUT = dtcPreferences(
        test_dao, test_configuration, site_dao=test_common_dao, test='True',
    )
    DUT.request_do_select_all(ATTRIBUTES)

    DUT.request_get_preferences(site=False, user=True)
    DUT._dtm_data_model.user_preferences['hr_multiplier'] = 1.0

    _new_user = RAMSTKUser()
    _new_user.user_lname = 'Rowland'
    _new_user.user_fname = 'Doyle'
    _new_user.user_email = 'doyle.rowland@rwliaqual.com'
    _new_user.user_phone = '269.491.4766'
    _new_user.user_group_id = 1
    DUT._dtm_data_model.site_preferences['users'].append(_new_user)

    assert not DUT.request_do_update()
