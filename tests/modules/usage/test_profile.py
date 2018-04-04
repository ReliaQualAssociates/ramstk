#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.modules.usage.test_profile.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for Usage Profile algorithms and models."""

from treelib import Tree

import pytest

from rtk.dao import (RTKMission, RTKMissionPhase, RTKEnvironment)
from rtk.modules.usage import (dtmEnvironment, dtmMission, dtmMissionPhase,
                               dtmUsageProfile, dtcUsageProfile)

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Doyle "Weibullguy" Rowland'

ATTRIBUTES = {
    'mission_id': 1,
    'revision_id': 1,
    'mission_time': 72.0,
    'description': 'Test Mission Description',
    'time_units': u'minutes'
}


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_create_data_model(test_dao):
    """ __init__() should create a Usage Profile data model. """
    DUT = dtmUsageProfile(test_dao)

    assert isinstance(DUT, dtmUsageProfile)
    assert isinstance(DUT.dtm_mission, dtmMission)
    assert isinstance(DUT.dtm_phase, dtmMissionPhase)
    assert isinstance(DUT.dtm_environment, dtmEnvironment)
    assert isinstance(DUT.tree, Tree)
    assert DUT.last_id is None
    assert DUT.dao == test_dao


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_select_all(test_dao):
    """ select_all() should return an empty Tree() when passed a Revision ID that doesn't exist. """
    DUT = dtmUsageProfile(test_dao)
    _tree = DUT.select_all(1)

    assert isinstance(_tree, Tree)
    assert _tree.get_node(0).tag == 'Usage Profiles'
    assert isinstance(_tree.get_node(1).data, RTKMission)
    assert isinstance(_tree.get_node(11).data, RTKMissionPhase)
    assert isinstance(_tree.get_node(111).data, RTKEnvironment)


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_select_all_non_existent_id(test_dao):
    """ select_all() should return an empty Tree() when passed a Revision ID that doesn't exist. """
    DUT = dtmUsageProfile(test_dao)
    _tree = DUT.select_all(100)

    assert isinstance(_tree, Tree)
    assert _tree.get_node(0).tag == 'Usage Profiles'
    assert _tree.get_node(1) is None


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_select(test_dao):
    """ select() should return a Tree() on success. """
    DUT = dtmUsageProfile(test_dao)
    DUT.select_all(1)

    _entity = DUT.select(1)

    assert isinstance(_entity, RTKMission)
    assert _entity.description == 'Test Mission Description'


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_insert_mission(test_dao):
    """ insert() should return a zero error code on success when adding a new Mission. """
    DUT = dtmUsageProfile(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(entity_id=1, parent_id=0, level='mission')

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")
    assert isinstance(DUT.select(2), RTKMission)


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_insert_phase(test_dao):
    """ insert() should return a zero error code on success when adding a new Mission Phase. """
    DUT = dtmUsageProfile(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(entity_id=2, parent_id=1, level='phase')

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")
    assert isinstance(DUT.select(12), RTKMissionPhase)


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_insert_environment(test_dao):
    """ insert() should return a zero error code on success when adding a new Environment. """
    DUT = dtmUsageProfile(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(
        entity_id=2, parent_id=11, level='environment')

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK Program "
                    "database.")
    assert isinstance(DUT.tree.get_node(112).data, RTKEnvironment)


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_insert_non_existent_type(test_dao):
    """ insert() should return a 2105 error code when attempting to add something other than a Mission, Phase, or Environment. """
    DUT = dtmUsageProfile(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.insert(
        entity_id=1, parent_id=0, level='scadamoosh')

    assert _error_code == 2105
    assert _msg == ("RTK ERROR: Attempted to add an item to the Usage Profile "
                    "with an undefined indenture level.  Level scadamoosh was "
                    "requested.  Must be one of mission, phase, or "
                    "environment.")


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_delete_environment(test_dao):
    """ delete() should return a zero error code on success when removing an Environment. """
    DUT = dtmUsageProfile(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(223)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_delete_non_existent_node_id(test_dao):
    """ delete() should return a 2005 error code when attempting to remove a non-existant item from the Profile. """
    DUT = dtmUsageProfile(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.delete(4)

    assert _error_code == 2005
    assert _msg == ("  RTK ERROR: Attempted to delete non-existent Usage "
                    "Profile entity with Node ID 4.")


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmUsageProfile(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update(1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_update_non_existent_node_id(test_dao):
    """ update() should return a 2006 error code when attempting to update a non-existent Node ID. """
    DUT = dtmUsageProfile(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == ("RTK ERROR: Attempted to save non-existent Usage Profile "
                    "entity with Node ID 100.")


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmUsageProfile(test_dao)
    DUT.select_all(1)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating the RTK Program database.')


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_create_data_controller(test_dao, test_configuration):
    """ __init__() should create an instance of a UsageProfile data controller. """
    DUT = dtcUsageProfile(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcUsageProfile)
    assert isinstance(DUT._dtm_data_model, dtmUsageProfile)


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_request_select_all(test_dao, test_configuration):
    """ request_select_all() should return a treelib Tree() with the Usage Profile. """
    DUT = dtcUsageProfile(test_dao, test_configuration, test=True)

    assert isinstance(DUT.request_select_all(1), Tree)


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_request_insert_mission(test_dao, test_configuration):
    """ request_insert() should return False on success. """
    DUT = dtcUsageProfile(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_insert(1, 0, 'mission')


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_request_delete(test_dao, test_configuration):
    """ request_delete() should return False on success. """
    DUT = dtcUsageProfile(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_delete(3)


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_request_delete_non_existent_id(test_dao, test_configuration):
    """ request_delete() should return True when attempting to delete a non-existent Node ID. """
    DUT = dtcUsageProfile(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert DUT.request_delete(222)


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_request_get_attributes(test_dao, test_configuration):
    """ request_get_attributes() should return a dict of {attribute name:attribute value} pairs. """
    DUT = dtcUsageProfile(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _attributes = DUT.request_get_attributes(1)

    assert isinstance(_attributes, dict)
    assert _attributes['revision_id'] == 1


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_request_set_attributes(test_dao, test_configuration):
    """ request_set_attributes() should return a zero error code on success. """
    DUT = dtcUsageProfile(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _error_code, _msg = DUT.request_set_attributes(1, ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Updating RTKMission 1 attributes.')


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_request_last_mission_id(test_dao, test_configuration):
    """ request_last_id() should return the last Mission ID used in the RTK Program database. """
    DUT = dtcUsageProfile(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _last_id = DUT.request_last_id('mission')

    assert _last_id == 2


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_request_last_mission_phase_id(test_dao, test_configuration):
    """ request_last_id() should return the last Mission Phase ID used in the RTK Program database. """
    DUT = dtcUsageProfile(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert DUT.request_last_id('phase') == 2


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_request_last_environment_id(test_dao, test_configuration):
    """ request_last_id() should return the last Environment ID used in the RTK Program database. """
    DUT = dtcUsageProfile(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert DUT.request_last_id('environment') == 2


@pytest.mark.integration
@pytest.mark.revision
@pytest.mark.usage
def test_request_update_all(test_dao, test_configuration):
    """ request_update_all() should return False on success. """
    DUT = dtcUsageProfile(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_update_all()
